"""
Tests for mm_epic (downloading Epic's sample DNA). No network: a fake opener plays Epic's repository.

    python -m unittest discover -s tests -v
"""

import io
import json
import os
import sys
import tempfile
import unittest

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, ".."))

import mm_epic  # noqa: E402

FILES = {
    "LICENSE": b"MetaHuman DNA Calibration License Agreement",
    "README.md": b"# readme",
    mm_epic.SAMPLE_DNA: b"DNA" * 2000000,
    mm_epic.FACE_BOARD: b"//Maya ASCII 2023 scene",
    "data/gui.ma": b"older board, not wanted",
    "dna_viewer/__init__.py": b"not wanted any more",
    "data/dna_files/Taro.dna": b"not wanted",
    "lib/Maya2024/windows/dna.py": b"not wanted",
}


class FakeEpic:
    def __init__(self, files=FILES, truncated=False):
        self.files = dict(files)
        self.truncated = truncated
        self.urls = []

    def tree(self):
        items = [{"path": p, "type": "blob", "size": len(b)} for p, b in self.files.items()]
        items.append({"path": "data", "type": "tree"})
        return {"tree": items, "truncated": self.truncated}

    def __call__(self, url, timeout):
        self.urls.append(url)
        if url == mm_epic.TREE_URL:
            return io.BytesIO(json.dumps(self.tree()).encode())
        assert url.startswith(mm_epic.RAW_URL), url
        return io.BytesIO(self.files[url[len(mm_epic.RAW_URL):]])


class TestEpicDownload(unittest.TestCase):
    def test_nothing_without_accepting_the_licence(self):
        epic = FakeEpic()
        with tempfile.TemporaryDirectory() as root:
            with self.assertRaises(RuntimeError) as e:
                mm_epic.download(root, accepted=False, opener=epic)
            self.assertIn("licence", str(e.exception))
            self.assertEqual(epic.urls, [])
            self.assertEqual(os.listdir(root), [])

    def test_downloads_only_the_sample_dna_and_the_licence(self):
        epic = FakeEpic()
        with tempfile.TemporaryDirectory() as root:
            said, bar = [], []
            got = mm_epic.download(root, accepted=True, opener=epic, progress=said.append, fraction=bar.append)
            repo = mm_epic.folder(root)
            on_disk = sorted(os.path.relpath(os.path.join(d, f), repo).replace(os.sep, "/")
                             for d, _, fs in os.walk(repo) for f in fs)
            self.assertEqual(on_disk, sorted(["LICENSE", "README.md", mm_epic.ACCEPTED_FILE, mm_epic.SAMPLE_DNA, mm_epic.FACE_BOARD]))
            self.assertEqual(got.dna, os.path.join(repo, "data", "mh4", "dna_files", "Ada.dna"))
            self.assertEqual(bar, sorted(bar))  # only goes forward
            self.assertAlmostEqual(bar[-1], 1.0)
            self.assertTrue(any("%" in s for s in said))
            self.assertEqual(mm_epic.found(root), got)
            epic.urls.clear()  # a second run downloads nothing again
            mm_epic.download(root, accepted=True, opener=epic, progress=lambda s: None)
            self.assertEqual(epic.urls, [mm_epic.TREE_URL])

    def test_update_fetches_what_changed_and_force_fetches_everything(self):
        epic = FakeEpic()
        with tempfile.TemporaryDirectory() as root:
            mm_epic.download(root, accepted=True, opener=epic, progress=lambda s: None)
            epic.files["README.md"] = b"# readme, newer and longer"
            epic.urls.clear()
            mm_epic.download(root, accepted=True, opener=epic, progress=lambda s: None)
            self.assertEqual(epic.urls, [mm_epic.TREE_URL, mm_epic.RAW_URL + "README.md"])
            epic.urls.clear()
            mm_epic.download(root, accepted=True, opener=epic, progress=lambda s: None, force=True)
            self.assertEqual(len(epic.urls), 1 + len(mm_epic.WANTED))

    def test_refuses_bad_listings(self):
        with tempfile.TemporaryDirectory() as root:
            with self.assertRaises(RuntimeError):
                mm_epic.download(root, accepted=True, opener=FakeEpic(truncated=True), progress=lambda s: None)
            no_dna = {p: b for p, b in FILES.items() if p != mm_epic.SAMPLE_DNA}
            with self.assertRaises(RuntimeError):
                mm_epic.download(root, accepted=True, opener=FakeEpic(no_dna), progress=lambda s: None)
        with tempfile.TemporaryDirectory() as repo:
            with self.assertRaises(RuntimeError):
                mm_epic._safe_target(repo, "data/../../escape.dna")

    def test_remove_deletes_only_the_download(self):
        with tempfile.TemporaryDirectory() as root:
            self.assertFalse(mm_epic.remove(root))
            got = mm_epic.download(root, accepted=True, opener=FakeEpic(), progress=lambda s: None)
            mine = os.path.join(root, "keep.txt")
            open(mine, "w").close()
            self.assertTrue(mm_epic.remove(root))
            self.assertFalse(os.path.exists(got.root))
            self.assertTrue(os.path.isfile(mine))
            os.makedirs(os.path.join(mm_epic.folder(root), "something"))  # same name, not the download
            with self.assertRaises(RuntimeError):
                mm_epic.remove(root)
            self.assertTrue(os.path.isdir(os.path.join(mm_epic.folder(root), "something")))

    def test_found_needs_the_accepted_licence(self):
        with tempfile.TemporaryDirectory() as root:
            got = mm_epic.download(root, accepted=True, opener=FakeEpic(), progress=lambda s: None)
            os.remove(os.path.join(got.root, mm_epic.ACCEPTED_FILE))
            self.assertIsNone(mm_epic.found(root))

    def test_default_dir_is_outside_mutant_tools(self):
        self.assertEqual(mm_epic.default_dir(os.path.join("C:", "maya")), os.path.join("C:", "maya", "MetaMutant", "epic"))


if __name__ == "__main__":
    unittest.main()
