import sys
import tempfile
import unittest
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO / "sitekit"))

import preview  # noqa: E402


class ResolveTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        root = Path(self.tmp.name).resolve()
        (root / "public" / "zh").mkdir(parents=True)
        (root / "public" / "faq.html").write_text("faq")
        (root / "secret.txt").write_text("secret")
        self.saved, preview.PUB = preview.PUB, root / "public"

    def tearDown(self):
        preview.PUB = self.saved
        self.tmp.cleanup()

    def test_paths_inside_public(self):
        self.assertEqual(preview.resolve("/faq?x=1")[0], "/faq")
        self.assertEqual(preview.resolve("/zh/")[0], "/zh/")
        self.assertEqual(preview.resolve("/zh/./")[0], "/zh/")
        self.assertEqual(preview.resolve("/")[1], preview.PUB)

    def test_paths_never_leave_public(self):
        # ".." above the root collapses (as browsers do); the result is refused or stays inside public/.
        for path in ("/../secret.txt", "/%2e%2e/secret.txt", "/zh/../../secret.txt", "/..%2fsecret.txt"):
            result = preview.resolve(path)
            if result is not None:
                self.assertIn(preview.PUB, [result[1], *result[1].parents], path)
                self.assertFalse(result[1].exists(), path)

    def test_control_characters_are_refused(self):
        for path in ("/zh%0d%0aX-Evil:1", "/a%00b", "/a%5cb", "relative"):
            self.assertIsNone(preview.resolve(path), path)


if __name__ == "__main__":
    unittest.main()
