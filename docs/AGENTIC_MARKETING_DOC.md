# Agentic Process: Building the Prometheus AGS 2026 Marketing Document (Pages 1–6)

This document captures the **prompting methodology** and the **agentic workflow** used to create the Prometheus AGS marketing document content and assemble it into a single PDF deliverable.

It is written so the workflow can later be **productized as an agent** (and integrated into *The Boss*—a customized fork of Cherry Studio) with repeatable steps, tool standards, and progress tracking via a memory server.

---

## 0) Context: What we were building

We are producing a **multi-page marketing document** for **Prometheus Agentic Solutions / Prometheus AGS** that includes:

- A planned **table of contents (TOC)** (derived from an example document)
- **Per-page content generation** (copy + UI/UX examples)
- **Per-page rendering** as **static XHTML/HTML artifacts** suitable for screenshot-to-PDF export
- A final **combined PDF** compiled from the pages

A key requirement of the workflow is that pages can include **UI/UX “example screens”** for platform capabilities (governance, registry, audit evidence, etc.), while still being deterministic and renderable as one page.

---

## 1) Agent system prompt (“AI Platform Sales & Marketing Strategist for Prometheus AGS”)

The agent used in this process operated under the following system prompt (provided by the user), which framed the agent’s default behavior, constraints, and output expectations.

> **System prompt (as used):**
>
> ```
> # Role:
> AI Platform Sales & Marketing Strategist for Prometheus AGS
> 
> ## Background:
> As a seasoned expert in AI platforms and applications consulting, I specialize in analyzing sales meeting insights and partner feedback to craft data-driven, actionable sales strategies. My expertise spans understanding complex AI solution architectures, partner ecosystem dynamics, and enterprise buyer journeys. I have deep knowledge of market positioning, competitive differentiation, and go-to-market strategies specifically tailored for AI/AGS (AI Governance & Strategy) platforms in the rapidly evolving 2026 landscape.
> 
> ## Preferences:
> - Data-driven approach with clear metrics and KPIs
> - Practical, actionable recommendations over theoretical concepts
> - Visual frameworks and structured strategic models
> - Collaborative partner-centric sales methodology
> - Focus on value-based selling rather than feature-based pitching
> 
> ## Profile:
> - version: 0.2
> - language: English
> - description: An AI platform sales strategist who transforms sales meeting notes and partner feedback into comprehensive, actionable go-to-market strategies for Prometheus AGS, driving revenue growth through targeted customer segmentation and partner enablement.
> 
> ## Goals:
> - Analyze sales partner meeting notes to identify key opportunities, challenges, and market insights
> - Develop targeted sales strategies for specific customer segments and markets
> - Create actionable partner enablement plans to maximize Prometheus AGS sales in 2026
> - Identify competitive advantages and differentiation strategies based on field intelligence
> - Generate specific tactical recommendations with measurable outcomes
> 
> ## Constraints:
> - Must base recommendations on actual meeting notes and partner feedback provided
> - All strategies must be realistic and executable within 2026 timeframe
> - Must consider partner capabilities and readiness levels
> - Recommendations must align with typical AI platform sales cycles (3-12 months)
> - Must respect competitive intelligence boundaries and ethical sales practices
> - Cannot make assumptions about Prometheus AGS capabilities not mentioned in provided information
> 
> ## Skills:
> - Sales meeting analysis and insight extraction
> - Strategic market segmentation and targeting
> - Partner ecosystem development and enablement
> - Competitive positioning and differentiation strategy
> - Value proposition articulation for technical solutions
> - Sales playbook and enablement content creation
> - Revenue forecasting and pipeline management
> - Stakeholder mapping and account planning
> - ROI modeling and business case development
> - Change management and adoption strategy
> 
> ## Examples:
> 
> **Example 1 - Strategy Output:**
> "Based on meeting notes indicating partners struggle with technical complexity, recommend developing a '3-tier certification program': 
> - Bronze (product basics, 2-day training)
> - Silver (solution architecture, 5-day workshop)
> - Gold (enterprise implementation, mentor-led)
> Target: Certify 50 Silver partners by Q2 2026 to address identified gap."
> 
> **Example 2 - Market Insight:**
> "Meeting notes reveal 60% of prospects ask about industry-specific use cases. Strategic response: Create vertical solution packages for:
> - Financial Services (compliance focus)
> - Healthcare (data privacy emphasis)
> - Manufacturing (operational AI focus)
> Equip partners with industry-specific ROI calculators and case studies by Q1 2026."
> 
> ## OutputFormat:
> 
> **Step 1: Meeting Notes Analysis**
> - Summarize key themes and insights from provided sales meeting notes
> - Identify patterns across different partners and regions
> - Highlight critical opportunities and obstacles
> 
> **Step 2: Strategic Recommendations**
> - Present 3-5 prioritized strategic initiatives
> - Include specific customer/market segments to target
> - Provide rationale based on meeting insights
> 
> **Step 3: Tactical Action Plans**
> - Break down each strategy into concrete action items
> - Assign timeline recommendations (Q1-Q4 2026)
> - Suggest success metrics and KPIs
> 
> **Step 4: Partner Enablement Requirements**
> - Specify tools, training, and resources partners need
> - Recommend support structures and programs
> 
> **Step 5: Expected Outcomes**
> - Quantify anticipated impact on sales pipeline and revenue
> - Identify risk factors and mitigation approaches
> 
> ## Initialization:
> As your **AI Platform Sales & Marketing Strategist for Prometheus AGS**, I bring expertise in sales analysis, strategic planning, partner enablement, and AI platform go-to-market strategies. I strictly adhere to data-driven recommendations, realistic timelines, ethical sales practices, partner-centric approaches, and actionable insights.
> 
> Welcome! I'm excited to help you transform your sales partner meeting insights into winning strategies for Prometheus AGS in 2026. 
> 
> **I'm ready to analyze your sales meeting notes and develop targeted strategies to accelerate growth.** 
> 
> Please share:
> 1. Your sales partner meeting notes or summaries
> 2. Any specific markets/segments you're particularly focused on
> 3. Current challenges or opportunities you'd like me to prioritize
> 
> Let's build a powerful sales strategy together! 🚀
> ```

**How this prompt was used in practice:**

- Even though the system prompt is oriented toward sales strategy, we applied it as an **operating lens** for copy tone (value-based, outcome-first) and for building UI examples that reinforce **governance + platform assurance**.
- The agent was then steered into **document/page construction tasks** via user instructions (static HTMX pages, inline CSS, UI examples, etc.).

---

## 2) Tooling & environment (“The Boss” + Knowledge Base + Memory)

### 2.1 “The Boss” (custom Cherry Studio fork)
We used a customized tool environment (internally referred to as **The Boss**) that provides:

- A chat-driven agent UI
- A knowledge base for storing artifacts and conversation context
- MCP integrations for file IO and memory tracking

### 2.2 Surreal Memory MCP (progress tracking)
We used (and/or designed the workflow to use) the **Surreal Memory MCP server** to:

- Store the TOC and page objectives
- Track completion status (page-by-page)
- Record corrections (e.g., scope changes between pages)

**Important note:** In this specific conversation thread, we discussed and requested memory updates, but the practical intent is that every page completion should be persisted as a memory update to keep the project state consistent.

---

## 3) Prompt engineering methodology (the repeatable “page factory” loop)

This project followed a repeatable loop that can be formalized into an agent later:

### Step A — Define or confirm the page scope
For each page:

- Confirm the page number and its *unique* purpose within the TOC
- Prevent scope drift (avoid duplicating earlier pages)
- Explicitly list: **headline**, **subheadline**, **modules**, and **UI example(s)**

### Step B — Enforce a rendering standard
We standardized each page as a single renderable artifact:

- **Static HTML/XHTML** output
- **All CSS inline** (no external CSS files)
- **HTMX included** via script tag when requested
- No server-required HTMX requests (no `hx-get` to remote endpoints) unless explicitly available
- **Critical CSS requirements for PDF rendering:**
  - **Zero margins reset:** `html, body { margin: 0; padding: 0; width: 8.5in; height: 11in; overflow: hidden; }`
  - **Fixed page dimensions:** Page containers must use `width: 8.5in; height: 11in;` (not responsive sizing like `min(980px, 100%)` or `aspect-ratio`)
  - **No visual effects:** Set `border-radius: 0;` and `box-shadow: none;` on page containers for PDF output
  - These settings ensure edge-to-edge rendering without white margins in the generated PDFs

### Step C — Build “UI Example” representations
Because a marketing deck often needs UI screenshots before the real UI is available (or before final screenshots are captured), we used a two-tier UI example approach:

1. **Real screenshots** when available (absolute URLs)
2. **Mock UI SVG “screens”** when screenshots are not yet available

The mock UI approach still allows:

- Visual hierarchy (nav + tables + states)
- Themed styling consistent with the brand palette
- Deterministic single-page rendering

### Step D — Add content blocks that sell outcomes
Each page includes:

- A clear value proposition
- Right-rail cards describing “what it is”, “why it matters”, “outputs/outcomes”
- Bottom metrics blocks (short KPI-friendly labels)

### Step E — Iterate / correct
As we discovered mis-scoping or mislabeling, we corrected:

- page number
- module naming
- content structure

### Step F — Mark complete in memory
Once a page meets the standard:

- Store completion status
- Save canonical artifact reference(s): HTML filename, screenshot URLs, etc.

---

## 4) What happened in this conversation (Page 6 creation + correction)

### 4.1 Initial request
The user requested a **single static HTMX file** with:

- inline CSS
- HTMX JS included
- content displayed properly for **Page 6** (explicitly *not* Page 5)

### 4.2 First output (mistake)
The initial Page 6 draft incorrectly used **“Governance Intake”** content (which belongs to Page 5).

### 4.3 Scope correction (critical)
The user corrected the scope:

- **Page 6 = Policy Controls, Evidence & Audit Trail, Model Registry**
- Page 5 already existed

### 4.4 Final Page 6 artifact (static HTMX, self-contained)
We then produced a corrected Page 6 HTML artifact with:

- Header: **Policy Controls, Evidence & Audit Trail, Model Registry**
- A tabbed module selector (3 tabs):
  - Policy Controls
  - Evidence & Audit Trail
  - Model Registry
- Tab behavior:
  - implemented using `hx-on:click` handlers
  - swaps **left UI example**, **right-rail content**, and **bottom metrics**
  - uses inline `<template>` blocks (no server)
- UI examples:
  - implemented as **inline SVG mock screens** (ready to be replaced by real screenshots later)

This satisfies the “one static file” requirement while still showing multiple UI examples.

---

## 5) Assembling the final PDF with Typst

Since Typst cannot render HTML/HTMX directly, we defined a two-stage build pipeline:

1) **Render each HTML page to a single-page PDF** (Playwright/Chromium)
2) **Combine those PDFs into one document** (Typst)

### 5.1 Proposed repository layout

```text
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

### 5.2 Typst template (`src/typst/main.typ`)

- Page size: **8.5in x 11in**
- Margin: **0pt**
- Each page is placed edge-to-edge as an image/PDF page

Key function:

- `fullpage(asset, pdf_page: 1)`

And then:

- `#fullpage("../../build/pages/page1.pdf")`
- `#pagebreak()`
- … repeat through page 6

### 5.3 Build script (`build_deck.py`)
The build program:

- Uses **Playwright (Chromium)** to load each HTML file and export to PDF:
  - `width: '8.5in'`
  - `height: '11in'`
  - `printBackground: true`
  - **`margin: { top: '0', right: '0', bottom: '0', left: '0' }`** (critical: prevents default page margins)
- Then calls Typst:
  - `typst compile src/typst/main.typ build/deck.pdf`

This creates a predictable and repeatable pipeline:

- HTML is the design system + layout source of truth
- PDFs are the intermediate render targets
- Typst is the final assembler for a multi-page deliverable

### 5.4 One-time dependencies

- Typst CLI (`typst` on PATH)
- Node + Playwright
  - `npm i playwright`
  - `npx playwright install chromium`

---

## 6) Why HTMX was included even though pages are “static”

HTMX was included because:

- The standard required “HTMX JS links, etc.”
- We wanted lightweight interactivity (tabs) without a framework

However, to keep pages fully renderable and exportable:

- We avoided server-backed `hx-get` requests
- We used `hx-on:click` only as an event binding mechanism
- Content swaps are performed by cloning inline `<template>` HTML

This preserves:

- portability
- deterministic rendering
- offline/page-local behavior

---

## 7) How this becomes a reusable agent (“Page Builder Agent”)

This workflow can be automated into a structured agent with tools:

### Inputs
- TOC definition (page-by-page spec)
- Brand palette and style tokens
- Asset manifest (screenshots, diagrams, icons)

### Tool chain
- Memory (Surreal MCP) for tracking state
- Renderer (Flux Pro 2.0 via Fal.ai) for illustrations where needed
- HTML/XHTML generator for page layouts
- Playwright exporter for per-page PDFs
- Typst assembler for the final multi-page PDF

### Output
- `src/pages/pageN.html` artifacts
- `build/pages/pageN.pdf` intermediates
- `build/deck.pdf` final deliverable
- README + audit log of changes and scope corrections

---

## 8) Deliverables and artifacts referenced in this process

Within this conversation, we specifically produced:

- **Page 6 static HTML artifact** (Policy Controls / Evidence & Audit Trail / Model Registry)
- A proposed **Typst template** (`src/typst/main.typ`)
- A proposed **build script** (`build_deck.py`) using Playwright + Typst

Other pages (1–5) are referenced as part of the workflow, but their full content artifacts were not reprinted in this conversation thread.

---

## 9) Next recommended hardening steps

1. **Replace mock UI SVGs with real screenshots** for page 6
2. ~~Enforce a consistent per-page wrapper:~~ ✅ **COMPLETED**
   - ~~fixed 8.5x11 container~~ ✅ All pages now use `width: 8.5in; height: 11in;`
   - ~~print-friendly CSS~~ ✅ Zero margins, no border-radius, no box-shadow
3. Add a build check:
   - verify each page renders without network dependency
   - verify each exported PDF is exactly 1 page
4. Add memory automation:
   - automatically mark page complete when an HTML + PDF pair exists

---

## Appendix A — Tabbed “static HTMX” pattern (used on Page 6)

Pattern summary:

- Each tab triggers `hx-on:click="p6Swap(event,'policy')"` etc.
- `p6Swap` swaps:
  - `#p6-ui`
  - `#p6-rail`
  - `#p6-metrics`
- Content is stored in `<template id="...">` blocks

This avoids server endpoints while keeping the interaction model consistent with HTMX conventions.

---

## Appendix B — Critical lesson learned: CSS for PDF rendering (Jan 8, 2026)

### B.1 The problem
After initial page generation, all PDFs had white margins on the top, left, and bottom edges. The content appeared offset/centered rather than edge-to-edge.

### B.2 Root cause
The issue was **not** in the Playwright rendering configuration alone, but primarily in the **HTML/CSS** of the pages:

1. **Default browser margins:** HTML pages had no CSS reset for `html` and `body` elements, which have default margins
2. **Responsive sizing:** Page containers used `width: min(980px, 100%)` with `aspect-ratio: 8.5 / 11` instead of fixed dimensions
3. **Visual effects:** Pages included `border-radius` and `box-shadow` which aren't appropriate for PDF output

### B.3 The solution (two-part fix)

**Part 1: HTML/CSS changes (in all `src/pages/*.html` files)**

Add immediately after the `@import` statement:

```css
/* Reset for PDF rendering - remove all margins */
html, body {
  margin: 0;
  padding: 0;
  width: 8.5in;
  height: 11in;
  overflow: hidden;
}
```

Change the page container (`.pds-page`, `.p2-page`, etc.):

```css
/* Before (WRONG for PDF): */
.page-container {
  width: min(980px, 100%);
  aspect-ratio: 8.5 / 11;
  border-radius: var(--radius);
  box-shadow: var(--shadow);
}

/* After (CORRECT for PDF): */
.page-container {
  width: 8.5in;
  height: 11in;
  border-radius: 0;
  box-shadow: none;
}
```

**Part 2: Playwright configuration (in `build_deck.py`)**

Ensure the `page.pdf()` call includes explicit zero margins:

```javascript
await page.pdf({
  path: 'output.pdf',
  width: '8.5in',
  height: '11in',
  printBackground: true,
  pageRanges: '1',
  margin: {
    top: '0',
    right: '0',
    bottom: '0',
    left: '0'
  }
});
```

### B.4 Prevention checklist

When generating new pages, **always include**:

- [ ] CSS reset for `html, body` with zero margins and fixed dimensions
- [ ] Fixed page container dimensions (`8.5in x 11in`)
- [ ] No `border-radius` or `box-shadow` on the main page container
- [ ] Playwright PDF margins set to `'0'` for all sides
- [ ] Test render a single page before generating all pages

### B.5 Why this matters for the agent workflow

When this process is productized as an agent:

1. The **page generation prompt** must include these CSS requirements as mandatory constraints
2. The **HTML template** should have the CSS reset pre-included
3. The **build script** must enforce zero margins in Playwright configuration
4. **Quality checks** should verify edge-to-edge rendering before marking a page complete

This lesson ensures that future page generation will produce PDFs with proper edge-to-edge rendering from the start, avoiding the need for retroactive fixes.
