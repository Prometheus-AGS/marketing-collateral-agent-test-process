# MARKETING_AGENT_SYSTEM_SPECIFICATION

> **Purpose**: Define how we generalize the end-to-end workflow used to produce the Prometheus AGS 2026 6-page marketing PDF into a reusable **Prometheus Unified Agent Runtime (UAR)** agent (“The Boss”) that can guide any startup/service through **research → ideation → specification → planning → execution (page-by-page) → QA/reflection → final PDF build**.
>
> **Scope**: This spec is grounded in the actual working build pipeline in this repo (`/Users/gqadonis/obsidian/prometheus/2026/paper`) and the actual UAR code in `/Users/gqadonis/Projects/references/axum-leptos-htmx-wc`.

---

## 1) Current state: what we built (paper repo)

### 1.1 Repository: `/Users/gqadonis/obsidian/prometheus/2026/paper`

This repo already contains a deterministic “HTML pages → PDFs → combined PDF” pipeline:

- **Source pages**: `src/pages/page1.html` … `src/pages/page6.html`
- **Intermediate PDFs**: `build/pages/page1.pdf` … `build/pages/page6.pdf`
- **Final combined PDF**: `build/deck.pdf`

### 1.2 Build orchestration: `build_deck.py`

`build_deck.py` is the *actual* build program.

Key behaviors:

- Defines file locations:
  - `HTML_DIR = src/pages`
  - `OUT_PDF_DIR = build/pages`
  - `TYPST_MAIN = src/typst/main.typ`
  - `FINAL_PDF = build/deck.pdf`
- Uses **Node + Playwright** to render each HTML page to a 1-page PDF:
  - `width: '8.5in'`, `height: '11in'`
  - `printBackground: true`
  - explicit `margin: 0` on all sides
- Compiles Typst to assemble the final `build/deck.pdf`.

> **Critical detail**: Typst is compiled with `--root <parent of project>` so that Typst can access PDFs under `build/` even though `main.typ` sits under `src/typst/`.

**Excerpt (ground truth) — Playwright PDF export configuration**:

```js
await page.pdf({
  path: '...',
  width: '8.5in',
  height: '11in',
  printBackground: true,
  pageRanges: '1',
  margin: { top: '0', right: '0', bottom: '0', left: '0' }
});
```

### 1.3 Typst assembly: `src/typst/main.typ`

The Typst file is a “stitcher”: it full-bleeds each single-page PDF into a Typst page.

Key behaviors:

- Page size set to **US Letter** and `margin: 0pt`.
- Uses `image(asset, page: 1, width: 100%, height: 100%)`.

**Excerpt (ground truth)**:

```typst
#set page(
  width: 8.5in,
  height: 11in,
  margin: 0pt,
)

#let fullpage(asset, pdf_page: 1) = {
  image(asset, page: pdf_page, width: 100%, height: 100%)
}
```

### 1.4 Design constraints discovered during build

From the Page 6 iteration and PDF output validation, the workflow depends on strict page-rendering constraints:

- Each HTML page must be deterministic, single-screen, and printable.
- **No browser default margins** (ensure `html, body { margin:0; padding:0; }`).
- The “page container” must be fixed sized: `width: 8.5in; height: 11in;`.
- Avoid `border-radius` / `box-shadow` on the main container for predictable print output.

These become *agent-enforced acceptance criteria*.

---

## 2) UAR grounding: what the runtime already supports (axum-leptos-htmx-wc)

### 2.1 Tool-loop orchestration exists

`src/llm/orchestrator.rs` implements an LLM tool loop that:

- Streams model output
- Detects/accumulates tool calls
- Executes tools via MCP (`McpRegistry`)
- Feeds tool results back to the model
- Repeats until the model completes or hits `MAX_TOOL_ITERATIONS`.

This is a strong foundation for a page-by-page producer that must repeatedly call tools (file writes, builds, validations).

### 2.2 MCP Registry exists (tool discovery + namespacing)

`src/mcp/registry.rs` supports:

- Loading MCP servers from config (`load_from_file`, `from_config`)
- Connecting to MCP servers via stdio or remote HTTP
- Listing tools
- Namespacing tools as `{server}__{tool}` and sanitizing names for OpenAI tool-name constraints
- Executing namespaced tools via `call_namespaced_tool()`

This means the marketing agent can be built as a tool-first system:

- Filesystem IO, memory tracking, rendering, QA, etc. can all be tools.

### 2.3 Skills exist (prompt overlays + per-skill MCP tool bundles)

`src/uar/runtime/skills.rs` loads **`SKILL.md` packages** recursively.

Important behavior:

- Skills have a prompt overlay and triggers.
- If a skill folder contains an `mcp.json`, it is loaded.
- Skill MCP servers are **namespaced to avoid collisions**.

This is the correct mechanism for “sub-agents”: create specialized skills that can be dynamically activated.

### 2.4 Run Manager composes system prompt + RAG + skills + tools

`src/uar/runtime/manager.rs`:

- Builds the effective **system prompt** using:
  - artifact prompt
  - optional RAG content
  - injected skill overlays
- Merges MCP registries:
  - global MCP
  - skill MCP
- Spawns the orchestrator stream
- Emits normalized events (chat deltas, tool starts/ends, state patches, etc.)

This is exactly the runtime we need to guide a user through spec → plan → execute → reflect.

### 2.5 AgentArtifact exists (formal agent package)

`src/uar/domain/artifact.rs` defines `AgentArtifact` with:

- `prompt.system` and `prompt.instructions`
- `policy.tools` and `policy.skills`
- `tools.bundles`
- `memory` config
- `ui` config

This is the correct place to implement “The Boss” as a productized marketing agent.

---

## 3) Problem statement (generalized)

We want an agent/service that can:

1. **Ideate + research** for a company’s positioning, audience, and claims.
2. **Generate a table of contents** from an example deck (or from a target narrative structure).
3. **Plan execution** page-by-page with clear acceptance criteria.
4. **Produce artifacts** deterministically:
   - each page as a printable HTML/XHTML artifact
   - assets (images, icons, diagrams)
   - a final combined PDF
5. **Track progress** and provide a full audit trail:
   - “what changed”
   - “why”
   - “which tool outputs were used”
   - “build status”

---

## 4) Standards & protocols for generalizing into an extensible service

We support and should explicitly integrate these standards where they add leverage:

### 4.1 MCP (Model Context Protocol): agent ↔ tools/data

MCP is the tool substrate for:

- filesystem operations
- memory/progress tracking
- external asset generation
- rendering/build pipeline operations
- linting/QA

In UAR, MCP is already first-class via `McpRegistry`.

### 4.2 A2A (Agent-to-Agent): agent ↔ agent

A2A is a standard for agent-to-agent communication with discovery and capability exchange. A useful way to position it:

- MCP solves agent→tools (“vertical” integration)
- A2A solves agent→agent (“horizontal” integration)

This mapping is explicitly described in third-party summaries (example: Descope’s A2A guide) which frames A2A vs MCP as complementary layers.\
Source: https://www.descope.com/learn/post/a2a

**How A2A fits this marketing-doc agent**:

- The Boss can remain the orchestrator.
- Specialist agents can be external services (research agent, design agent, compliance agent, etc.).
- Each external agent publishes an “Agent Card” and can be discovered dynamically.

### 4.3 AG-UI (Agent–User Interaction): agent ↔ UI

AG-UI is an open, event-based protocol for connecting agentic backends to user-facing applications. The AG-UI docs describe it as a bi-directional protocol that standardizes how agent state and interactions flow between backend and frontend.\
Source: https://docs.ag-ui.com/

**How AG-UI fits**:

- The Boss can run as a service with an AG-UI client (web, desktop, mobile).
- The UX can be more than chat: show plan state, page checklist, build logs, artifact previews.
- The agent can stream structured events (tool calls, state patches), which your UAR already does (see `RunManager` emitting events).

### 4.4 A2UI (Agent-to-UI): declarative generative UI payloads

A2UI is an open project for agent-driven interfaces. Google’s announcement describes:

- a secure, declarative approach to sending UI as data (not executable code)
- compatibility with remote agents and multi-agent meshes
- transport via A2A or AG-UI

Source: https://developers.googleblog.com/introducing-a2ui-an-open-project-for-agent-driven-interfaces/

The A2UI v0.8 specification describes it as a JSONL/SSE streaming protocol for rendering UI progressively.\
Source: https://a2ui.org/specification/v0.8-a2ui/

**How A2UI fits**:

- Today we used HTML/HTMX to mock UI in a printable deck.
- For a generalized service, the agent can optionally output UI previews using A2UI so the host client can render native preview widgets safely.
- This enables “preview the page layout” and “approve/reject section” interactions without trusting raw HTML.

### 4.5 Recommended “protocol stack” viewpoint

For the extensible service, treat the ecosystem as a layered stack:

- **AG-UI**: event transport and UX sync (frontend ↔ backend)
- **A2UI**: optional generative UI payload format (agent ↔ UI)
- **A2A**: agent mesh composition and delegation (agent ↔ agent)
- **MCP**: tools and data access (agent ↔ tools)

This stack is consistent with how Google describes A2UI as being transported over A2A/AG-UI and with AG-UI docs mapping the three prominent open protocols.\
Sources: https://developers.googleblog.com/introducing-a2ui-an-open-project-for-agent-driven-interfaces/ and https://docs.ag-ui.com/

---

## 5) Target agent: “The Boss — Marketing Doc Builder”

### 5.1 Primary capability

Provide a guided, deterministic workflow:

- **Spec → Plan → Execute → Reflect** (with PMPO discipline)
- produce a multi-page marketing doc as:
  - `src/pages/pageN.html`
  - `build/pages/pageN.pdf`
  - `build/deck.pdf`
- store progress and provenance in memory

### 5.2 Output formats (service-level)

The agent should support multiple “deliverable backends”:

- **Deck PDF** (this repo’s pipeline: HTML → per-page PDF → Typst stitched PDF)
- **Web microsite** (export the pages as a multi-route static site)
- **Social cuts** (1080×1350, 1080×1080 crops from page sections)
- **One-pager** (single-page Typst with condensed content)

This is primarily an “export adapter” problem (tools + templates), not a reasoning problem.

---

## 6) Agent architecture inside UAR (single orchestrator + skill-based sub-agents)

### 6.1 Why skills (not fully separate agents) for v1

UAR already supports skill overlays + tool bundle injection, which is sufficient to get “sub-agent behavior” without needing multi-run orchestration.

Use skills as the main decomposition mechanism.

### 6.2 Proposed skill packages (sub-agent roles)

Each skill is a folder with:

- `SKILL.md` (frontmatter + overlay prompt)
- optional `mcp.json` (skill-scoped MCP servers/tools)

Suggested skills:

1. **Research & Narrative Skill**
   - Tavily searches, competitor/market research
   - outputs: `docs/research/*.md`

2. **TOC & Spec Skill**
   - builds TOC (from example), acceptance criteria per page
   - outputs: `docs/spec/TOC.md`, `docs/spec/pageN.md`

3. **Page Copywriter Skill**
   - writes page copy consistent with brand voice

4. **UI Example / Diagram Skill**
   - generates mock UI (SVG), workflows, architecture diagrams

5. **Asset Generation Skill**
   - image generation (Flux/other), icons

6. **HTML/XHTML Page Builder Skill**
   - turns spec + assets into deterministic 8.5×11 pages
   - enforces CSS constraints

7. **QA & Compliance Skill**
   - validates claims, checks tone, ensures citations/attribution

8. **Build & Release Skill**
   - executes `build_deck.py` (or equivalent tool) and verifies outputs

### 6.3 Skill matching

UAR’s `RunManager` already performs:

- tag matching
- vector matching

so you can trigger skills by:

- explicit user commands (“generate TOC”, “render page 3”)
- semantic triggers (“make a cover page”, “build the PDF”, etc.)

---

## 7) Tooling plan: MCP servers needed to cover the whole workflow

### 7.1 Required MCP capabilities

To replicate and generalize the workflow end-to-end, we want tools for:

- progress + memory
- research
- asset generation
- page rendering
- QA
- final build

### 7.2 Proposed MCP servers (buildable in-house)

#### A) `prom_marketing_memory` (Surreal Memory)

- `create_project`, `update_project`
- `set_toc`, `set_page_status`, `append_observation`
- `list_pages`, `current_status`

#### B) `prom_marketing_fs` (Filesystem helpers)

Even with a generic filesystem tool, it’s valuable to provide “safe higher-level” helpers:

- `write_page_html(page_num, html)` → writes to canonical path and records checksum
- `write_asset(name, bytes)`
- `read_page_html(page_num)`

#### C) `prom_marketing_assets` (Flux Pro / image generation)

- `generate_image(prompt, style, size, out_path)`
- `generate_svg_diagram(spec, out_path)` (optional)

#### D) `prom_marketing_lint` (HTML/XHTML + page constraints)

- `validate_xhtml(path)`
- `validate_page_constraints(path)`
  - checks 8.5×11 size
  - checks margin reset
  - checks “no external dependency” policy

#### E) `prom_marketing_render` (HTML → PDF)

Two viable approaches:

1) **Wrap existing build script**: expose `build_pdf(paper_root)` that runs the proven pipeline.
2) **Adopt Playwright MCP**: use an MCP server for browser automation.

Playwright MCP reference: https://github.com/microsoft/playwright-mcp

> In either case, the tool should enforce deterministic rendering, capture logs, and return file paths.

#### F) `prom_marketing_typst` (Typst compile)

- `typst_compile(main_typ, out_pdf, root)`
- `pdf_page_count(path)` (for QA)

> Recommendation: implement **one consolidated “Deck Build MCP server”** that exposes:
> - `render_html_to_pdf`
> - `compile_typst`
> - `build_deck`
> so the agent can’t “shell out” arbitrarily.

---

## 8) Agent system prompt: changes required to generalize

### 8.1 Why the current prompt is insufficient

The prompt used during this project is a “Sales & Marketing Strategist” persona. It is excellent for narrative/copy, but it does not enforce:

- artifact production discipline
- plan execution discipline
- tool-driven verification

### 8.2 New “Boss” system prompt (design)

The new system prompt should:

- operate as an **orchestrator** of specialized skills
- explicitly enforce **Spec → Plan → Execute → Reflect**
- define **Definition of Done** for each page and for the final PDF
- require tool-based verification before claiming success
- require progress tracking writes to memory

#### Required prompt primitives

- **State machine**: `{specifying, planning, executing, reflecting, building, done}`
- **Page loop**: “One page at a time” with acceptance criteria checks
- **Artifact verification**: “Never say complete unless file exists and build succeeds.”
- **Citations policy**: If the agent claims market facts, it must attach sources (Tavily results → citations).

### 8.3 Keep the original strategist prompt as a skill overlay

Instead of using the Sales Strategist prompt as the global system prompt, embed it as a **skill** (Copywriting/Positioning skill).

This preserves:

- value-based selling tone
- KPI focus

without compromising production discipline.

---

## 9) Runtime usage model (how this becomes an extensible service)

### 9.1 “Agent as a Service” (AaaS) approach

Offer this as:

- a hosted UAR backend with MCP connections
- an AG-UI client frontend
- optional A2UI rendering for rich previews
- optional A2A integration for delegating work to external agents

### 9.2 Multi-tenancy & isolation

Key needs:

- workspace isolation per customer/project
- tool policy enforcement (`AgentArtifact.policy.tools` allow/deny)
- data retention and audit trails

### 9.3 Observability & provenance

For each deliverable:

- store:
  - which prompts produced which artifacts
  - tool inputs/outputs
  - hashes of page HTML
  - build logs

This is critical if you’re selling “agentic marketing” to regulated industries.

---

## 10) Execution plan: building the generalized agent (phased)

### Phase 1 (1–2 weeks): deterministic agent + local build

- Create `marketing-doc-boss` AgentArtifact
- Implement core skills:
  - TOC/spec
  - page builder
  - build/release
- Implement a minimal Deck Build MCP server that wraps:
  - Playwright PDF export
  - Typst compile

### Phase 2 (2–4 weeks): QA + assets + preview UX

- Add:
  - lint/constraints server
  - asset generation server
  - A2UI preview mode (optional)
- Add UI:
  - plan panel
  - page checklist
  - artifact previews

### Phase 3 (4–8 weeks): “extensible service” packaging

- Add:
  - templates marketplace
  - multi-tenant project management
  - A2A specialist agent marketplace

---

## 11) Acceptance criteria (for the generalized agent)

A run is considered successful only when:

1. A TOC exists with page-by-page specs.
2. Each page has:
   - `src/pages/pageN.html` present
   - `build/pages/pageN.pdf` present
   - “page constraints validation” passed
3. The combined PDF exists:
   - `build/deck.pdf`
   - correct page count
4. Memory contains:
   - TOC
   - per-page completion status
   - build metadata + timestamps

---

## 12) Appendix: relevant sources (standards)

- A2UI announcement (Google): https://developers.googleblog.com/introducing-a2ui-an-open-project-for-agent-driven-interfaces/
- A2UI v0.8 spec: https://a2ui.org/specification/v0.8-a2ui/
- AG-UI overview: https://docs.ag-ui.com/
- A2A overview (third-party summary): https://www.descope.com/learn/post/a2a
- Playwright MCP server: https://github.com/microsoft/playwright-mcp
