# Repository Guidelines

This repository builds a six-page Prometheus AGS PDF from HTML source pages. The pipeline renders HTML with Playwright/Chromium and assembles the final document with Typst.

## Project Structure & Module Organization
- `src/pages/`: Source HTML pages (`page1.html` ... `page6.html`) with inline CSS.
- `src/typst/main.typ`: Typst template that stitches page PDFs together.
- `build_deck.py`: Build orchestrator (HTML -> page PDFs -> final deck PDF).
- `build/`: Generated outputs (`build/pages/*.pdf`, `build/deck.pdf`); do not edit by hand.

## Build, Test, and Development Commands
- `npm install`: Installs Playwright.
- `npx playwright install chromium`: Ensures the Chromium browser is available for rendering.
- `python3 ./build_deck.py`: Runs the full pipeline and writes PDFs into `build/`.
- `typst compile --root .. src/typst/main.typ build/deck.pdf`: Optional manual Typst run if you need to debug assembly.

## Coding Style & Naming Conventions
- HTML pages are named `pageN.html`; keep content fully self-contained (inline CSS, no external stylesheets).
- Use CSS custom properties for palette/typography consistency and design for an 8.5x11 layout.
- When adding pages, update `PAGES` in `build_deck.py` and the Typst include list in `src/typst/main.typ`.
- Python follows standard 4-space indentation; no formatter is enforced.

## Testing Guidelines
- There is no automated test suite; `npm test` intentionally exits with an error.
- Manual checks: run `python3 ./build_deck.py`, then verify `build/pages/pageN.pdf` and `build/deck.pdf` visually.

## Commit & Pull Request Guidelines
- This directory is not currently a git repository, so no commit conventions are enforced.
- If you initialize git, use short, imperative commits like "Add page7 layout" and include PDFs or screenshots in PRs for visual changes.

## Dependencies & Configuration Tips
- Prerequisites: Python 3, Node.js, Typst on PATH, and Playwright's Chromium download.
- Use absolute URLs for external assets to ensure Playwright can fetch them during rendering.
