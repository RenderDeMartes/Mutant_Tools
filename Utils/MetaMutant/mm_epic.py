"""
Epic's sample head DNA (Ada) for Meta Mutant, downloaded from Epic onto this machine.

Only needed when you have no MetaHuman DNA of your own. It comes from Epic's
MetaHuman-DNA-Calibration repository, whose licence allows using it in tools like
this one but not distributing it, so Mutant Tools does not ship it: each artist
downloads it from Epic after accepting Epic's licence, into a folder outside the
Mutant Tools repository.

    import mm_epic
    folder = mm_epic.default_dir(maya_app_dir)
    found = mm_epic.download(folder, accepted=True, progress=print)
    found.dna

Only the sample DNA, Epic's face board (gui.ma, the MetaHuman control board: Meta Mutant's face
board uses it when it is here) and the licence are downloaded (about 80 MB), not the whole
repository. Standard library only.
"""

from __future__ import annotations

import json
import os
import time
import urllib.request
from dataclasses import dataclass
from typing import Callable, Iterable, List, Optional

REPO = "EpicGames/MetaHuman-DNA-Calibration"
BRANCH = "main"
REPO_URL = f"https://github.com/{REPO}"
LICENSE_URL = f"{REPO_URL}/blob/{BRANCH}/LICENSE"
TREE_URL = f"https://api.github.com/repos/{REPO}/git/trees/{BRANCH}?recursive=1"
RAW_URL = f"https://raw.githubusercontent.com/{REPO}/{BRANCH}/"
FOLDER_NAME = "MetaHuman-DNA-Calibration"
SAMPLE_DNA = "data/mh4/dna_files/Ada.dna"
FACE_BOARD = "data/mh4/gui.ma"
ACCEPTED_FILE = "LICENSE_ACCEPTED.txt"
WANTED = ("LICENSE", "README.md", SAMPLE_DNA, FACE_BOARD)


@dataclass
class EpicFiles:
    root: str
    dna: str
    face_board: Optional[str] = None  # Epic's gui.ma, when downloaded


def default_dir(maya_app_dir: str) -> str:
    """<Maya user folder>/MetaMutant/epic: next to Mutant Tools, never inside it."""
    return os.path.join(maya_app_dir, "MetaMutant", "epic")


def wanted_files(tree: Iterable[dict]) -> List[dict]:
    """The blobs of the repository tree Meta Mutant needs."""
    return [item for item in tree if item.get("type") == "blob" and item.get("path") in WANTED]


def folder(root: str) -> str:
    """Where the download lives: <root>/MetaHuman-DNA-Calibration."""
    return os.path.join(root, FOLDER_NAME)


def found(root: str) -> Optional[EpicFiles]:
    """The downloaded sample DNA, when the licence was accepted and the file is there."""
    repo = folder(root)
    dna = os.path.join(repo, *SAMPLE_DNA.split("/"))
    if not (os.path.isfile(os.path.join(repo, ACCEPTED_FILE)) and os.path.isfile(dna)):
        return None
    board = os.path.join(repo, *FACE_BOARD.split("/"))
    return EpicFiles(repo, dna, board if os.path.isfile(board) else None)


def _open(url: str, timeout: float):
    request = urllib.request.Request(url, headers={"User-Agent": "MutantTools-MetaMutant"})
    return urllib.request.urlopen(request, timeout=timeout)


def fetch_tree(opener=_open, timeout: float = 30) -> List[dict]:
    with opener(TREE_URL, timeout) as response:
        data = json.loads(response.read().decode("utf-8"))
    if data.get("truncated"):
        raise RuntimeError("Epic's repository listing came back incomplete; try again later")
    return data.get("tree", [])


def _safe_target(repo: str, path: str) -> str:
    """repo/<path>, refusing anything that would land outside repo."""
    parts = path.split("/")
    if not path or path.startswith("/") or any(p in ("", ".", "..") or ":" in p or "\\" in p for p in parts):
        raise RuntimeError(f"unexpected path in Epic's repository: {path!r}")
    target = os.path.abspath(os.path.join(repo, *parts))
    if os.path.commonpath([target, os.path.abspath(repo)]) != os.path.abspath(repo):
        raise RuntimeError(f"unexpected path in Epic's repository: {path!r}")
    return target


def remove(root: str) -> bool:
    """Delete the download (only the MetaHuman-DNA-Calibration folder this module made). True when removed."""
    import shutil

    repo = folder(root)
    if not os.path.isdir(repo):
        return False
    if not os.path.isfile(os.path.join(repo, ACCEPTED_FILE)) and not os.path.isfile(os.path.join(repo, *SAMPLE_DNA.split("/"))):
        raise RuntimeError(f"{repo} does not look like Meta Mutant's download; not deleting it")
    shutil.rmtree(repo)
    return True


def download(root: str, accepted: bool = False, progress: Callable[[str], None] = print, opener=_open,
             timeout: float = 60, fraction: Optional[Callable[[float], None]] = None, force: bool = False) -> EpicFiles:
    """
    Download the sample DNA from Epic into <root>/MetaHuman-DNA-Calibration. Files already there
    with the right size are kept (an update fetches only what changed); `force` downloads them
    again. `accepted` must be True: the artist accepted Epic's licence. `fraction(0..1)` follows
    the bytes, for a progress bar.
    """
    fraction = fraction or (lambda f: None)
    if not accepted:
        raise RuntimeError(f"accept Epic's MetaHuman DNA Calibration licence first: {LICENSE_URL}")
    repo = folder(root)
    os.makedirs(repo, exist_ok=True)
    files = wanted_files(fetch_tree(opener))
    if not any(f["path"] == SAMPLE_DNA for f in files):
        raise RuntimeError(f"{SAMPLE_DNA} is no longer in Epic's repository; use your own MetaHuman's DNA instead")
    total = sum(f.get("size") or 0 for f in files)
    done = 0
    for f in files:
        target = _safe_target(repo, f["path"])
        size = f.get("size") or 0
        if not force and os.path.isfile(target) and os.path.getsize(target) == size:
            done += size
            fraction(done / max(total, 1))
            continue
        os.makedirs(os.path.dirname(target), exist_ok=True)
        part = target + ".part"
        with opener(RAW_URL + f["path"], timeout) as response, open(part, "wb") as out:
            while True:
                chunk = response.read(1 << 20)
                if not chunk:
                    break
                out.write(chunk)
                done += len(chunk)
                fraction(min(done / max(total, 1), 1.0))
                if size > 1 << 22:
                    progress(f"{f['path']}: {done * 100 // max(total, 1)}% of {total / 1e6:.0f} MB")
        if size and os.path.getsize(part) != size:
            os.remove(part)
            raise RuntimeError(f"{f['path']} downloaded incomplete; try again")
        os.replace(part, target)
    with open(os.path.join(repo, ACCEPTED_FILE), "w", encoding="utf-8") as note:
        note.write(f"Epic's MetaHuman DNA Calibration licence ({LICENSE_URL}) accepted in Meta Mutant on "
                   f"{time.strftime('%Y-%m-%d %H:%M')} before downloading these files from {REPO_URL}.\n"
                   "Do not commit or share this folder: the licence does not allow distributing it.\n")
    result = found(root)
    if result is None:
        raise RuntimeError(f"the download in {repo} is incomplete; try again")
    progress(f"Epic's sample DNA is in {repo}")
    return result
