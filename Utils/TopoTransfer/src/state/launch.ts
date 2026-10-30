/**
 * Launch parameters: a local tool (a Maya tool through maya/tt_bridge.py) opens
 * the app as `?base=<url>&reference=<url>&return=<url>`. The meshes are
 * fetched from those URLs and loaded through the normal loader; Export then
 * POSTs the result to `return` instead of downloading it.
 *
 * Only loopback URLs (localhost, 127.0.0.1, [::1]) are accepted, so a link on
 * a web page cannot make the app fetch from or send meshes to another host.
 */

export interface LaunchParams {
  base: string | null;
  reference: string | null;
  returnUrl: string | null;
  /** rejected parameters, as messages for the log */
  errors: string[];
}

const LOOPBACK_HOSTS = new Set(['localhost', '127.0.0.1', '[::1]']);
const PARAMS = ['base', 'reference', 'return'] as const;

/** True for an http(s) URL on this machine without credentials in it. */
export function isLoopbackUrl(value: string): boolean {
  let u: URL;
  try {
    u = new URL(value);
  } catch {
    return false;
  }
  return (u.protocol === 'http:' || u.protocol === 'https:') && LOOPBACK_HOSTS.has(u.hostname.toLowerCase()) && !u.username && !u.password;
}

export function parseLaunchParams(search: string): LaunchParams {
  const q = new URLSearchParams(search);
  const out: LaunchParams = { base: null, reference: null, returnUrl: null, errors: [] };
  for (const key of PARAMS) {
    const v = q.get(key);
    if (v === null || v === '') continue;
    if (!isLoopbackUrl(v)) {
      out.errors.push(`Ignored "${key}" URL: only http(s) URLs on this machine (localhost, 127.0.0.1, [::1]) are accepted.`);
      continue;
    }
    if (key === 'return') out.returnUrl = v;
    else out[key] = v;
  }
  return out;
}

export function hasLaunchParams(p: LaunchParams): boolean {
  return !!(p.base || p.reference || p.returnUrl || p.errors.length);
}

/** The page URL without the launch parameters (they carry the bridge's access token). */
export function stripLaunchParams(href: string): string {
  const u = new URL(href);
  for (const key of PARAMS) u.searchParams.delete(key);
  return u.toString();
}

/** File name for the loader (format detection, export name) from the URL's last path segment. */
export function fileNameFromUrl(url: string, fallback: string): string {
  const seg = new URL(url).pathname.split('/').filter(Boolean).pop() ?? '';
  let name = seg;
  try {
    name = decodeURIComponent(seg);
  } catch {
    // keep the raw segment
  }
  name = name.replace(/[\\/]/g, '_');
  return name || fallback;
}

type Fetch = typeof fetch;

/** Fetch a mesh from a loopback URL; redirects are refused so the request cannot leave this machine. */
export async function fetchLaunchFile(url: string, fallbackName: string, fetchImpl: Fetch = fetch): Promise<{ name: string; buffer: ArrayBuffer }> {
  if (!isLoopbackUrl(url)) throw new Error(`${url} is not a loopback URL`);
  const r = await fetchImpl(url, { credentials: 'omit', redirect: 'error', cache: 'no-store' });
  if (!r.ok) throw new Error(`HTTP ${r.status} ${r.statusText}`.trim());
  return { name: fileNameFromUrl(url, fallbackName), buffer: await r.arrayBuffer() };
}

/** POST an exported file to the return URL. Resolves to the receiver's message (JSON `message` or text). */
export async function postResult(url: string, data: BlobPart, fetchImpl: Fetch = fetch): Promise<string> {
  if (!isLoopbackUrl(url)) throw new Error(`${url} is not a loopback URL`);
  // text/plain and no custom headers keep this a CORS "simple" request (no preflight);
  // the receiver chooses the file name
  const r = await fetchImpl(url, {
    method: 'POST',
    body: new Blob([data], { type: 'text/plain' }),
    headers: { 'Content-Type': 'text/plain' },
    credentials: 'omit',
    redirect: 'error',
    cache: 'no-store',
  });
  const text = await r.text();
  let message = text;
  try {
    const j = JSON.parse(text) as { message?: unknown };
    if (typeof j.message === 'string') message = j.message;
  } catch {
    // plain text answer
  }
  if (!r.ok) throw new Error(message || `HTTP ${r.status}`);
  return message;
}
