#!/usr/bin/env python3
"""Self-test of tools/blog.py. Works on a temporary copy of the repository, so
the tree is never changed.  Run: python3 tools/blog_selftest.py"""
import pathlib
import re
import shutil
import subprocess
import sys
import tempfile
import unittest

REPO = pathlib.Path(__file__).resolve().parent.parent


def run(cwd, *args, ok=True):
    p = subprocess.run([sys.executable, str(cwd / "tools" / "blog.py"), *args], cwd=cwd, capture_output=True, text=True)
    if ok and p.returncode != 0:
        raise AssertionError(f"blog.py {' '.join(args)} failed:\n{p.stdout}\n{p.stderr}")
    if not ok and p.returncode == 0:
        raise AssertionError(f"blog.py {' '.join(args)} should have failed:\n{p.stdout}")
    return p


class BlogTest(unittest.TestCase):
    def setUp(self):
        self.tmp = pathlib.Path(tempfile.mkdtemp(prefix="blogtest-"))
        for name in ("tools", "blog", "assets", "sitemap.xml", "favicon.svg", "card.png"):
            src = REPO / name
            if src.is_dir():
                shutil.copytree(src, self.tmp / name, ignore=shutil.ignore_patterns("__pycache__"))
            else:
                shutil.copy2(src, self.tmp / name)
        self.demo = next((self.tmp / "blog").glob("0001_*"))

    def tearDown(self):
        shutil.rmtree(self.tmp, ignore_errors=True)

    def read(self, rel):
        return (self.tmp / rel).read_text(encoding="utf-8")

    def test_draft_is_not_listed_and_previews(self):
        run(self.tmp, "build", "--number", "1")
        self.assertFalse((self.tmp / "blog" / "index.html").exists())
        self.assertNotIn("/blog/", self.read("sitemap.xml"))
        self.assertTrue((self.tmp / ".blog-preview/blog/0001-blog-features-demo/index.html").exists())
        self.assertTrue((self.tmp / ".blog-preview/ru/blog/0001-blog-features-demo/figure.png").exists())
        self.assertFalse((self.tmp / "blog/0001-blog-features-demo").exists())

    def test_publish_cycle(self):
        run(self.tmp, "publish", "--number", "1", "--date", "2026-12-05")
        run(self.tmp, "publish", "--number", "1", ok=False)
        for lang_prefix in ("", "ru/"):
            page = self.read(f"{lang_prefix}blog/0001-blog-features-demo/index.html")
            self.assertIn('rel="canonical"', page)
            self.assertIn('hreflang="en"', page)
            self.assertIn('hreflang="ru"', page)
            self.assertIn('property="og:image"', page)
            self.assertIn('name="twitter:card"', page)
            self.assertIn('"@type": "BlogPosting"', page)
            self.assertIn('"datePublished": "2026-12-05"', page)
            self.assertNotIn("noindex", page)
            self.assertIn('class="code code-tabs"', page)
            self.assertIn('class="table-wrap"', page)
            self.assertIn("<figcaption>", page)
            self.assertIn('class="footnote-backref"', page)
            self.assertIn('class="headerlink"', page)
            self.assertIn('target="_blank" rel="noopener"', page)
            self.assertIn('loading="lazy"', page)
            self.assertIn('class="hl"', page)
            self.assertTrue((self.tmp / f"{lang_prefix}blog/0001-blog-features-demo/cover.png").exists())
        for rel in ("blog/index.html", "ru/blog/index.html", "blog/tags/demo/index.html", "ru/blog/tags/blog/index.html"):
            self.assertIn("0001-blog-features-demo", self.read(rel))
        sm = self.read("sitemap.xml")
        self.assertIn("https://donmutti.com/blog/0001-blog-features-demo/", sm)
        self.assertIn("https://donmutti.com/ru/blog/tags/demo/", sm)
        self.assertEqual(sm.count("https://donmutti.com/events/</loc>"), 1)
        run(self.tmp, "build")
        self.assertEqual(self.read("sitemap.xml"), sm, "build is idempotent")

    def test_code_tabs_group_only_different_languages(self):
        run(self.tmp, "publish", "--number", "1", "--date", "2026-12-05")
        page = self.read("blog/0001-blog-features-demo/index.html")
        self.assertEqual(page.count('class="code code-tabs"'), 2)
        first = page.split('class="code code-tabs"')[1]
        self.assertEqual(first.split('<h2')[0].count('role="tab"'), 3)

    def test_start_numbers_and_state_helpers(self):
        run(self.tmp, "start", "second-article", "--target", "2027-01", "--title", "Second")
        folder = self.tmp / "blog" / "0002_second-article"
        self.assertTrue((folder / "2027-01-xx_x.md").exists())
        self.assertTrue((folder / "2027-01-xx_linkedin.md").exists())
        run(self.tmp, "start", "second-article", "--target", "2027-01", ok=False)
        run(self.tmp, "publish", "--number", "2", ok=False)  # no description
        run(self.tmp, "publish", "--number", "1", "--date", "2026-12-05")
        run(self.tmp, "post-published", "--number", "1", "--file", "2026-12-xx_x.md", "--url", "https://x.com/a/status/1", "--date", "2026-12-06")
        self.assertTrue((self.demo / "2026-12-06_x.md").exists())
        self.assertFalse((self.demo / "2026-12-xx_x.md").exists())
        text = (self.demo / "2026-12-06_x.md").read_text()
        self.assertIn("status: published", text)
        self.assertIn("url: \"https://x.com/a/status/1\"", text)
        run(self.tmp, "post-published", "--number", "1", "--file", "2026-12-06_x.md", "--url", "u", ok=False)
        run(self.tmp, "add-update", "--number", "1", "--en", "Fixed a thing.", "--ru", "Исправил.", "--date", "2026-12-07")
        run(self.tmp, "build")
        self.assertIn("Updated 2026-12-07:", self.read("blog/0001-blog-features-demo/index.html"))
        self.assertIn("Обновлено 2026-12-07:", self.read("ru/blog/0001-blog-features-demo/index.html"))
        out = run(self.tmp, "status").stdout
        self.assertIn("0002", out)
        self.assertIn("published 2026-12-05", out)

    def test_only_published_listed(self):
        run(self.tmp, "start", "second-article", "--target", "2027-01-15", "--title", "Second")
        run(self.tmp, "publish", "--number", "1", "--date", "2026-12-05")
        listing = self.read("blog/index.html")
        self.assertIn("0001-blog-features-demo", listing)
        self.assertNotIn("0002", listing)
        self.assertNotIn("0002", self.read("sitemap.xml"))

    def test_missing_image_fails_published_build(self):
        run(self.tmp, "publish", "--number", "1", "--date", "2026-12-05")
        (self.demo / "figure.png").unlink()
        p = run(self.tmp, "build", ok=False)
        self.assertIn("figure.png", p.stderr)


if __name__ == "__main__":
    unittest.main(verbosity=2)
