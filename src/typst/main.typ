// src/typst/main.typ
#set page(
  width: 8.5in,
  height: 11in,
  margin: 0pt,
)

// Helper: place a full-page PDF (or image) edge-to-edge
#let fullpage(asset, pdf_page: 1) = {
  // For PDFs, Typst supports selecting a page with `page:`.
  // If you use PNGs instead, remove `page:`.
  image(asset, page: pdf_page, width: 100%, height: 100%)
}

// Pages (single-page PDFs recommended)
#fullpage("../../build/pages/page1.pdf")
#pagebreak()

#fullpage("../../build/pages/page2.pdf")
#pagebreak()

#fullpage("../../build/pages/page3.pdf")
#pagebreak()

#fullpage("../../build/pages/page4.pdf")
#pagebreak()

#fullpage("../../build/pages/page5.pdf")
#pagebreak()

#fullpage("../../build/pages/page6.pdf")
