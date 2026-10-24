#!/usr/bin/env python3
"""Render card/index.html to the Open Graph card PNG using headless Chromium."""
import pathlib
from playwright.sync_api import sync_playwright

ROOT = pathlib.Path(__file__).parent
HTML = ROOT / "index.html"
OUT = ROOT.parent / "card.png"

with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page(viewport={"width": 1200, "height": 630})
    page.goto(HTML.as_uri())
    page.wait_for_timeout(300)
    page.screenshot(path=str(OUT))
    browser.close()

print(f"wrote {OUT}")
