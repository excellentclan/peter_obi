# Peter Obi: The Anambra Governance Record

An NDC-branded, source-preserving digital reading experience for the uploaded historical publication **Is Anambra State Cursed or Are We the Cause?** This is a client-side website suitable for GitHub Pages. It presents the historical document as a primary source, not a fact-checked audit or a certification of political affiliation.

## What is included

- `index.html`: Complete responsive layout, CSS, JavaScript, original NDC logo embedded inline, 340-page OCR index embedded inline, page-by-page reading interface and project collection cards. No JavaScript library, framework, or CDN is required.
- `assets/pages/0001.webp` through `assets/pages/0340.webp`: All 340 scans prepared for efficient on-demand reading. The original PDF is **not modified**.
- `assets/peter-obi-anambra-original.pdf`: Original uploaded 340-page scanned PDF (19.5 MB), provided as a direct download.
- `assets/ndc-logo.png`: Original uploaded logo.
- `assets/social-preview.jpg`: Site social-sharing preview.
- `data/ocr-index.json`: Full machine-generated page-by-page text index with confidence data.
- `scripts/build_archive.py`: Reproducible OCR and page-rendering workflow.
- `scripts/assemble_site.py`: Assembles the self-contained application code and, optionally, a fully embedded single-file edition.
- `index.template.html`: Maintainable source template for the website. **Do not deploy the template instead of `index.html`.**
- `QA.md`: Verification and limitations.

## Publish to GitHub Pages

1. Create a GitHub repository, for example `anambra-governance-record`.
2. Extract the provided **GitHub Pages ZIP**. Put `index.html` and the `assets` folder at the **repository root**. You may also upload `README.md`, `QA.md`, `data`, `scripts` and `index.template.html` for reproducibility.
3. Commit and push the repository contents to its `main` branch. GitHub Desktop or Git is recommended because the project contains 340 images. An example using Git from within the extracted directory:

   ```bash
   git init
   git add .
   git commit -m "Publish Anambra governance archive"
   git branch -M main
   git remote add origin https://github.com/YOUR_USERNAME/anambra-governance-record.git
   git push -u origin main
   ```

4. On GitHub open **Settings → Pages → Build and deployment**. Choose **Deploy from a branch**, `main`, and `/ (root)`. Save.
5. The site will be available at `https://YOUR_USERNAME.github.io/anambra-governance-record/` after GitHub Pages publishes it.
6. Verify that the cover, a middle PDF page, the last PDF page, search and original PDF download all work on the public address.

**Paths are relative**, so the site works under a GitHub Pages repository subpath. No API keys or hosting backend are required.

## Strictly one-file option

A separate `anambra-standalone-index.html` has been generated. It contains **everything in one HTML file**: the responsive application, NDC logo, all 340 page images, OCR index and original 19.5 MB PDF encoded directly in the HTML. To deploy it alone, rename this file to `index.html` and push it to the root of a GitHub Pages repository. Because it is approximately **61 MB**, use Git or GitHub Desktop rather than GitHub's browser file-upload interface.

**Recommended for a public-facing mobile experience:** use the regular project ZIP. The one-file edition transfers the entire PDF and all pages during the initial page load, whereas the regular edition loads individual pages only as visitors request them.

## Reader features

- Page-by-page navigation, keyboard arrows, touch swipe gestures and subtle page transitions.
- Continuous scroll with lazy-loaded page images and automatic unloading of images far from the viewport.
- OCR text mode, source-page navigation and text-size controls.
- Search across the **actual OCR transcription** of all 340 pages with contextual snippets.
- Navigation by source-grounded categories; direct PDF-page selection and nearby thumbnails.
- Page bookmarks saved to local storage and links to specific PDF pages via `?page=NN&mode=flip#reader`.
- Fit-to-width/fit-to-page and manual zoom controls; full-screen mode where supported.
- Download of the **unaltered** source PDF.
- Responsive layouts tested at widths of 320 px, 390 px and 1,365 px.

## Content integrity

- The source document has **340 PDF pages**, contrary to an earlier prompt that said 150.
- Almost every page is a scanned image; the source's extractable text consists predominantly of a `CamScanner` footer. The searchable text was created with Tesseract OCR and is **not a quality-assured transcription**.
- PDF page indices do not consistently match printed pagination in the historical scans. All application page links refer to the **PDF page index**, beginning with page 1 for the cover.
- The original PDF is preserved byte-for-byte and is never overwritten by OCR.
- Summaries on the landing page describe what the historical publication **says it documents**. They are not external verification of expenditures, implementation completion, impacts or contemporary political nominations.
- The NDC logo brands this **modern presentation**, not the original publication.
- The public publisher should confirm redistribution rights for the scanned publication and photographs.

## Rebuild the OCR and page images

For a technical editor who wishes to rerun processing:

```bash
python -m pip install pymupdf pillow
# Install the Tesseract OCR executable using your OS package manager.
python scripts/build_archive.py assets/peter-obi-anambra-original.pdf
python scripts/assemble_site.py
# Or regenerate the standalone file from the project root:
python scripts/assemble_site.py --standalone
```

Run `assemble_site.py` from within the provided `scripts` directory only through the path above. The `--standalone` output is written to the **parent of the project folder** and named `anambra-standalone-index.html`.

The `data/ocr-index.json` file includes confidence scores to assist editorial quality checks. For public quotations, finances, exact numbers and names, check the corresponding original scans before adding any claims.

## Notes for publishing

- Add an absolute `og:image` URL and canonical URL to the head of `index.html` after you know the final website address, if rich link previews are essential.
- There are no cookies, user analytics or third-party trackers in the application. Bookmarks and the last-read position remain in the reader's browser local storage.
- The downloadable original PDF is a separately linked static asset in the recommended build. In the one-file build, it is embedded and decoded on demand when the visitor presses **Download original PDF**.
