# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a multi-format document generation system that creates professional PDF documents from HTML source files. The project combines HTML/CSS for content authoring with Playwright for PDF rendering and Typst for final document assembly.

## Architecture

The project uses a hybrid approach with three key technologies:

1. **HTML Pages** (`src/pages/`): Source content with embedded CSS styling
2. **Playwright** (Node.js): Converts HTML pages to individual PDFs with consistent formatting
3. **Typst** (`src/typst/main.typ`): Assembles individual page PDFs into the final document

### Build Pipeline

The build process is orchestrated by `build_deck.py`:
1. HTML files → individual page PDFs (via Playwright/Chromium)
2. Individual PDFs → final compiled document (via Typst)

## Common Commands

### Build the Complete Document
```bash
python3 ./build_deck.py
```
This runs the full pipeline and generates `build/deck.pdf`.

### Install Dependencies
```bash
npm install  # Install Playwright
```

### Prerequisites
- Python 3
- Node.js
- Typst compiler
- Playwright (automatically installs Chromium)

## Key Files and Directories

- `build_deck.py`: Main build orchestration script
- `src/pages/page[1-6].html`: Source content pages with embedded styling
- `src/typst/main.typ`: Typst template for final document assembly
- `build/pages/`: Generated individual page PDFs (intermediate files)
- `build/deck.pdf`: Final output document

## Configuration

### Page Configuration
Pages are defined in `build_deck.py` in the `PAGES` list:
```python
PAGES = [
    ("page1.html", "page1.pdf"),
    ("page2.html", "page2.pdf"),
    # ... etc
]
```

### PDF Settings
- Page size: 8.5" × 11" (US Letter)
- Viewport: 1100×1424 pixels (~129 DPI)
- Full background printing enabled
- Zero margins for edge-to-edge design

### Typst Root Configuration
The build script uses `--root` parameter to allow Typst to access files outside its default project scope:
```python
subprocess.check_call([
    "typst", "compile", "--root", str(project_root.parent), 
    str(TYPST_MAIN), str(FINAL_PDF)
])
```

## Development Workflow

### Adding New Pages
1. Create HTML file in `src/pages/` following the naming convention `pageN.html`
2. Add entry to `PAGES` list in `build_deck.py`
3. Add corresponding `#fullpage()` call in `src/typst/main.typ`

### Modifying Existing Pages
1. Edit HTML files directly in `src/pages/`
2. Run `python3 ./build_deck.py` to rebuild

### Styling Guidelines
- Use embedded CSS in HTML files for complete self-contained pages
- Leverage CSS custom properties (variables) for consistent theming
- Design for 8.5×11 aspect ratio
- Consider print-friendly styling (background images, colors)

## Technical Notes

- Playwright renders pages using Chromium with `networkidle` wait condition
- 250ms additional timeout ensures animations/loading complete
- Typst requires specific path handling for cross-directory file access
- Build artifacts in `build/` directory are excluded from version control

## Troubleshooting

### Typst "access denied" errors
Ensure the `--root` parameter is correctly set to allow access to the build directory. The current implementation sets root to the parent of the project directory.

### Missing dependencies
Run `npm install` to ensure Playwright is available. Verify Typst is installed and accessible in PATH.