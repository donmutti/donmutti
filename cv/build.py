#!/usr/bin/env python3
"""Render cv/index.html to the CV PDF using headless Chromium."""
import pathlib
from playwright.sync_api import sync_playwright

ROOT = pathlib.Path(__file__).parent
HTML = ROOT / "index.html"
OUT = ROOT.parent / "Dmitrii Petukhov – CV.pdf"

with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page(viewport={"width": 794, "height": 1123})
    page.goto(HTML.as_uri())
    page.emulate_media(media="print")
    page.pdf(
        path=str(OUT),
        width="8.277in",
        height="11.706in",
        print_background=True,
        margin={"top": "0", "bottom": "0", "left": "0", "right": "0"},
    )
    browser.close()

print(f"wrote {OUT}")
