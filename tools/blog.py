#!/usr/bin/env python3
"""The donmutti.com blog tool.

Sources live in blog/<nnnn>_<slug>/ (underscore). Built pages are generated
into blog/<nnnn>-<slug>/ and ru/blog/<nnnn>-<slug>/ (hyphen), together with
the lists, the tag pages and the blog entries of sitemap.xml.

    python3 tools/blog.py start <slug> --target 2026-12-xx --title "..." --title-ru "..."
    python3 tools/blog.py build [--number N] [--out DIR]
    python3 tools/blog.py publish --number N [--date YYYY-MM-DD]
    python3 tools/blog.py new-draft --number N --platform x|linkedin [--lang en|ru] [--target DATE]
    python3 tools/blog.py post-published --number N --file NAME --url URL [--date YYYY-MM-DD]
    python3 tools/blog.py add-update --number N --en "..." --ru "..." [--date YYYY-MM-DD]
    python3 tools/blog.py status [--json]

Needs the packages in tools/requirements.txt (a Markdown library and Pygments
for build-time syntax highlighting). Everything else is the standard library.
"""
from __future__ import annotations

import argparse
import datetime
import html
import json
import os
import pathlib
import re
import shutil
import struct
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
TEMPLATES = pathlib.Path(__file__).resolve().parent / "blog_templates"
SITE = "https://donmutti.com"
PREVIEW = ".blog-preview"
LANGS = ("en", "ru")
PLATFORMS = ("x", "linkedin")
IMAGE_EXT = (".png", ".jpg", ".jpeg", ".gif", ".webp", ".svg", ".avif")
SLUG_RE = re.compile(r"^[a-z0-9]+(-[a-z0-9]+)*$")
SRC_DIR_RE = re.compile(r"^(\d{4})_([a-z0-9]+(?:-[a-z0-9]+)*)$")
MASK_RE = re.compile(r"^\d{4}-(\d{2}|xx)-(\d{2}|xx)$")
DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")

RU_MONTHS = ("января", "февраля", "марта", "апреля", "мая", "июня", "июля",
             "августа", "сентября", "октября", "ноября", "декабря")
EN_MONTHS = ("January", "February", "March", "April", "May", "June", "July",
             "August", "September", "October", "November", "December")

S = {
    "en": {
        "lang_label": "Language", "back_home": "Back", "back_list": "Blog", "blog": "Blog",
        "list_description": "Articles by Dmitrii Petukhov.", "empty": "No articles yet.",
        "tag": "Tag", "updated": "Updated", "see_also": "See also", "discussion": "Discussion",
        "thread": "Thread", "copy": "Copy", "copied": "Copied", "draft": "Draft",
        "target": "Target", "anchor": "Link to this section", "table": "Table",
        "footnote_back": "Jump back to footnote %d in the text", "author": "Dmitrii Petukhov",
        "locale": "en_US", "home": "/", "prefix": "",
    },
    "ru": {
        "lang_label": "Язык", "back_home": "Назад", "back_list": "Блог", "blog": "Блог",
        "list_description": "Статьи Дмитрия Петухова.", "empty": "Статей пока нет.",
        "tag": "Тег", "updated": "Обновлено", "see_also": "Читайте также", "discussion": "Обсуждение",
        "thread": "Тред", "copy": "Копировать", "copied": "Скопировано", "draft": "Черновик",
        "target": "Цель", "anchor": "Ссылка на этот раздел", "table": "Таблица",
        "footnote_back": "Вернуться к сноске %d в тексте", "author": "Дмитрий Петухов",
        "locale": "ru_RU", "home": "/ru/", "prefix": "/ru",
    },
}


class BlogError(Exception):
    pass


# ----------------------------------------------------------------------------
# A small YAML subset: maps, lists, flow lists and scalars. That is all the
# blog files use, so no YAML library is needed.
# ----------------------------------------------------------------------------

def _yaml_scalar(text: str):
    s = text.strip()
    if s == "":
        return None
    if s[0] == '"':
        return json.loads(s)
    if s[0] == "'" and s.endswith("'") and len(s) > 1:
        return s[1:-1].replace("''", "'")
    if s[0] == "[":
        inner = s[1:-1].strip()
        if not inner:
            return []
        items = re.findall(r'"(?:[^"\\]|\\.)*"|\'[^\']*\'|[^,]+', inner)
        return [_yaml_scalar(i) for i in items]
    s = re.split(r"\s+#", s, maxsplit=1)[0].strip()
    if s in ("null", "~"):
        return None
    if s == "true":
        return True
    if s == "false":
        return False
    if re.fullmatch(r"-?\d+", s):
        return int(s)
    return s


def _yaml_block(lines, i, indent):
    if i >= len(lines):
        return None, i
    if lines[i][1] == "-" or lines[i][1].startswith("- "):
        out = []
        while i < len(lines) and lines[i][0] == indent and (lines[i][1] == "-" or lines[i][1].startswith("- ")):
            text = lines[i][1]
            rest = text[1:].strip()
            if rest == "":
                if i + 1 < len(lines) and lines[i + 1][0] > indent:
                    val, i = _yaml_block(lines, i + 1, lines[i + 1][0])
                else:
                    val, i = None, i + 1
                out.append(val)
            elif re.match(r"^[A-Za-z_][\w-]*:(\s|$)", rest):
                offset = len(text) - len(text[1:].lstrip())
                lines[i] = (indent + offset, rest)
                val, i = _yaml_block(lines, i, indent + offset)
                out.append(val)
            else:
                out.append(_yaml_scalar(rest))
                i += 1
        return out, i
    out = {}
    while i < len(lines) and lines[i][0] == indent and not lines[i][1].startswith("- "):
        key, sep, rest = lines[i][1].partition(":")
        if not sep:
            raise BlogError(f"cannot parse line: {lines[i][1]!r}")
        key = key.strip()
        if rest.strip() != "":
            out[key] = _yaml_scalar(rest)
            i += 1
        elif i + 1 < len(lines) and (lines[i + 1][0] > indent or (lines[i + 1][0] == indent and lines[i + 1][1].startswith("- "))):
            out[key], i = _yaml_block(lines, i + 1, lines[i + 1][0])
        else:
            out[key] = None
            i += 1
    return out, i


def parse_yaml(text: str) -> dict:
    lines = []
    for raw in text.splitlines():
        if not raw.strip() or raw.lstrip().startswith("#"):
            continue
        lines.append((len(raw) - len(raw.lstrip(" ")), raw.strip()))
    if not lines:
        return {}
    val, _ = _yaml_block(lines, 0, lines[0][0])
    return val if isinstance(val, dict) else {}


def yq(value) -> str:
    """Format one scalar for a YAML file."""
    if value is None:
        return ""
    if isinstance(value, bool):
        return "true" if value else "false"
    if isinstance(value, int):
        return str(value)
    s = str(value)
    plain = re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9 ._/-]*", s) and not re.fullmatch(r"-?\d+|true|false|null", s) and not s.endswith(" ")
    return s if plain else json.dumps(s, ensure_ascii=False)


def set_scalar(text: str, key: str, value) -> str:
    line = f"{key}: {yq(value)}".rstrip()
    pat = re.compile(rf"^{re.escape(key)}:.*$", re.M)
    if pat.search(text):
        return pat.sub(lambda _m: line, text, count=1)
    return text.rstrip("\n") + "\n" + line + "\n"


def split_front(text: str):
    m = re.match(r"^---\n(.*?)\n---\n?(.*)$", text, re.S)
    if not m:
        return {}, text, None
    return parse_yaml(m.group(1)), m.group(2), m.group(1)


def read_md(path: pathlib.Path):
    text = path.read_text(encoding="utf-8")
    fm, body, _ = split_front(text)
    return fm, body


def write_front_key(path: pathlib.Path, key: str, value) -> None:
    text = path.read_text(encoding="utf-8")
    m = re.match(r"^---\n(.*?)\n---\n?(.*)$", text, re.S)
    if not m:
        raise BlogError(f"{path} has no frontmatter")
    head = set_scalar(m.group(1) + "\n", key, value).rstrip("\n")
    path.write_text(f"---\n{head}\n---\n{m.group(2)}", encoding="utf-8")


# ----------------------------------------------------------------------------
# Dates and strings
# ----------------------------------------------------------------------------

def today() -> str:
    return datetime.date.today().isoformat()


def fmt_date(iso: str, lang: str) -> str:
    try:
        d = datetime.date.fromisoformat(str(iso))
    except ValueError:
        return str(iso)
    month = (RU_MONTHS if lang == "ru" else EN_MONTHS)[d.month - 1]
    return f"{d.day} {month} {d.year}"


def plural_comments(n: int, lang: str) -> str:
    if lang == "ru":
        if n % 10 == 1 and n % 100 != 11:
            word = "комментарий"
        elif 2 <= n % 10 <= 4 and not 12 <= n % 100 <= 14:
            word = "комментария"
        else:
            word = "комментариев"
        return f"{n} {word}"
    return f"{n} comment" + ("" if n == 1 else "s")


def esc(value) -> str:
    return html.escape(str(value if value is not None else ""), quote=True)


def normalize_mask(raw: str) -> str:
    s = raw.strip().lower().replace("?", "x")
    if re.fullmatch(r"\d{4}", s):
        s += "-xx-xx"
    elif re.fullmatch(r"\d{4}-(\d{2}|xx)", s):
        s += "-xx"
    if not MASK_RE.match(s):
        raise BlogError(f"bad date {raw!r}: use YYYY-MM-DD, with xx for unknown parts, for example 2026-12-xx")
    return s


def render_template(name: str, **kw) -> str:
    text = (TEMPLATES / name).read_text(encoding="utf-8")

    def sub(m):
        key = m.group(1)
        if key not in kw:
            raise BlogError(f"template {name}: no value for {key}")
        return str(kw[key])

    return re.sub(r"\{\{(\w+)\}\}", sub, text)


# ----------------------------------------------------------------------------
# Articles
# ----------------------------------------------------------------------------

class Article:
    def __init__(self, path: pathlib.Path):
        m = SRC_DIR_RE.match(path.name)
        if not m:
            raise BlogError(f"{path.name} is not a source folder name")
        self.dir = path
        self.number = int(m.group(1))
        self.slug = m.group(2)
        meta_path = path / "meta.yml"
        if not meta_path.exists():
            raise BlogError(f"{path.name}: meta.yml is missing")
        self.meta = parse_yaml(meta_path.read_text(encoding="utf-8"))
        self.status = self.meta.get("status")
        self.target = self.meta.get("target")
        self.published = self.meta.get("published")
        self.tags = self.meta.get("tags") or []
        self.cover = self.meta.get("cover")
        self.updates = self.meta.get("updates") or []
        self.text = {}
        for lang in LANGS:
            p = path / f"{lang}.md"
            if p.exists():
                fm, body = read_md(p)
                self.text[lang] = {"title": str(fm.get("title") or ""), "description": str(fm.get("description") or ""), "body": body}
            else:
                self.text[lang] = None
        self.drafts = self._drafts()

    @property
    def key(self) -> str:
        return f"{self.number:04d}-{self.slug}"

    @property
    def is_published(self) -> bool:
        return self.status == "published"

    def url(self, lang: str) -> str:
        return f"{S[lang]['prefix']}/blog/{self.key}/"

    def title(self, lang: str) -> str:
        t = self.text[lang]["title"] if self.text[lang] else ""
        return t or "(untitled)"

    def _drafts(self):
        out = []
        for p in sorted(self.dir.glob("*_*.md")):
            m = re.match(r"^(\d{4}-(?:\d{2}|xx)-(?:\d{2}|xx))_([a-z]+)\.md$", p.name)
            if not m:
                continue
            fm, body = read_md(p)
            out.append({"file": p.name, "date": m.group(1), "platform": fm.get("platform") or m.group(2),
                        "lang": fm.get("lang"), "status": fm.get("status"), "published": fm.get("published"),
                        "url": fm.get("url")})
        return out

    def json_file(self, name: str):
        p = self.dir / name
        if not p.exists():
            return None
        try:
            return json.loads(p.read_text(encoding="utf-8"))
        except json.JSONDecodeError as e:
            raise BlogError(f"{self.dir.name}/{name}: {e}")

    def images(self):
        return sorted(p for p in self.dir.iterdir() if p.is_file() and p.suffix.lower() in IMAGE_EXT)

    def problems(self) -> list[str]:
        out = []
        if self.status not in ("draft", "published"):
            out.append("status must be draft or published")
        if self.meta.get("number") != self.number:
            out.append(f"meta number {self.meta.get('number')!r} does not match folder number {self.number}")
        if self.meta.get("slug") != self.slug:
            out.append(f"meta slug {self.meta.get('slug')!r} does not match folder slug {self.slug!r}")
        if self.is_published and not (self.published and DATE_RE.match(str(self.published))):
            out.append("published needs an exact date YYYY-MM-DD")
        for t in self.tags:
            if not SLUG_RE.match(str(t)):
                out.append(f"tag {t!r} is not kebab-case")
        if self.cover and not (self.dir / str(self.cover)).exists():
            out.append(f"cover {self.cover} does not exist")
        for lang in LANGS:
            t = self.text[lang]
            if t is None:
                out.append(f"{lang}.md is missing")
            elif self.is_published:
                if not t["title"].strip():
                    out.append(f"{lang}.md has no title")
                if not t["description"].strip():
                    out.append(f"{lang}.md has no description")
        for u in self.updates:
            if not isinstance(u, dict) or not u.get("date"):
                out.append("each update needs date, en and ru")
        return out


def blog_dirs() -> list[pathlib.Path]:
    base = ROOT / "blog"
    if not base.exists():
        return []
    return sorted(p for p in base.iterdir() if p.is_dir() and SRC_DIR_RE.match(p.name))


def load_articles() -> list[Article]:
    return [Article(p) for p in blog_dirs()]


def find_article(number: int) -> Article:
    for a in load_articles():
        if a.number == number:
            return a
    raise BlogError(f"no article with number {number}")


def next_number() -> int:
    nums = [0]
    for base in (ROOT / "blog", ROOT / "ru" / "blog"):
        if base.exists():
            for p in base.iterdir():
                m = re.match(r"^(\d{4})[_-]", p.name)
                if m and p.is_dir():
                    nums.append(int(m.group(1)))
    return max(nums) + 1


# ----------------------------------------------------------------------------
# Markdown rendering
# ----------------------------------------------------------------------------

CODE_ALIASES = {
    "py": "python", "python3": "python", "js": "javascript", "mjs": "javascript", "node": "javascript",
    "ts": "typescript", "sh": "bash", "shell": "bash", "zsh": "bash", "yml": "yaml", "md": "markdown",
    "rb": "ruby", "c++": "cpp", "c#": "csharp", "cs": "csharp", "golang": "go", "rs": "rust",
    "jsonc": "json", "htm": "html", "txt": "text", "plain": "text", "plaintext": "text", "ps1": "powershell",
    "kt": "kotlin",
}
CODE_NAMES = {
    "python": "Python", "javascript": "JavaScript", "typescript": "TypeScript", "bash": "Bash",
    "yaml": "YAML", "json": "JSON", "html": "HTML", "css": "CSS", "sql": "SQL", "go": "Go",
    "rust": "Rust", "ruby": "Ruby", "cpp": "C++", "csharp": "C#", "c": "C", "java": "Java",
    "kotlin": "Kotlin", "swift": "Swift", "markdown": "Markdown", "diff": "Diff", "toml": "TOML",
    "text": "Text", "php": "PHP", "dockerfile": "Dockerfile", "ini": "INI", "xml": "XML",
    "powershell": "PowerShell", "jsx": "JSX", "tsx": "TSX",
}


def canon_lang(tag: str) -> str:
    t = tag.strip().lower()
    return CODE_ALIASES.get(t, t)


def lang_label(canon: str, tag: str) -> str:
    return CODE_NAMES.get(canon, tag)


def highlight(code: str, canon: str) -> str:
    from pygments import highlight as pyg_highlight
    from pygments.formatters import HtmlFormatter
    from pygments.lexers import get_lexer_by_name
    from pygments.util import ClassNotFound
    if not canon or canon == "text":
        return esc(code)
    try:
        lexer = get_lexer_by_name(canon)
    except ClassNotFound:
        return esc(code)
    out = pyg_highlight(code, lexer, HtmlFormatter(nowrap=True))
    return out.rstrip("\n")


def unicode_slugify(value: str, separator: str) -> str:
    value = re.sub(r"[^\w\s-]", "", value.strip().lower())
    return re.sub(r"[\s_-]+", separator, value).strip(separator) or "section"


def _strike_extension():
    import markdown
    from markdown.inlinepatterns import InlineProcessor
    import xml.etree.ElementTree as etree

    class Strike(InlineProcessor):
        def handleMatch(self, m, data):
            el = etree.Element("del")
            el.text = m.group(1)
            return el, m.start(0), m.end(0)

    class StrikeExt(markdown.Extension):
        def extendMarkdown(self, md):
            md.inlinePatterns.register(Strike(r"~~(?=\S)(.+?)(?<=\S)~~"), "strike", 60)

    return StrikeExt()


def image_size(path: pathlib.Path):
    try:
        data = path.read_bytes()
    except OSError:
        return None
    if data[:8] == b"\x89PNG\r\n\x1a\n":
        return struct.unpack(">II", data[16:24])
    if data[:6] in (b"GIF87a", b"GIF89a"):
        return struct.unpack("<HH", data[6:10])
    if data[:2] == b"\xff\xd8":
        i = 2
        while i + 9 < len(data):
            if data[i] != 0xFF:
                i += 1
                continue
            marker = data[i + 1]
            if marker in (0xD8, 0x01) or 0xD0 <= marker <= 0xD7:
                i += 2
                continue
            length = struct.unpack(">H", data[i + 2:i + 4])[0]
            if 0xC0 <= marker <= 0xCF and marker not in (0xC4, 0xC8, 0xCC):
                h, w = struct.unpack(">HH", data[i + 5:i + 9])
                return w, h
            i += 2 + length
    return None


class Renderer:
    """Turns one article body into HTML with the article components."""

    def __init__(self, article: Article, lang: str):
        self.article = article
        self.lang = lang
        self.errors: list[str] = []

    def render(self, body: str) -> str:
        import markdown
        s = S[self.lang]
        md = markdown.Markdown(
            extensions=["tables", "fenced_code", "footnotes", "sane_lists", "toc", _strike_extension()],
            extension_configs={
                "toc": {"permalink": "#", "permalink_class": "headerlink", "permalink_title": s["anchor"],
                        "toc_depth": "2-4", "slugify": unicode_slugify},
                "footnotes": {"BACKLINK_TITLE": s["footnote_back"]},
            },
        )
        out = md.convert(body)
        out = self._figures(out)
        out = self._images(out)
        out = self._links(out)
        out = self._tables(out)
        out = self._code(out)
        return out

    # figures and images

    def _figures(self, out: str) -> str:
        def fig(m):
            tag = m.group(1)
            attrs = dict(re.findall(r'([\w-]+)="([^"]*)"', tag))
            cap = attrs.pop("title", "")
            tag = re.sub(r'\s+title="[^"]*"', "", tag)
            inner = tag + (f"\n<figcaption>{cap}</figcaption>\n" if cap else "")
            return f"<figure>{inner}</figure>" if cap else f"<figure>{tag}</figure>"
        return re.sub(r"<p>\s*(<img\b[^>]*>)\s*</p>", fig, out)

    def _images(self, out: str) -> str:
        def img(m):
            tag = m.group(0)
            attrs = dict(re.findall(r'([\w-]+)="([^"]*)"', tag))
            src = html.unescape(attrs.get("src", ""))
            new = tag
            if src and not re.match(r"^([a-z][a-z0-9+.-]*:|/|#|//)", src, re.I):
                name = pathlib.PurePosixPath(src).name
                file = self.article.dir / src
                if not file.is_file():
                    self.errors.append(f"image {src} is not in {self.article.dir.name}/")
                else:
                    size = image_size(file)
                    if size and "width" not in attrs:
                        new = new.replace("<img", f'<img width="{size[0]}" height="{size[1]}"', 1)
                new = new.replace(f'src="{attrs["src"]}"', f'src="{esc(self.article.url(self.lang) + src)}"', 1)
            if "loading=" not in new:
                new = new.replace("<img", '<img loading="lazy" decoding="async"', 1)
            return new
        return re.sub(r"<img\b[^>]*>", img, out)

    # links

    def _links(self, out: str) -> str:
        prefix = S[self.lang]["prefix"]

        def link(m):
            tag = m.group(0)
            href_m = re.search(r'href="([^"]*)"', tag)
            if not href_m:
                return tag
            href = html.unescape(href_m.group(1))
            ext = re.match(r"^https?://([^/:?#]+)", href, re.I)
            if ext:
                host = ext.group(1).lower()
                if host in ("donmutti.com", "www.donmutti.com"):
                    return tag
                if "target=" not in tag:
                    tag = tag[:-1] + ' target="_blank" rel="noopener">'
                return tag
            art = re.match(r"^(?:\.\./|\./)?(\d{4})[-_]([a-z0-9]+(?:-[a-z0-9]+)*)/?(#.*)?$", href)
            if art:
                new = f"{prefix}/blog/{art.group(1)}-{art.group(2)}/{art.group(3) or ''}"
                tag = tag.replace(href_m.group(0), f'href="{esc(new)}"', 1)
            return tag
        return re.sub(r"<a\s[^>]*>", link, out)

    # tables

    def _tables(self, out: str) -> str:
        label = esc(S[self.lang]["table"])
        out = re.sub(r"<table>", f'<div class="table-wrap" tabindex="0" role="region" aria-label="{label}">\n<table>', out)
        return out.replace("</table>", "</table>\n</div>")

    # code and code tabs

    def _code(self, out: str) -> str:
        s = S[self.lang]
        pat = re.compile(r'<pre><code(?: class="language-([^"]*)")?>(.*?)</code></pre>', re.S)
        matches = list(pat.finditer(out))
        if not matches:
            return out
        blocks = []
        for m in matches:
            tag = m.group(1) or ""
            canon = canon_lang(tag) if tag else ""
            code = html.unescape(m.group(2))
            if code.endswith("\n"):
                code = code[:-1]
            blocks.append({"span": m.span(), "tag": tag, "canon": canon, "code": code})
        groups = []
        for b in blocks:
            if groups and b["canon"] and out[groups[-1][-1]["span"][1]:b["span"][0]].strip() == "" \
                    and groups[-1][0]["canon"] and b["canon"] not in [x["canon"] for x in groups[-1]]:
                groups[-1].append(b)
            else:
                groups.append([b])
        copy = f'<button type="button" class="code-copy" data-label="{esc(s["copy"])}" data-copied="{esc(s["copied"])}">{esc(s["copy"])}</button>'
        result = []
        last = 0
        for g in groups:
            start, end = g[0]["span"][0], g[-1]["span"][1]
            result.append(out[last:start])
            last = end
            if len(g) == 1:
                b = g[0]
                label = lang_label(b["canon"], b["tag"]) if b["canon"] else ""
                result.append(
                    f'<div class="code" data-lang="{esc(b["canon"])}">'
                    f'<div class="code-bar"><span class="code-lang">{esc(label)}</span>{copy}</div>'
                    f'<pre><code class="hl">{highlight(b["code"], b["canon"])}</code></pre></div>'
                )
                continue
            tabs = "".join(
                f'<button type="button" role="tab" class="code-tab" data-lang="{esc(b["canon"])}" '
                f'aria-selected="{"true" if i == 0 else "false"}" tabindex="{0 if i == 0 else -1}">{esc(lang_label(b["canon"], b["tag"]))}</button>'
                for i, b in enumerate(g))
            panels = "".join(
                f'<div class="code-panel{" is-active" if i == 0 else ""}" role="tabpanel" data-lang="{esc(b["canon"])}">'
                f'<div class="code-panel-label">{esc(lang_label(b["canon"], b["tag"]))}</div>'
                f'<pre><code class="hl">{highlight(b["code"], b["canon"])}</code></pre></div>'
                for i, b in enumerate(g))
            result.append(
                f'<div class="code code-tabs">'
                f'<div class="code-bar"><div class="code-tablist" role="tablist">{tabs}</div>{copy}</div>'
                f'{panels}</div>'
            )
        result.append(out[last:])
        return "".join(result)


# ----------------------------------------------------------------------------
# Pages
# ----------------------------------------------------------------------------

def hreflang_block(en_path: str, ru_path: str) -> str:
    en, ru = SITE + en_path, SITE + ru_path
    return (f'  <link rel="alternate" hreflang="en" href="{en}">\n'
            f'  <link rel="alternate" hreflang="ru" href="{ru}">\n'
            f'  <link rel="alternate" hreflang="x-default" href="{en}">')


def lang_links(en_path: str, ru_path: str, lang: str) -> str:
    cur = ' aria-current="page"'
    return (f'    <a href="{en_path}" hreflang="en" lang="en"{cur if lang == "en" else ""}>EN</a>\n'
            f'    <a href="{ru_path}" hreflang="ru" lang="ru"{cur if lang == "ru" else ""}>RU</a>')


def page(lang: str, title: str, description: str, canonical_path: str, en_path: str, ru_path: str,
         social: str, jsonld: str, content: str, noindex: bool = False) -> str:
    s = S[lang]
    robots = '  <meta name="robots" content="noindex, nofollow">\n' if noindex else ""
    return render_template(
        "page.html", lang=lang, title=esc(title), description=esc(description), robots=robots,
        canonical=esc(SITE + canonical_path), hreflang=hreflang_block(en_path, ru_path),
        social=social, jsonld=jsonld, lang_label=esc(s["lang_label"]),
        lang_links=lang_links(en_path, ru_path, lang), content=content)


def social_block(lang: str, kind: str, url: str, title: str, description: str, image: str,
                 published: str | None = None, tags=()) -> str:
    s = S[lang]
    other = "ru_RU" if lang == "en" else "en_US"
    lines = [
        f'  <meta property="og:type" content="{kind}">',
        f'  <meta property="og:url" content="{esc(url)}">',
        f'  <meta property="og:title" content="{esc(title)}">',
        f'  <meta property="og:description" content="{esc(description)}">',
        f'  <meta property="og:locale" content="{s["locale"]}">',
        f'  <meta property="og:locale:alternate" content="{other}">',
        f'  <meta property="og:image" content="{esc(image)}">',
    ]
    if published:
        lines.append(f'  <meta property="article:published_time" content="{esc(published)}">')
        lines.append(f'  <meta property="article:author" content="{SITE}/">')
    for t in tags:
        lines.append(f'  <meta property="article:tag" content="{esc(t)}">')
    lines += [
        '',
        '  <meta name="twitter:card" content="summary_large_image">',
        f'  <meta name="twitter:title" content="{esc(title)}">',
        f'  <meta name="twitter:description" content="{esc(description)}">',
        f'  <meta name="twitter:image" content="{esc(image)}">',
    ]
    return "\n".join(lines)


def jsonld_block(data: dict) -> str:
    text = json.dumps(data, ensure_ascii=False, indent=2).replace("</", "<\\/")
    return f'  <script type="application/ld+json">\n{text}\n  </script>'


def tags_html(tags, lang: str, linked: bool = True) -> str:
    if not tags:
        return ""
    prefix = S[lang]["prefix"]
    chips = "".join(
        (f'<a class="tag" href="{prefix}/blog/tags/{esc(t)}/">{esc(t)}</a>' if linked else f'<span class="tag">{esc(t)}</span>')
        for t in tags)
    return f'<span class="tags">{chips}</span>'


def meta_line(article: Article, lang: str) -> str:
    s = S[lang]
    parts = []
    if article.is_published:
        parts.append(f'<time datetime="{esc(article.published)}">{esc(fmt_date(article.published, lang))}</time>')
    else:
        parts.append(f'<span class="draft-badge">{esc(s["draft"])}</span>')
        if article.target:
            parts.append(f'<span>{esc(s["target"])} {esc(article.target)}</span>')
    t = tags_html(article.tags, lang)
    if t:
        parts.append(t)
    return "".join(parts)


def updates_section(article: Article, lang: str) -> str:
    items = sorted((u for u in article.updates if isinstance(u, dict)), key=lambda u: str(u.get("date")))
    if not items:
        return ""
    s = S[lang]
    rows = "\n".join(
        f'        <p><span class="u-date">{esc(s["updated"])} {esc(u.get("date"))}:</span> {esc(u.get(lang) or u.get("en") or "")}</p>'
        for u in items)
    return f'\n      <section class="post-section updates">\n{rows}\n      </section>'


def see_also_section(article: Article, lang: str) -> str:
    data = article.json_file("see-also.json")
    items = (data or {}).get(lang) if isinstance(data, dict) else None
    if not items:
        return ""
    s = S[lang]
    rows = []
    for it in items:
        src = ", ".join(x for x in (it.get("source"), fmt_date(it["date"], lang) if it.get("date") else "") if x)
        rows.append(
            f'          <li><a class="see-title" href="{esc(it["url"])}" target="_blank" rel="noopener">{esc(it["title"])}</a>'
            + (f' <span class="see-src">– {esc(src)}</span>' if src else "")
            + (f'<span class="see-why">{esc(it["why"])}</span>' if it.get("why") else "") + "</li>")
    return render_template("section.html", cls="see-also", heading=esc(s["see_also"]),
                           content="        <ul>\n" + "\n".join(rows) + "\n        </ul>")


def discussion_section(article: Article, lang: str) -> str:
    data = article.json_file("discussion.json")
    posts = data.get("posts") if isinstance(data, dict) else data
    if not posts:
        return ""
    s = S[lang]
    names = {"x": "X", "linkedin": "LinkedIn"}
    blocks = []
    for p in posts:
        label = names.get(p.get("platform"), str(p.get("platform")))
        head = f'<a href="{esc(p["url"])}" target="_blank" rel="noopener">{esc(label)}</a>'
        if p.get("comments") is not None:
            head += f' <span class="disc-count">· {esc(plural_comments(int(p["comments"]), lang))}</span>'
        threads = "".join(
            f'\n            <li><span class="disc-handle">{esc(t["handle"])}</span>: {esc(t["summary"])} '
            f'<a href="{esc(t["url"])}" target="_blank" rel="noopener">[{esc(s["thread"])}]</a></li>'
            for t in (p.get("threads") or [])[:3])
        blocks.append(
            f'        <div class="disc-post">\n          <p>{head}</p>'
            + (f'\n          <ul class="disc-threads">{threads}\n          </ul>' if threads else "")
            + "\n        </div>")
    return render_template("section.html", cls="discussion", heading=esc(s["discussion"]), content="\n".join(blocks))


def render_article_page(article: Article, lang: str, errors: list[str]) -> str:
    s = S[lang]
    t = article.text[lang]
    r = Renderer(article, lang)
    body = r.render(t["body"])
    errors.extend(f"{article.key} {lang}: {e}" for e in r.errors)
    sections = "".join((updates_section(article, lang), see_also_section(article, lang), discussion_section(article, lang)))
    content = render_template(
        "article.html", back_href=S[lang]["prefix"] + "/blog/", back_label=esc(s["back_list"]),
        title=esc(article.title(lang)), meta=meta_line(article, lang), body=body, sections=sections)
    url = SITE + article.url(lang)
    title = f'{article.title(lang)} — Dmitrii Petukhov'
    desc = t["description"]
    image = f"{url}{article.cover}" if article.cover else f"{SITE}/card.png"
    mod = max([str(article.published)] + [str(u.get("date")) for u in article.updates if isinstance(u, dict)]) if article.is_published else None
    ld = {
        "@context": "https://schema.org",
        "@type": "BlogPosting",
        "@id": url + "#article",
        "mainEntityOfPage": {"@type": "WebPage", "@id": url},
        "headline": article.title(lang),
        "description": desc,
        "inLanguage": lang,
        "url": url,
        "image": image,
        "author": {"@type": "Person", "@id": SITE + "/#person", "name": s["author"], "url": SITE},
        "publisher": {"@type": "Person", "@id": SITE + "/#person", "name": s["author"]},
    }
    if article.is_published:
        ld["datePublished"] = str(article.published)
        ld["dateModified"] = mod
    if article.tags:
        ld["keywords"] = ", ".join(str(x) for x in article.tags)
    social = social_block(lang, "article", url, article.title(lang), desc, image,
                          str(article.published) if article.is_published else None, article.tags)
    return page(lang, title, desc, article.url(lang), article.url("en"), article.url("ru"), social,
                jsonld_block(ld), content, noindex=not article.is_published)


def render_list_page(lang: str, articles: list[Article], tag: str | None) -> str:
    s = S[lang]
    prefix = s["prefix"]
    items = "\n".join(
        render_template("card.html", href=esc(a.url(lang)), title=esc(a.title(lang)), meta=meta_line(a, lang),
                        description=esc(a.text[lang]["description"]))
        for a in articles) or f'      <li class="list-empty">{esc(s["empty"])}</li>'
    if tag:
        title_text = f'{s["tag"]}: {tag}'
        en_path, ru_path = f"/blog/tags/{tag}/", f"/ru/blog/tags/{tag}/"
        back = f"{prefix}/blog/"
        back_label = s["back_list"]
        desc = f'{s["blog"]}: {tag}'
    else:
        title_text = s["blog"]
        en_path, ru_path = "/blog/", "/ru/blog/"
        back = s["home"]
        back_label = s["back_home"]
        desc = s["list_description"]
    content = render_template("list.html", back_href=back, back_label=esc(back_label), title=esc(title_text), intro="", items=items)
    canonical = en_path if lang == "en" else ru_path
    social = social_block(lang, "website", SITE + canonical, f"{title_text} — Dmitrii Petukhov", desc, SITE + "/card.png")
    return page(lang, f"{title_text} — Dmitrii Petukhov", desc, canonical, en_path, ru_path, social, "", content)


# ----------------------------------------------------------------------------
# Build
# ----------------------------------------------------------------------------

def sorted_published(articles):
    pub = [a for a in articles if a.is_published]
    return sorted(pub, key=lambda a: (str(a.published), a.number), reverse=True)


def write(path: pathlib.Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def clean_built(out: pathlib.Path) -> None:
    for base in (out / "blog", out / "ru" / "blog"):
        if not base.exists():
            continue
        for p in base.iterdir():
            if p.is_dir() and re.match(r"^\d{4}-", p.name):
                shutil.rmtree(p)
            elif p.is_dir() and p.name == "tags":
                shutil.rmtree(p)
            elif p.is_file() and p.name == "index.html":
                p.unlink()


def link_site_assets(out: pathlib.Path) -> None:
    if out.resolve() == ROOT:
        return
    out.mkdir(parents=True, exist_ok=True)
    for name in ("assets", "favicon.svg", "card.png"):
        dst = out / name
        if not dst.exists() and not dst.is_symlink() and (ROOT / name).exists():
            os.symlink(ROOT / name, dst)


def copy_images(article: Article, out: pathlib.Path) -> None:
    for lang in LANGS:
        dest = out / article.url(lang).strip("/")
        for img in article.images():
            shutil.copy2(img, dest / img.name)


def sitemap_entry(en_path: str, ru_path: str, loc_path: str, lastmod: str | None) -> str:
    en, ru, loc = SITE + en_path, SITE + ru_path, SITE + loc_path
    lm = f"\n    <lastmod>{lastmod}</lastmod>" if lastmod else ""
    return (f"  <url>\n    <loc>{loc}</loc>{lm}\n"
            f'    <xhtml:link rel="alternate" hreflang="en" href="{en}"/>\n'
            f'    <xhtml:link rel="alternate" hreflang="ru" href="{ru}"/>\n'
            f'    <xhtml:link rel="alternate" hreflang="x-default" href="{en}"/>\n  </url>\n')


SITEMAP_SHELL = (
    '<?xml version="1.0" encoding="UTF-8"?>\n'
    '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" '
    'xmlns:xhtml="http://www.w3.org/1999/xhtml">\n</urlset>\n'
)


def update_sitemap(out: pathlib.Path, published: list[Article]) -> None:
    src = ROOT / "sitemap.xml"
    text = src.read_text(encoding="utf-8") if src.exists() else SITEMAP_SHELL

    def drop(m):
        loc = m.group(1)
        return "" if re.match(r"^https://donmutti\.com/(ru/)?blog(/|$)", loc) else m.group(0)

    text = re.sub(r"[ \t]*<url>\s*<loc>([^<]*)</loc>.*?</url>\n?", drop, text, flags=re.S)
    entries = ""
    if published:
        entries += sitemap_entry("/blog/", "/ru/blog/", "/blog/", None)
        entries += sitemap_entry("/blog/", "/ru/blog/", "/ru/blog/", None)
        for tag in sorted({str(t) for a in published for t in a.tags}):
            entries += sitemap_entry(f"/blog/tags/{tag}/", f"/ru/blog/tags/{tag}/", f"/blog/tags/{tag}/", None)
            entries += sitemap_entry(f"/blog/tags/{tag}/", f"/ru/blog/tags/{tag}/", f"/ru/blog/tags/{tag}/", None)
        for a in published:
            last = max([str(a.published)] + [str(u.get("date")) for u in a.updates if isinstance(u, dict)])
            entries += sitemap_entry(a.url("en"), a.url("ru"), a.url("en"), last)
            entries += sitemap_entry(a.url("en"), a.url("ru"), a.url("ru"), last)
    text = text.replace("</urlset>", entries + "</urlset>")
    write(out / "sitemap.xml", text)


def build(out: pathlib.Path | None = None, number: int | None = None) -> list[str]:
    articles = load_articles()
    report: list[str] = []
    errors: list[str] = []
    site_out = (out or ROOT).resolve()
    if out is not None:
        link_site_assets(site_out)
    published = sorted_published(articles)

    for a in published:
        probs = a.problems()
        if probs:
            raise BlogError(f"{a.dir.name}: " + "; ".join(probs))

    clean_built(site_out)
    for a in published:
        for lang in LANGS:
            write(site_out / a.url(lang).strip("/") / "index.html", render_article_page(a, lang, errors))
        copy_images(a, site_out)
        report.append(f"article {a.key}: published {a.published}, en + ru, {len(a.images())} image file(s)")

    if published:
        for lang in LANGS:
            write(site_out / S[lang]["prefix"].strip("/") / "blog" / "index.html", render_list_page(lang, published, None))
        report.append(f"lists: /blog/ and /ru/blog/ with {len(published)} article(s)")
        tags = sorted({str(t) for a in published for t in a.tags})
        for tag in tags:
            having = [a for a in published if tag in [str(t) for t in a.tags]]
            for lang in LANGS:
                write(site_out / S[lang]["prefix"].strip("/") / "blog" / "tags" / tag / "index.html", render_list_page(lang, having, tag))
        report.append(f"tag pages: {len(tags)} tag(s) x 2 languages")
    else:
        report.append("lists and tag pages: none, no published articles")

    update_sitemap(site_out, published)
    report.append(f"sitemap.xml: {len(published)} published article(s) listed")

    if number is not None:
        a = next((x for x in articles if x.number == number), None)
        if a is None:
            raise BlogError(f"no article with number {number}")
        if not a.is_published:
            probs = [p for p in a.problems() if not p.endswith("has no title") and not p.endswith("has no description")]
            if probs:
                raise BlogError(f"{a.dir.name}: " + "; ".join(probs))
            prev = out.resolve() if out is not None else ROOT / PREVIEW
            link_site_assets(prev)
            for lang in LANGS:
                write(prev / a.url(lang).strip("/") / "index.html", render_article_page(a, lang, errors))
            copy_images(a, prev)
            report.append(f"draft {a.key}: rendered to {prev.relative_to(ROOT) if prev.is_relative_to(ROOT) else prev}"
                          f"{a.url('en')} and {a.url('ru')} (noindex, not in lists or sitemap)")
    if errors:
        for e in errors:
            report.append("problem: " + e)
        if any(a.is_published for a in published):
            raise BlogError("build problems:\n" + "\n".join(errors))
    return report


# ----------------------------------------------------------------------------
# Commands
# ----------------------------------------------------------------------------

def meta_template(number: int, slug: str, target: str) -> str:
    return (f"number: {number}\nslug: {slug}\ntarget: {target}\nstatus: draft\npublished:\n"
            f"tags: []\ncover:\nupdates: []\n")


def md_template(title: str) -> str:
    return f"---\ntitle: {yq(title) if title else chr(34) * 2}\ndescription: \"\"\n---\n\n"


def draft_template(platform: str, lang: str) -> str:
    return f"---\nplatform: {platform}\nlang: {lang}\nstatus: draft\npublished:\nurl:\n---\n\n"


def cmd_start(args) -> None:
    slug = args.slug
    if not SLUG_RE.match(slug):
        raise BlogError("slug must be kebab-case")
    target = normalize_mask(args.target)
    if any(a.slug == slug for a in load_articles()):
        raise BlogError(f"slug {slug} is already used")
    number = next_number()
    folder = ROOT / "blog" / f"{number:04d}_{slug}"
    folder.mkdir(parents=True)
    (folder / "meta.yml").write_text(meta_template(number, slug, target), encoding="utf-8")
    (folder / "en.md").write_text(md_template(args.title or ""), encoding="utf-8")
    (folder / "ru.md").write_text(md_template(args.title_ru or ""), encoding="utf-8")
    for platform in PLATFORMS:
        (folder / f"{target}_{platform}.md").write_text(draft_template(platform, args.draft_lang), encoding="utf-8")
    print(f"created {folder.relative_to(ROOT)}/")
    for p in sorted(folder.iterdir()):
        print(f"  {p.name}")


def cmd_build(args) -> None:
    out = pathlib.Path(args.out).resolve() if args.out else None
    for line in build(out, args.number):
        print(line)


def cmd_publish(args) -> None:
    a = find_article(args.number)
    if a.is_published:
        raise BlogError(f"article {a.number} is already published ({a.published})")
    date = args.date or today()
    if not DATE_RE.match(date):
        raise BlogError("date must be YYYY-MM-DD")
    probs = [p for p in a.problems() if not p.startswith("status must")]
    for lang in LANGS:
        t = a.text[lang]
        if t is not None:
            if not t["title"].strip():
                probs.append(f"{lang}.md has no title")
            if not t["description"].strip():
                probs.append(f"{lang}.md has no description")
    if probs:
        raise BlogError("cannot publish: " + "; ".join(sorted(set(probs))))
    path = a.dir / "meta.yml"
    text = set_scalar(path.read_text(encoding="utf-8"), "status", "published")
    text = set_scalar(text, "published", date)
    path.write_text(text, encoding="utf-8")
    try:
        for line in build(None, None):
            print(line)
    except BlogError:
        path.write_text(set_scalar(set_scalar(text, "status", "draft"), "published", None), encoding="utf-8")
        raise
    print(f"published {a.key}: {SITE}{a.url('en')} and {SITE}{a.url('ru')}")


def cmd_new_draft(args) -> None:
    a = find_article(args.number)
    target = normalize_mask(args.target or a.target or today())
    name = f"{target}_{args.platform}.md"
    path = a.dir / name
    if path.exists():
        raise BlogError(f"{name} already exists")
    path.write_text(draft_template(args.platform, args.lang), encoding="utf-8")
    print(f"created {path.relative_to(ROOT)}")


def cmd_post_published(args) -> None:
    a = find_article(args.number)
    if not a.is_published:
        raise BlogError(f"article {a.number} is not published")
    draft = next((d for d in a.drafts if d["file"] == args.file), None)
    if draft is None:
        raise BlogError(f"no draft {args.file} in {a.dir.name}/")
    if draft["status"] == "published":
        raise BlogError(f"{args.file} is already published")
    date = args.date or today()
    if not DATE_RE.match(date):
        raise BlogError("date must be YYYY-MM-DD")
    new_name = f"{date}_{draft['platform']}.md"
    if (a.dir / new_name).exists() and new_name != args.file:
        raise BlogError(f"{new_name} already exists")
    path = a.dir / args.file
    write_front_key(path, "status", "published")
    write_front_key(path, "published", date)
    write_front_key(path, "url", args.url)
    if new_name != args.file:
        path.rename(a.dir / new_name)
    print(f"{a.dir.name}/{new_name}: published {date} {args.url}")


def cmd_add_update(args) -> None:
    a = find_article(args.number)
    if not a.is_published:
        raise BlogError("updates are for published articles")
    date = args.date or today()
    path = a.dir / "meta.yml"
    text = path.read_text(encoding="utf-8")
    entry = f"  - date: {date}\n    en: {json.dumps(args.en, ensure_ascii=False)}\n    ru: {json.dumps(args.ru, ensure_ascii=False)}\n"
    if re.search(r"^updates:\s*\[\]\s*$", text, re.M):
        text = re.sub(r"^updates:\s*\[\]\s*$", lambda _m: "updates:\n" + entry.rstrip("\n"), text, count=1, flags=re.M)
        text = text.rstrip("\n") + "\n"
    elif re.search(r"^updates:\s*$", text, re.M):
        lines = text.split("\n")
        idx = next(i for i, l in enumerate(lines) if re.match(r"^updates:\s*$", l))
        end = idx + 1
        while end < len(lines) and (lines[end].startswith(" ") or lines[end].startswith("-")):
            end += 1
        lines[end:end] = entry.rstrip("\n").split("\n")
        text = "\n".join(lines)
    else:
        text = text.rstrip("\n") + "\nupdates:\n" + entry
    path.write_text(text, encoding="utf-8")
    print(f"{a.dir.name}/meta.yml: update {date} added")


def status_rows():
    rows = []
    for a in load_articles():
        rows.append({
            "number": a.number, "slug": a.slug, "title": a.title("en"), "title_ru": a.title("ru"),
            "status": a.status, "date": str(a.published) if a.is_published else str(a.target),
            "drafts": [{"file": d["file"], "platform": d["platform"], "lang": d["lang"], "status": d["status"], "url": d["url"]} for d in a.drafts],
        })
    return rows


def cmd_status(args) -> None:
    rows = status_rows()
    if args.json:
        print(json.dumps(rows, ensure_ascii=False, indent=2))
        return
    if not rows:
        print("no articles")
        return
    for r in rows:
        when = ("published " if r["status"] == "published" else "target ") + r["date"]
        print(f"{r['number']:04d}  {r['status']:<9}  {when:<22}  {r['title']}")
        for d in r["drafts"]:
            tail = f" {d['url']}" if d["url"] else ""
            print(f"        {d['platform']:<8} {d['lang']}  {d['status']}  {d['file']}{tail}")


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(prog="blog.py", description="donmutti.com blog tool")
    sub = ap.add_subparsers(dest="cmd", required=True)

    p = sub.add_parser("start", help="start a new article draft")
    p.add_argument("slug")
    p.add_argument("--target", required=True, help="planned date, may be a mask: 2026-12-xx")
    p.add_argument("--title", help="English title")
    p.add_argument("--title-ru", help="Russian title")
    p.add_argument("--draft-lang", default="en", choices=LANGS, help="language of the platform drafts")
    p.set_defaults(fn=cmd_start)

    p = sub.add_parser("build", help="build published articles, lists, tags and the sitemap")
    p.add_argument("--number", type=int, help="also render this article, a draft goes to a preview folder")
    p.add_argument("--out", help="write into this folder instead of the repository")
    p.set_defaults(fn=cmd_build)

    p = sub.add_parser("publish", help="set an article to published and build")
    p.add_argument("--number", type=int, required=True)
    p.add_argument("--date", help="exact date, default today")
    p.set_defaults(fn=cmd_publish)

    p = sub.add_parser("new-draft", help="add a platform draft to an article")
    p.add_argument("--number", type=int, required=True)
    p.add_argument("--platform", required=True, choices=PLATFORMS)
    p.add_argument("--lang", default="en", choices=LANGS)
    p.add_argument("--target", help="date or mask for the file name, default the article target")
    p.set_defaults(fn=cmd_new_draft)

    p = sub.add_parser("post-published", help="record that a platform draft was posted")
    p.add_argument("--number", type=int, required=True)
    p.add_argument("--file", required=True, help="draft file name, for example 2026-12-xx_x.md")
    p.add_argument("--url", required=True)
    p.add_argument("--date", help="exact date, default today")
    p.set_defaults(fn=cmd_post_published)

    p = sub.add_parser("add-update", help="add an update note to a published article")
    p.add_argument("--number", type=int, required=True)
    p.add_argument("--en", required=True)
    p.add_argument("--ru", required=True)
    p.add_argument("--date", help="default today")
    p.set_defaults(fn=cmd_add_update)

    p = sub.add_parser("status", help="list articles and platform drafts")
    p.add_argument("--json", action="store_true")
    p.set_defaults(fn=cmd_status)

    args = ap.parse_args(argv)
    try:
        args.fn(args)
    except BlogError as e:
        print(f"error: {e}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
