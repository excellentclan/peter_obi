# Quality assurance and known limitations

**Source checked:** supplied `Peter Obi Projects as Governor updated(1).pdf` and NDC logo. 15 November 2026.

## Verification completed

| Check | Result |
|---|---|
| Original scanned document page count | **340 pages**, confirmed using PyMuPDF |
| Meaningful embedded PDF text | Not available beyond repeated `CamScanner` text |
| Original PDF integrity | Output PDF SHA-256 matches uploaded PDF exactly |
| Prepared page images | All **340** numbered WebP page images present |
| OCR | Tesseract generated page-indexed text for all **340** scanned pages, with confidence scores |
| Responsive HTML/JavaScript | Browser JavaScript executed with no reported page errors at 1365, 390 and 320 px |
| Horizontal overflow | None at 1365, 390 and 320 px in Chromium layout checks |
| Reader page navigation | Page 1 → page 2 and direct page 340 navigation validated |
| Last-page boundary | Next-page control disabled at page 340 |
| Text reading | OCR text displayed for selected source pages |
| Continuous scroll | 340 virtualized/lazy-loaded page slots rendered; programmatic navigation to page 340 validated |
| Document search | OCR query `hospital` returned 45 page results in tested build; `health` returned 32 |
| Search overlay | Open and close interactions validated |
| Page bookmarks | Bookmark state and saved-page link validated in desktop and mobile layouts |
| GitHub Pages compatibility | Relative asset references; no custom backend or API required |
| Original PDF download | Source PDF included and download links present; document bytes SHA-256 checked |
| Source provenance note | Present in application |

## Not fully verified

- **No live GitHub Pages deployment has been made.** Browser checks used HTML-loaded Chromium DOM interactions, with representative image data inlined for screenshots. They did not test the actual deployed HTTP content delivery.
- Safari on actual iOS devices, Android hardware, network throttling and screen-reader/manual WCAG 2.2 AA testing have not been carried out.
- The **single-file** variant's 60.7 MB initial transfer may be unsuitable for slow mobile connections. Use the standard asset-based edition for deployment.
- OCR is automated and was not human-verified on all 340 pages. Page headings, names, figures and amounts may be misrecognized or omitted; search will return false negatives. The scanned page remains the authoritative source.
- Printed page numbers are not mapped 1:1 to PDF indices.
- Page turns use a light page-transition effect, not a physically simulated book engine.
- Social cards use a relative preview image path; absolute Open Graph URLs can be added after a public domain is chosen.
- No external evidence-verification process was performed. This is a digital presentation of a historical source.

## Recommended public release check

After deployment, manually check first and last images, one page from each thematic section, search for a known phrase, browser back/forward behaviour, local PDF downloads and mobile readability on a physical device. Commission a human OCR correction pass if you plan to quote exact amounts, dates or names publicly.
