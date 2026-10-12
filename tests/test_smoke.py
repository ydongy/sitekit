import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO))
sys.path.insert(0, str(REPO / "sitekit"))


class SmokeTest(unittest.TestCase):
    def test_package_exports(self):
        import sitekit

        for name in ("Site", "Page", "build", "load", "attr", "DEFAULT_PAGES"):
            self.assertTrue(hasattr(sitekit, name), name)

    def test_site_defaults(self):
        from sitekit import DEFAULT_PAGES, Site

        site = Site(root=Path("/tmp/x"), url="https://example.com", name="Example",
                    contact="hi@example.com", theme=(("#fff", "light"), ("#000", "dark")))
        self.assertEqual(site.public, Path("/tmp/x/public"))
        self.assertEqual(site.pages, DEFAULT_PAGES)
        self.assertIn('media="(prefers-color-scheme: dark)"', site.theme_meta())

    def test_attr_escapes(self):
        from sitekit import attr

        self.assertNotIn('"', attr('a "quoted" value'))

    def test_checks_import(self):
        import check_i18n  # check_site and preview run at import time; compileall covers them

        tags_a, marks_a = check_i18n.shape('<a href="x">{v}</a>')
        tags_b, marks_b = check_i18n.shape('<a href="x">{v} y</a>')
        self.assertEqual((tags_a, marks_a), (tags_b, marks_b))
        self.assertNotEqual(check_i18n.shape("<b>x</b>"), check_i18n.shape("x"))

    def test_vendor_script(self):
        with tempfile.TemporaryDirectory() as tmp:
            (Path(tmp) / "scripts").mkdir()
            subprocess.run(["bash", str(REPO / "vendor.sh"), tmp], check=True, capture_output=True)
            dest = Path(tmp) / "scripts" / "sitekit"
            for name in ("core.py", "check_i18n.py", "check_site.py", "preview.py", "VERSION"):
                self.assertTrue((dest / name).is_file(), name)
            shutil.rmtree(dest)


if __name__ == "__main__":
    unittest.main()
