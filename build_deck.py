#!/usr/bin/env python3
import os
import subprocess
from pathlib import Path

HTML_DIR = Path("src/pages")
OUT_PDF_DIR = Path("build/pages")
TYPST_MAIN = Path("src/typst/main.typ")
FINAL_PDF = Path("build/deck.pdf")

PAGES = [
    ("page1.html", "page1.pdf"),
    ("page2.html", "page2.pdf"),
    ("page3.html", "page3.pdf"),
    ("page4.html", "page4.pdf"),
    ("page5.html", "page5.pdf"),
    ("page6.html", "page6.pdf"),
]


def ensure_dirs():
    OUT_PDF_DIR.mkdir(parents=True, exist_ok=True)
    FINAL_PDF.parent.mkdir(parents=True, exist_ok=True)


def render_with_playwright(html_path: Path, pdf_path: Path):
    # Uses Playwright via node for consistent PDF output.
    # Note: Must be served as a file:// URL or http:// URL.
    url = html_path.resolve().as_uri()

    js = f"""
const {{ chromium }} = require('playwright');
(async () => {{
  const browser = await chromium.launch();
  const page = await browser.newPage({{
    viewport: {{ width: 1100, height: 1424 }} // ~8.5x11 at ~129dpi; PDF uses explicit inches below
  }});
  await page.goto('{url}', {{ waitUntil: 'networkidle' }});

  // If your pages animate/load, add a small delay:
  await page.waitForTimeout(250);

  await page.pdf({{
    path: '{pdf_path.as_posix()}',
    width: '8.5in',
    height: '11in',
    printBackground: true,
    pageRanges: '1',
    margin: {{
      top: '0',
      right: '0',
      bottom: '0',
      left: '0'
    }}
  }});

  await browser.close();
}})();
"""
    subprocess.check_call(["node", "-e", js])


def compile_typst():
    # Set root to parent of parent of typst file to allow access to build directory
    project_root = Path.cwd()
    subprocess.check_call(
        [
            "typst",
            "compile",
            "--root",
            str(project_root.parent),
            str(TYPST_MAIN),
            str(FINAL_PDF),
        ]
    )


def main():
    ensure_dirs()

    # 1) Render each HTML page to PDF
    for html_name, pdf_name in PAGES:
        html_path = HTML_DIR / html_name
        pdf_path = OUT_PDF_DIR / pdf_name

        if not html_path.exists():
            raise FileNotFoundError(f"Missing HTML: {html_path}")

        print(f"Rendering {html_path} -> {pdf_path}")
        render_with_playwright(html_path, pdf_path)

    # 2) Assemble into final PDF via Typst
    print(f"Compiling Typst -> {FINAL_PDF}")
    compile_typst()

    print("Done.")


if __name__ == "__main__":
    main()
