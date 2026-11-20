"""Tests for skills/core-design/scripts/check-tells.py. Run: python3 -m unittest discover tests"""

import contextlib
import importlib.util
import io
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
        self.assertFalse([h for h in self.hits if h[0] in (13, 14)])

    def test_focus_removal_variants(self):
        self.assertIn((15, "focus outline removed"), self.hits)  # focus-visible:outline-none
        self.assertIn((16, "focus outline removed"), self.hits)  # ring-0 is not a ring
        self.assertIn((17, "focus outline removed"), self.hits)  # Tailwind v4 outline-hidden

    def test_div_onclick_after_arrow_function(self):
        self.assertIn((18, "div with onClick"), self.hits)

    def test_italic_word_in_headline(self):
        self.assertIn((19, "italic or gradient word in headline"), self.hits)


class OtherBadFixtures(unittest.TestCase):
    def test_star_selectors_are_not_comments(self):
        hits = names(FIXTURES / "bad.css")
        self.assertIn((2, "focus outline removed"), hits)
        self.assertIn((3, "transition: all"), hits)

    def test_vue_and_svelte_click_handlers(self):
        self.assertIn((2, "div with onClick"), names(FIXTURES / "bad.vue"))
        self.assertIn((1, "div with onClick"), names(FIXTURES / "bad.svelte"))


class GoodFixture(unittest.TestCase):
    def test_no_false_alarms_css(self):
        # Includes multi-line :focus:not(:focus-visible), main:focus, border-left-color, block comments.
        self.assertEqual(check_tells.scan(str(FIXTURES / "good.css")), [])

    def test_no_false_alarms_product_tsx(self):
        # Ring before outline-none, ring on the next line of cn(), skip-link <main>,
        # divs with role or aria-hidden, an @unleash import, an "acme" slug.
        self.assertEqual(check_tells.scan(str(FIXTURES / "focus.tsx")), [])

    def test_spinner_needs_no_reduced_motion_block(self):
        self.assertEqual(check_tells.scan(str(FIXTURES / "spinner.css")), [])

    def test_only_defaults_in_tsx(self):
        # Comments, placeholder examples, focus-within wrappers: no [always] hits.
        hits = check_tells.scan(str(FIXTURES / "good.tsx"))
        self.assertEqual([h for h in hits if h[1] == "always"], [])
        self.assertIn("pulse", {h[2] for h in hits})

    def test_rtl_is_opt_in(self):
        plain = {h[2] for h in check_tells.scan(str(FIXTURES / "good.tsx"))}
        rtl = {h[2] for h in check_tells.scan(str(FIXTURES / "good.tsx"), rtl=True)}
        self.assertNotIn("physical left/right spacing", plain)
        self.assertIn("physical left/right spacing", rtl)


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

    def test_bounce_is_default(self):
        # A loader or typing dot can bounce; the checker can't tell it from a CTA.
        self.assertEqual(self.tags(FIXTURES / "good.tsx")["bounce/ping"], "default")


class Walk(unittest.TestCase):
    def test_folder_scan_skips_test_files(self):
        walked = {pathlib.Path(p).name for p in check_tells.iter_files([str(FIXTURES)])}
        self.assertIn("bad.tsx", walked)
        self.assertNotIn("profile.test.tsx", walked)

    def test_test_file_named_directly_is_scanned(self):
        self.assertIn((2, "placeholder people/companies"), names(FIXTURES / "profile.test.tsx"))


class ExitCode(unittest.TestCase):
    def test_exit_codes(self):
        with contextlib.redirect_stdout(io.StringIO()), contextlib.redirect_stderr(io.StringIO()):
            self.assertEqual(check_tells.main(["x", str(FIXTURES / "bad.tsx")]), 1)
            self.assertEqual(check_tells.main(["x", str(FIXTURES / "good.css")]), 0)
            self.assertEqual(check_tells.main(["x", "--only", "always", str(FIXTURES / "bad.tsx")]), 1)
            self.assertEqual(check_tells.main(["x", "--only", "nope", str(FIXTURES / "bad.tsx")]), 2)
            self.assertEqual(check_tells.main(["x", str(FIXTURES / "no-such-dir")]), 2)
            self.assertEqual(check_tells.main(["x", "--help"]), 0)


if __name__ == "__main__":
    unittest.main()
