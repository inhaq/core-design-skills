"""Tests for skills/core-design/scripts/check-tells.py. Run: python3 -m unittest discover tests"""

import importlib.util
import pathlib
import unittest

ROOT = pathlib.Path(__file__).resolve().parent.parent
FIXTURES = ROOT / "tests" / "fixtures"

spec = importlib.util.spec_from_file_location("check_tells", ROOT / "skills/core-design/scripts/check-tells.py")
check_tells = importlib.util.module_from_spec(spec)
spec.loader.exec_module(check_tells)


def names(path):
    return {(line, name) for line, _tag, name, _fix in check_tells.scan(str(path))}


class BadFixture(unittest.TestCase):
    def setUp(self):
        self.hits = names(FIXTURES / "bad.tsx")

    def test_left_bar_variants(self):
        self.assertIn((2, "left-edge accent bar"), self.hits)
        self.assertIn((3, "left-edge bar via inset shadow"), self.hits)
        self.assertIn((4, "left-edge bar via ::before"), self.hits)

    def test_tracking_either_order(self):
        self.assertIn((5, "wide uppercase tracking"), self.hits)

    def test_core_tells(self):
        self.assertIn((6, "h-screen"), self.hits)
        self.assertIn((7, "transition: all"), self.hits)
        self.assertIn((8, "focus outline removed"), self.hits)
        self.assertIn((12, "buzzword copy"), self.hits)

    def test_multiline_div_onclick(self):
        self.assertIn((9, "div with onClick"), self.hits)

    def test_ignore_pragma(self):
        self.assertFalse([h for h in self.hits if h[0] == 13])


class GoodFixture(unittest.TestCase):
    def test_no_false_alarms(self):
        self.assertEqual(check_tells.scan(str(FIXTURES / "good.css")), [])


class Tags(unittest.TestCase):
    def tags(self, path):
        return {name: tag for _line, tag, name, _fix in check_tells.scan(str(path))}

    def test_min_h_screen_is_not_h_screen(self):
        tags = self.tags(FIXTURES / "no-reduced-motion.css")
        self.assertNotIn("h-screen", tags)
        self.assertEqual(tags["100vh min-height"], "default")

    def test_decorative_loop_is_default(self):
        self.assertEqual(self.tags(FIXTURES / "no-reduced-motion.css")["infinite animation"], "default")

    def test_missing_reduced_motion_is_always(self):
        self.assertEqual(self.tags(FIXTURES / "no-reduced-motion.css")["motion with no reduced-motion fallback"], "always")


class ExitCode(unittest.TestCase):
    def test_exit_codes(self):
        self.assertEqual(check_tells.main(["x", str(FIXTURES / "bad.tsx")]), 1)
        self.assertEqual(check_tells.main(["x", str(FIXTURES / "good.css")]), 0)


if __name__ == "__main__":
    unittest.main()
