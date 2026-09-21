#!/usr/bin/env python3
"""Push a release zip onto a Gumroad product.

Gumroad's v2 API takes files in three steps: ask for a presigned multipart
upload, PUT each part to S3 yourself, then tell Gumroad the upload finished.
Only then can the resulting file URL be attached to a product.

    POST /v2/files/presign    filename, file_size  -> upload_id, key, parts[]
    PUT  <presigned_url>      each 100 MB part     -> ETag response header
    POST /v2/files/complete   upload_id, key, parts -> canonical file_url
    PUT  /v2/products/:id     files=[{url, ...}]   -> attaches it

Usage:
    gumroad_sync.py DIST.zip --version 1.6 [--ensure-link] [--dry-run]

Environment:
    GUMROAD_ACCESS_TOKEN   OAuth token with the edit_products scope
    GUMROAD_PRODUCT_ID     the product's permalink (the code in its URL) or id

Standard library only - runners should not need a pip install to ship a release.
"""
from __future__ import annotations

import argparse
import json
import os
import sys
import urllib.error
import urllib.request

API = "https://api.gumroad.com/v2"

# Must match Api::V2::FilesController::PART_SIZE. presign divides file_size by
# this to decide how many presigned URLs to hand back, so a different chunk size
# here means the part count will not line up.
PART_SIZE = 100 * 1024 * 1024

LINK_MARKER = "<!-- mutant-tools-latest-release -->"
RELEASES_URL = "https://github.com/RenderDeMartes/Mutant_Tools/releases/latest"


class GumroadError(RuntimeError):
    pass


def _request(method, url, token=None, body=None, headers=None, raw=False):
    data = None
    hdrs = dict(headers or {})
    if body is not None and not raw:
        data = json.dumps(body).encode("utf-8")
        hdrs["Content-Type"] = "application/json"
    elif raw:
        data = body
    if token:
        hdrs["Authorization"] = "Bearer " + token

    req = urllib.request.Request(url, data=data, headers=hdrs, method=method)
    try:
        with urllib.request.urlopen(req, timeout=600) as resp:
            return resp.status, resp.headers, resp.read()
    except urllib.error.HTTPError as exc:
        return exc.code, exc.headers, exc.read()


def _api(method, path, token, body=None):
    status, _, payload = _request(method, API + path, token=token, body=body)
    try:
        parsed = json.loads(payload.decode("utf-8"))
    except ValueError:
        raise GumroadError("%s %s returned non-JSON (HTTP %s): %s"
                           % (method, path, status, payload[:300]))
    if status >= 400 or not parsed.get("success", True):
        raise GumroadError("%s %s failed (HTTP %s): %s"
                           % (method, path, status, parsed.get("message", parsed)))
    return parsed


def upload(token, path):
    """Run the three-step upload. Returns the canonical file URL."""
    filename = os.path.basename(path)
    size = os.path.getsize(path)
    print("uploading %s (%.1f MB)" % (filename, size / 1048576.0))

    presigned = _api("POST", "/files/presign", token,
                     {"filename": filename, "file_size": size})
    upload_id = presigned["upload_id"]
    key = presigned["key"]
    parts = presigned["parts"]
    print("  %d part(s), upload_id=%s" % (len(parts), upload_id))

    finished = []
    try:
        with open(path, "rb") as handle:
            for part in sorted(parts, key=lambda p: int(p["part_number"])):
                number = int(part["part_number"])
                chunk = handle.read(PART_SIZE)
                if not chunk:
                    raise GumroadError("ran out of data at part %d - file changed mid-upload?" % number)
                status, headers, payload = _request(
                    "PUT", part["presigned_url"], body=chunk, raw=True,
                    headers={"Content-Length": str(len(chunk))})
                if status >= 400:
                    raise GumroadError("part %d rejected by S3 (HTTP %s): %s"
                                       % (number, status, payload[:300]))
                etag = headers.get("ETag") or headers.get("Etag")
                if not etag:
                    raise GumroadError("part %d uploaded but S3 returned no ETag" % number)
                finished.append({"part_number": number, "etag": etag})
                print("  part %d/%d ok (%.1f MB)" % (number, len(parts), len(chunk) / 1048576.0))
    except Exception:
        # Anything before `complete` leaves a dangling multipart upload that S3
        # will bill for. Tidy it up, but never let cleanup mask the real error.
        try:
            _api("POST", "/files/abort", token, {"upload_id": upload_id, "key": key})
            print("  aborted the incomplete upload")
        except Exception as cleanup_error:      # noqa: BLE001
            print("  could not abort upload %s: %s" % (upload_id, cleanup_error))
        raise

    # /files/complete accepts an upload_id exactly once. If this throws, do NOT
    # retry it - start again from presign.
    done = _api("POST", "/files/complete", token,
                {"upload_id": upload_id, "key": key, "parts": finished})
    print("  complete -> %s" % done["file_url"])
    return done["file_url"]


def resolve_product(token, wanted):
    """Return (id, product) for `wanted`, however the seller identified it.

    GET /v2/products/:id only resolves an external id or a *unique* permalink -
    Gumroad's auto-generated code. The slug in a product's own URL is usually the
    *custom* permalink, which that endpoint rejects with "The product was not
    found" even though the model has a by_general_permalink scope covering both.
    So fall back to the list and match on anything a person might reasonably have
    pasted.
    """
    try:
        product = _api("GET", "/products/%s" % wanted, token).get("product", {})
        return wanted, product
    except GumroadError:
        pass

    products = _api("GET", "/products", token).get("products", []) or []
    for product in products:
        candidates = {
            str(product.get("id") or ""),
            str(product.get("custom_permalink") or ""),
            str(product.get("unique_permalink") or ""),
            str(product.get("short_url") or "").rstrip("/").rsplit("/", 1)[-1],
        }
        if wanted in candidates - {""}:
            resolved = product.get("id") or wanted
            print("resolved %r to product id %s" % (wanted, resolved))
            return resolved, product

    names = ", ".join(
        "%s (%s)" % (p.get("name"), str(p.get("short_url") or "").rstrip("/").rsplit("/", 1)[-1])
        for p in products) or "none"
    raise GumroadError("no product matches %r. This account has: %s" % (wanted, names))


def attach(token, product_id, file_url, display_name):
    """Point the product at the new file.

    `files` is the product's whole desired file list, not an addition - anything
    left out is removed. That is what we want: one zip, replaced each release.
    """
    result = _api("PUT", "/products/%s" % product_id, token,
                  {"files": [{"url": file_url, "display_name": display_name}]})
    product = result.get("product", {})
    print("attached to %r" % (product.get("name") or product_id))
    return product


def ensure_link(token, product_id, product=None):
    """Append a link to the GitHub releases page, once.

    A fallback for the day a release run fails: buyers can still find the
    current version themselves. Idempotent via an HTML comment marker, and only
    ever appends - it never rewrites what is already there.
    """
    if product is None:
        product = _api("GET", "/products/%s" % product_id, token).get("product", {})
    description = product.get("description") or ""
    if LINK_MARKER in description:
        print("releases link already present")
        return
    addition = ('%s\n<p>Latest version, always: '
                '<a href="%s">github.com/RenderDeMartes/Mutant_Tools/releases/latest</a></p>'
                % (LINK_MARKER, RELEASES_URL))
    _api("PUT", "/products/%s" % product_id, token,
         {"description": description + "\n" + addition})
    print("added the releases link to the product description")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("zip_path")
    parser.add_argument("--version", required=True)
    parser.add_argument("--ensure-link", action="store_true",
                        help="append a GitHub releases link to the description if absent")
    parser.add_argument("--dry-run", action="store_true",
                        help="check credentials and the product, upload nothing")
    args = parser.parse_args()

    token = os.environ.get("GUMROAD_ACCESS_TOKEN", "").strip()
    product_id = os.environ.get("GUMROAD_PRODUCT_ID", "").strip()
    if not token or not product_id:
        print("GUMROAD_ACCESS_TOKEN and GUMROAD_PRODUCT_ID are not both set - skipping Gumroad.")
        return 0
    if not os.path.isfile(args.zip_path):
        print("no such file: %s" % args.zip_path, file=sys.stderr)
        return 1

    try:
        product_id, product = resolve_product(token, product_id)
        print("product: %s (%s)" % (product.get("name"), product.get("short_url") or product_id))

        if args.dry_run:
            print("dry run - would upload %s (%.1f MB)"
                  % (os.path.basename(args.zip_path),
                     os.path.getsize(args.zip_path) / 1048576.0))
            return 0

        file_url = upload(token, args.zip_path)
        attach(token, product_id, file_url, "Mutant Tools %s.zip" % args.version)
        if args.ensure_link:
            ensure_link(token, product_id)
    except GumroadError as exc:
        print("Gumroad sync failed: %s" % exc, file=sys.stderr)
        return 1

    print("Gumroad is now serving Mutant Tools %s" % args.version)
    return 0


if __name__ == "__main__":
    sys.exit(main())
