# Prometheus AGS 2026 Paper / Deck Build Notes (Pages 1–6)

This README summarizes what we did in this chat to generate the **Page 6** HTML/HTMX artifact (and fix styling issues), and how we set up a **Typst-based build pipeline** to combine **six pages** into a single **PDF**.

---

## 1) What happened in the conversation (end-to-end)

### A) Initial problem: missing CSS / incorrect rendering
- You reported that the provided HTML artifacts **did not include the CSS** needed for proper Prometheus AGS branding, so the pages did not render correctly.
- We fixed this by moving to a design where:
  - **All required CSS is included inline** in the HTML (no dependency on external stylesheets).
  - The file includes the **HTMX JS script tag**.

### B) Static-only constraint: no fragment endpoints
- You clarified the deliverable must be a **single static HTMX file** with everything embedded:
  - Inline CSS
  - HTMX JS include
  - All content embedded (no `/fragments/...` requests)
- We adjusted from a “fragment endpoint” approach to a **single self-contained page**.

### C) Page numbering correction (Page 6 ≠ Governance Intake)
- We initially produced a static page, but you identified a scope mismatch:
  - **Governance Intake** is **Page 5** (already done)
  - **Page 6** must be: **Policy Controls**, **Evidence & Audit Trail**, **Model Registry**
- We re-analyzed and produced **Page 6** correctly.

### D) Page 6 deliverable (final page artifact)
We produced a **single, embed-ready `<section>`** for **Page 6**, with:
- **Prometheus AGS branded CSS** fully inline (palette, typography, layout, cards, metrics).
- **HTMX included** via `<script src="https://unpkg.com/htmx.org@1.9.12"></script>`.
- A three-tab UX (static, no server):
  - **Policy Controls**
  - **Evidence & Audit Trail**
  - **Model Registry**
- Each tab swaps:
  - the **left UI example panel** (implemented as inline SVG “mock UI” screens)
  - the **right-rail descriptive cards**
  - the **bottom metrics row**
- Swapping is driven by HTMX’s `hx-on:click` calling a tiny inline JS helper.

> Note: The UI examples were implemented as **mock “screens”** (SVG-based) because we only had a Governance Intake screenshot URL available earlier, and Page 6 required different UI examples.

### E) “Mark complete through Page 6”
- You requested that we mark progress complete through Page 6 in the Surreal Memory MCP server and provide status.
- In the chat, we discussed/returned a completion status summary for pages through **Page 6**.

### F) Building a single combined PDF (Typst plan)
You requested a **Typst template + program** to combine the first 6 pages into **one PDF**.
Because Typst does not natively render HTML/HTMX, we proposed a robust two-stage pipeline:
1) Render each HTML page into a **single-page PDF** (Chromium/Playwright)
2) Use **Typst** to assemble those PDFs into one combined document

This ensures:
- pixel-accurate rendering of the HTML pages (including background colors and embedded assets)
- consistent 8.5"×11" output
- a clean, deterministic build step for the final PDF

---

## 2) Files we defined / referenced

### Suggested repository layout
```
deck/
  src/
    pages/
      page1.html
      page2.html
      page3.html
      page4.html
      page5.html
      page6.html
    typst/
      main.typ
  build/
    pages/          # generated single-page PDFs
    deck.pdf        # final combined output
  build_deck.py
```

### Page 6 artifact
- **`src/pages/page6.html`**
  - Self-contained Page 6 section
  - Inline CSS
  - HTMX included
  - Tabs swap UI example + rail + metrics via inline templates

### Typst assembly template
- **`src/typst/main.typ`**
  - Page size: **8.5in × 11in**, marginless
  - Includes each generated page PDF full-bleed
  - Produces: `build/deck.pdf`

### Build program
- **`build_deck.py`**
  - Renders each HTML page into a single-page PDF with Playwright/Chromium
  - Runs `typst compile` to assemble all page PDFs into the final combined PDF

---

## 3) Build pipeline (how to generate the final PDF)

### Step 1 — Install dependencies
**Typst CLI** (must be on PATH)

**Node + Playwright**
```bash
npm init -y
npm i playwright
npx playwright install chromium
```

### Step 2 — Render HTML pages to PDFs
The script uses Playwright to open each `pageN.html` and export a PDF at **8.5in × 11in**, with `printBackground: true`.

### Step 3 — Assemble final PDF via Typst
Typst includes each `build/pages/pageN.pdf` full-bleed, then pagebreaks.

Run everything:
```bash
./build_deck.py
```

Output:
- `build/pages/page1.pdf` … `build/pages/page6.pdf`
- `build/deck.pdf`

---

## 4) Operational notes / gotchas

- **Avoid HTMX network calls** in “static render” pages: Playwright will only render what the page can load without a server. Page 6 was built to be self-contained.
- Use **absolute URLs** for images/assets to ensure Playwright can fetch them during rendering.
- Ensure each HTML page’s layout is stable at print size (8.5×11). We used an **aspect-ratio** + fixed container approach.
- If/when you have real screenshots for Page 6 (Policy Controls / Evidence / Registry), replace the SVG mock screens with `<img>` tags while keeping the same swap templates.

---

## 5) Current completion scope
- This conversation produced a corrected, self-contained **Page 6** artifact aligned to:
  - **Policy Controls**
  - **Evidence & Audit Trail**
  - **Model Registry**
- We also defined the **Typst + Playwright** approach to combine **Pages 1–6** into a single final PDF.
