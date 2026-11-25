#!/usr/bin/env python3
"""Self-test of tools/blog.py. Works on a temporary copy of the repository, so
the tree is never changed. The sample article comes from tools/blog_fixture/,
not from blog/. Run: python3 tools/blog_selftest.py"""
import pathlib
import re
import shutil
import subprocess
import sys
import tempfile
import unittest

REPO = pathlib.Path(__file__).resolve().parent.parent
FIXTURE = pathlib.Path(__file__).resolve().parent / "blog_fixture"
SITEMAP_SHELL = (
    '<?xml version="1.0" encoding="UTF-8"?>\n'
    '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" '
    'xmlns:xhtml="http://www.w3.org/1999/xhtml">\n</urlset>\n'
)


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
        for name in ("tools", "assets", "sitemap.xml", "favicon.svg", "card.png"):
            src = REPO / name
            if not src.exists():
                continue
            if src.is_dir():
                shutil.copytree(src, self.tmp / name, ignore=shutil.ignore_patterns("__pycache__"))
            else:
                shutil.copy2(src, self.tmp / name)
        if not (self.tmp / "sitemap.xml").exists():
            (self.tmp / "sitemap.xml").write_text(SITEMAP_SHELL, encoding="utf-8")
        self.had_events = "https://donmutti.com/events/</loc>" in (self.tmp / "sitemap.xml").read_text(encoding="utf-8")
        demo_src = FIXTURE / "0001_blog-features-demo"
        if not demo_src.is_dir():
            raise AssertionError(f"missing fixture {demo_src}")
        self.demo = self.tmp / "blog" / "0001_blog-features-demo"
        shutil.copytree(demo_src, self.demo)
        # Placeholder audio lives only in the temporary copy, never in the repository.
        (self.demo / "v1_ru.ogg").write_bytes(b"fixture-ru")
        (self.demo / "v1_en.ogg").write_bytes(b"fixture-en")
        (self.demo / "quack.ogg").write_bytes(b"fixture-quack")

    def tearDown(self):
        shutil.rmtree(self.tmp, ignore_errors=True)

    def read(self, rel):
        return (self.tmp / rel).read_text(encoding="utf-8")

    def test_draft_is_not_listed_and_previews(self):
        run(self.tmp, "build", "--number", "1")
        listing = self.read("blog/index.html")
        self.assertIn("The first article is on its way.", listing)
        self.assertIn('href="/"', listing)
        self.assertIn("Home", listing)
        self.assertIn('class="topnav-blog" href="/blog/" aria-current="page">Blog</a>', listing)
        self.assertIn("Первая статья уже в работе.", self.read("ru/blog/index.html"))
        self.assertIn("На главную", self.read("ru/blog/index.html"))
        self.assertNotIn("0001-blog-features-demo", listing)
        self.assertFalse((self.tmp / "blog" / "tags").exists())
        sm = self.read("sitemap.xml")
        self.assertIn("<loc>https://donmutti.com/blog/</loc>", sm)
        self.assertIn("<loc>https://donmutti.com/ru/blog/</loc>", sm)
        self.assertNotIn("0001-blog-features-demo", sm)
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
            self.assertIn('draggable="false"', page)
            self.assertIn('class="hl"', page)
            self.assertTrue((self.tmp / f"{lang_prefix}blog/0001-blog-features-demo/cover.png").exists())
        for rel in ("blog/index.html", "ru/blog/index.html", "blog/tags/demo/index.html", "ru/blog/tags/blog/index.html"):
            self.assertIn("0001-blog-features-demo", self.read(rel))
        self.assertNotIn("The first article is on its way.", self.read("blog/index.html"))
        sm = self.read("sitemap.xml")
        self.assertIn("https://donmutti.com/blog/0001-blog-features-demo/", sm)
        self.assertIn("https://donmutti.com/ru/blog/tags/demo/", sm)
        if self.had_events:
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

    def test_audio_tabs_follow_page_language(self):
        run(self.tmp, "build", "--number", "1")
        en = self.read(".blog-preview/blog/0001-blog-features-demo/index.html")
        ru = self.read(".blog-preview/ru/blog/0001-blog-features-demo/index.html")
        self.assertEqual(en.count('class="audio audio-tabs"'), 2)
        self.assertEqual(ru.count('class="audio audio-tabs"'), 2)
        self.assertIn('src="/blog/0001-blog-features-demo/v1_ru.ogg"', en)
        self.assertIn('src="/blog/0001-blog-features-demo/v1_en.ogg"', en)
        self.assertIn('src="/ru/blog/0001-blog-features-demo/v1_ru.ogg"', ru)
        self.assertIn('src="/ru/blog/0001-blog-features-demo/v1_en.ogg"', ru)
        self.assertIn('src="https://example.com/ru.ogg"', en)
        self.assertIn('src="https://example.com/en.ogg"', ru)
        self.assertIn("<figcaption>A short caption under the player.</figcaption>", en)
        self.assertIn("<figcaption>Короткая подпись под плеером.</figcaption>", ru)
        self.assertIn('aria-label="Audio language"', en)
        self.assertIn('aria-label="Язык записи"', ru)
        en_first = en.split('class="audio audio-tabs"', 1)[1]
        ru_first = ru.split('class="audio audio-tabs"', 1)[1]
        en_tab = re.search(r'<button type="button" role="tab"[^>]*>', en_first).group(0)
        ru_tab = re.search(r'<button type="button" role="tab"[^>]*>', ru_first).group(0)
        self.assertIn('data-lang="en"', en_tab)
        self.assertIn('aria-selected="true"', en_tab)
        self.assertIn('data-lang="ru"', ru_tab)
        self.assertIn('aria-selected="true"', ru_tab)
        self.assertIn('role="tablist"', en)
        self.assertIn('role="tabpanel"', en)
        self.assertNotIn('class="language-audio"', en)
        for lang_prefix in ("", "ru/"):
            built = self.tmp / ".blog-preview" / f"{lang_prefix}blog/0001-blog-features-demo"
            self.assertEqual((built / "v1_ru.ogg").read_bytes(), (self.demo / "v1_ru.ogg").read_bytes())
            self.assertEqual((built / "v1_en.ogg").read_bytes(), (self.demo / "v1_en.ogg").read_bytes())
            self.assertFalse((built / "leftover.ogg").exists())

    def test_audio_single_source_renders_without_tabs(self):
        run(self.tmp, "build", "--number", "1")
        for lang_prefix, caption in (("", "A recording without a language."), ("ru/", "Запись без языка.")):
            page = self.read(f".blog-preview/{lang_prefix}blog/0001-blog-features-demo/index.html")
            self.assertEqual(page.count('class="audio audio-single"'), 1)
            single = page.split('class="audio audio-single"', 1)[1].split("</figure>", 1)[0]
            self.assertIn(f'src="/{lang_prefix}blog/0001-blog-features-demo/quack.ogg"', single)
            self.assertNotIn('role="tab"', single)
            self.assertIn(f"<figcaption>{caption}</figcaption>", single)
            built = self.tmp / ".blog-preview" / f"{lang_prefix}blog/0001-blog-features-demo"
            self.assertEqual((built / "quack.ogg").read_bytes(), b"fixture-quack")

    def test_audio_src_with_language_source_fails_published_build(self):
        run(self.tmp, "publish", "--number", "1", "--date", "2026-12-05")
        en = self.demo / "en.md"
        en.write_text(en.read_text(encoding="utf-8") + "\n\n```audio\nsrc: quack.ogg\nru: v1_ru.ogg\n```\n", encoding="utf-8")
        p = run(self.tmp, "build", ok=False)
        self.assertIn("src together with ru or en", p.stderr)

    def test_tags_keep_case_and_use_lower_case_urls(self):
        meta = self.demo / "meta.yml"
        meta.write_text(meta.read_text(encoding="utf-8").replace("tags: [demo, blog]", "tags: [AI, Voice]"), encoding="utf-8")
        run(self.tmp, "build", "--number", "1")
        draft = self.read(".blog-preview/blog/0001-blog-features-demo/index.html")
        self.assertIn('href="/blog/tags/ai/">AI</a>', draft)
        run(self.tmp, "publish", "--number", "1", "--date", "2026-12-05")
        en = self.read("blog/0001-blog-features-demo/index.html")
        ru = self.read("ru/blog/0001-blog-features-demo/index.html")
        self.assertIn('<a class="tag" href="/blog/tags/ai/">AI</a>', en)
        self.assertIn('<a class="tag" href="/ru/blog/tags/voice/">Voice</a>', ru)
        self.assertIn("Tag: AI", self.read("blog/tags/ai/index.html"))
        self.assertTrue((self.tmp / "ru/blog/tags/voice/index.html").exists())
        sitemap = self.read("sitemap.xml")
        self.assertIn("https://donmutti.com/blog/tags/ai/</loc>", sitemap)
        self.assertNotIn("/blog/tags/AI/", sitemap)

    def test_tags_differing_only_in_case_fail(self):
        meta = self.demo / "meta.yml"
        meta.write_text(meta.read_text(encoding="utf-8").replace("tags: [demo, blog]", "tags: [AI, ai]"), encoding="utf-8")
        p = run(self.tmp, "build", "--number", "1", ok=False)
        self.assertIn("repeats another tag", p.stderr)

    def test_draft_header_shows_target_date(self):
        run(self.tmp, "build", "--number", "1")
        en = self.read(".blog-preview/blog/0001-blog-features-demo/index.html")
        self.assertIn("<time>2026-12-xx</time>", en)
        self.assertNotIn("draft-badge", en)
        meta = self.demo / "meta.yml"
        meta.write_text(meta.read_text(encoding="utf-8").replace("target: 2026-12-xx", "target: 2026-11-25"), encoding="utf-8")
        run(self.tmp, "build", "--number", "1")
        en = self.read(".blog-preview/blog/0001-blog-features-demo/index.html")
        ru = self.read(".blog-preview/ru/blog/0001-blog-features-demo/index.html")
        self.assertIn('<time datetime="2026-11-25">25 November 2026</time>', en)
        self.assertIn('<time datetime="2026-11-25">', ru)
        self.assertIn("noindex, nofollow", en)
        self.assertNotIn("0001-blog-features-demo", self.read("blog/index.html"))

    def test_audio_missing_source_fails_published_build(self):
        run(self.tmp, "publish", "--number", "1", "--date", "2026-12-05")
        en = self.demo / "en.md"
        en.write_text(en.read_text(encoding="utf-8") + "\n\n```audio\nru: only-ru.ogg\n```\n", encoding="utf-8")
        p = run(self.tmp, "build", ok=False)
        self.assertIn("missing an en source", p.stderr)

    def test_audio_files_are_copied_on_publish_and_unreferenced_are_not(self):
        (self.demo / "leftover.ogg").write_bytes(b"unused")
        run(self.tmp, "publish", "--number", "1", "--date", "2026-12-05")
        for lang_prefix in ("", "ru/"):
            built = self.tmp / f"{lang_prefix}blog/0001-blog-features-demo"
            self.assertEqual((built / "v1_ru.ogg").read_bytes(), (self.demo / "v1_ru.ogg").read_bytes())
            self.assertEqual((built / "v1_en.ogg").read_bytes(), (self.demo / "v1_en.ogg").read_bytes())
            self.assertFalse((built / "leftover.ogg").exists())

    def test_missing_audio_fails_published_build(self):
        run(self.tmp, "publish", "--number", "1", "--date", "2026-12-05")
        (self.demo / "v1_ru.ogg").unlink()
        p = run(self.tmp, "build", ok=False)
        self.assertIn("v1_ru.ogg", p.stderr)
        self.assertIn("is not in", p.stderr)

    def test_media_requires_out_or_number(self):
        p = run(self.tmp, "build", "--media", str(self.tmp / "media"), ok=False)
        self.assertIn("--media requires --out", p.stderr)

    def test_media_must_be_an_absolute_directory(self):
        p = run(self.tmp, "build", "--number", "1", "--out", str(self.tmp / "out"), "--media", "media", ok=False)
        self.assertIn("absolute path", p.stderr)
        p = run(self.tmp, "build", "--number", "1", "--out", str(self.tmp / "out"), "--media", str(self.tmp / "missing-media"), ok=False)
        self.assertIn("is not a directory", p.stderr)

    def test_media_supplies_audio_missing_from_source_into_out_only(self):
        (self.demo / "v1_ru.ogg").unlink()
        (self.demo / "v1_en.ogg").unlink()
        media = self.tmp / "media"
        media.mkdir()
        (media / "v1_ru.ogg").write_bytes(b"from-media-ru")
        (media / "v1_en.ogg").write_bytes(b"from-media-en")
        out = self.tmp / "out"
        run(self.tmp, "build", "--number", "1", "--out", str(out), "--media", str(media))
        for lang_prefix in ("", "ru/"):
            built = out / f"{lang_prefix}blog/0001-blog-features-demo"
            self.assertEqual((built / "v1_ru.ogg").read_bytes(), b"from-media-ru")
            self.assertEqual((built / "v1_en.ogg").read_bytes(), b"from-media-en")
        self.assertFalse((self.demo / "v1_ru.ogg").exists())
        self.assertFalse((self.demo / "v1_en.ogg").exists())
        self.assertFalse((self.tmp / "blog" / "0001-blog-features-demo" / "v1_ru.ogg").exists())

    def test_media_prefers_source_folder_over_media_dir(self):
        media = self.tmp / "media"
        media.mkdir()
        (media / "v1_ru.ogg").write_bytes(b"from-media-ru")
        (media / "v1_en.ogg").write_bytes(b"from-media-en")
        out = self.tmp / "out"
        run(self.tmp, "build", "--number", "1", "--out", str(out), "--media", str(media))
        built = out / "blog/0001-blog-features-demo"
        self.assertEqual((built / "v1_ru.ogg").read_bytes(), b"fixture-ru")
        self.assertEqual((built / "v1_en.ogg").read_bytes(), b"fixture-en")

    def test_media_with_number_writes_only_to_blog_preview(self):
        (self.demo / "v1_ru.ogg").unlink()
        (self.demo / "v1_en.ogg").unlink()
        media = self.tmp / "media"
        media.mkdir()
        (media / "v1_ru.ogg").write_bytes(b"preview-ru")
        (media / "v1_en.ogg").write_bytes(b"preview-en")
        run(self.tmp, "build", "--number", "1", "--media", str(media))
        built = self.tmp / ".blog-preview/blog/0001-blog-features-demo"
        self.assertEqual((built / "v1_ru.ogg").read_bytes(), b"preview-ru")
        self.assertEqual((built / "v1_en.ogg").read_bytes(), b"preview-en")
        self.assertFalse((self.demo / "v1_ru.ogg").exists())
        self.assertFalse((self.tmp / "blog/0001-blog-features-demo").exists())

    def test_media_does_not_copy_into_repo_when_building_published_without_out(self):
        run(self.tmp, "publish", "--number", "1", "--date", "2026-12-05")
        (self.demo / "v1_ru.ogg").unlink()
        (self.demo / "v1_en.ogg").unlink()
        media = self.tmp / "media"
        media.mkdir()
        (media / "v1_ru.ogg").write_bytes(b"media-ru")
        (media / "v1_en.ogg").write_bytes(b"media-en")
        p = run(self.tmp, "build", "--number", "1", "--media", str(media), ok=False)
        self.assertIn("v1_ru.ogg", p.stderr)
        built = self.tmp / "blog/0001-blog-features-demo"
        self.assertFalse((built / "v1_ru.ogg").exists() and (built / "v1_ru.ogg").read_bytes() == b"media-ru")
        self.assertFalse((self.demo / "v1_ru.ogg").exists())

    def test_published_missing_audio_succeeds_with_media_and_out(self):
        run(self.tmp, "publish", "--number", "1", "--date", "2026-12-05")
        (self.demo / "v1_ru.ogg").unlink()
        (self.demo / "v1_en.ogg").unlink()
        media = self.tmp / "media"
        media.mkdir()
        (media / "v1_ru.ogg").write_bytes(b"out-ru")
        (media / "v1_en.ogg").write_bytes(b"out-en")
        out = self.tmp / "out"
        run(self.tmp, "build", "--out", str(out), "--media", str(media))
        built = out / "blog/0001-blog-features-demo"
        self.assertEqual((built / "v1_ru.ogg").read_bytes(), b"out-ru")
        self.assertEqual((built / "v1_en.ogg").read_bytes(), b"out-en")
        self.assertFalse((self.demo / "v1_ru.ogg").exists())


if __name__ == "__main__":
    unittest.main(verbosity=2)
