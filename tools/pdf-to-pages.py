#!/usr/bin/env python3
"""Render the sample edition PDF to pre-rendered page images for the viewer.

Usage (from the repo root):  python3 tools/pdf-to-pages.py [--pdf PDF] [--out DIR]
Renderer, checked in this order: pypdfium2 (pip install pypdfium2),
pdftoppm (poppler), Ghostscript — all three need Pillow for WebP output
(pypdfium2 wheels usually bundle it as a dependency; otherwise pip install
Pillow). If none is found, install pypdfium2.

Outputs, into the output dir (default sample-pages/):
  page-NN.webp   full pages, 2600px wide, WebP q82 (dropped to q75 if the
                 folder tops ~12MB)
  thumb-NN.webp  thumbnails, 300px wide, WebP q75
  manifest.json  per PDF page: files, pixel size, double-truck flag, print
                 page range (a truck counts as two print pages)

This is the seed of the future upload pipeline (see inkrun-md/DECISIONS.md).
"""
import argparse
import json
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DEFAULT_PDF = ROOT / "Sample" / "EDGJun26_2026.pdf"
DEFAULT_OUT = ROOT / "sample-pages"
FULL_W, FULL_Q = 2600, 82
THUMB_W, THUMB_Q = 300, 75
SIZE_CAP = 12 * 1024 * 1024
TRUCK_FACTOR = 1.6  # page this much wider than the median page = double truck


def via_pypdfium2():
    """Render directly at each target size. Returns (sizes_pt, render_fn)."""
    import pypdfium2 as pdfium

    pdf = pdfium.PdfDocument(str(PDF_PATH))
    sizes = [page.get_size() for page in pdf]

    def render(index, target_w):
        w, _ = sizes[index]
        return pdf[index].render(scale=target_w / w).to_pil().convert("RGB")

    return sizes, render


def via_external(cmd, output_pattern):
    """Render once at 150dpi with pdftoppm/Ghostscript, downscale with Pillow.
    Returns (sizes_px, render_fn) or None."""
    try:
        from PIL import Image
    except ImportError:
        return None
    tmp = tempfile.mkdtemp()
    try:
        subprocess.run(cmd + ["-sOutputFile=" + str(Path(tmp) / output_pattern), str(PDF_PATH)]
                       if cmd[0] == "gs" else cmd + [str(PDF_PATH), str(Path(tmp) / "p")],
                       check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        pngs = sorted(Path(tmp).glob("*.png"))
        if not pngs:
            return None
        images = []
        for p in pngs:
            im = Image.open(p)
            im.load()
            images.append(im)
    except Exception:
        return None
    finally:
        shutil.rmtree(tmp, ignore_errors=True)
    sizes = [(im.width, im.height) for im in images]

    def render(index, target_w):
        im = images[index]
        h = round(im.height * target_w / im.width)
        return im.resize((target_w, h), Image.LANCZOS).convert("RGB")

    return sizes, render


def pick_renderer():
    try:
        import pypdfium2  # noqa: F401
        return via_pypdfium2(), "pypdfium2"
    except ImportError:
        pass
    if shutil.which("pdftoppm"):
        r = via_external(["pdftoppm", "-png", "-r", "150"], "p-*.png")
        if r:
            return r, "pdftoppm"
    if shutil.which("gs"):
        r = via_external(["gs", "-dNOPAUSE", "-dBATCH", "-sDEVICE=png16m", "-r150"],
                         "p-%02d.png")
        if r:
            return r, "ghostscript"
    sys.exit("No PDF renderer found. Install one, e.g.:  pip install pypdfium2")


def main():
    global PDF_PATH, OUT_DIR, FULL_W, FULL_Q
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--pdf", type=Path, default=DEFAULT_PDF,
                        help="input PDF (default: %(default)s)")
    parser.add_argument("--out", type=Path, default=DEFAULT_OUT,
                        help="output directory for pages, thumbs and manifest (default: %(default)s)")
    parser.add_argument("--width", type=int, default=FULL_W,
                        help="full-page pixel width (default: %(default)s)")
    parser.add_argument("--quality", type=int, default=FULL_Q,
                        help="full-page WebP quality (default: %(default)s; auto-drops to 75 over the size cap)")
    args = parser.parse_args()

    PDF_PATH = args.pdf.resolve()
    OUT_DIR = args.out.resolve()
    FULL_W = args.width
    FULL_Q = args.quality

    (sizes, render), engine = pick_renderer()
    count = len(sizes)
    widths = sorted(w for w, _ in sizes)
    median_w = widths[count // 2]
    trucks = [w > median_w * TRUCK_FACTOR for w, _ in sizes]

    OUT_DIR.mkdir(exist_ok=True)
    pages = []
    folio = 1
    fulls = []
    for i in range(count):
        full = render(i, FULL_W)
        render(i, THUMB_W).save(OUT_DIR / f"thumb-{i + 1:02d}.webp",
                                "WEBP", quality=THUMB_Q)
        fulls.append(full)
        pages.append({
            "page": f"page-{i + 1:02d}.webp",
            "thumb": f"thumb-{i + 1:02d}.webp",
            "width": full.width,
            "height": full.height,
            "truck": trucks[i],
            "print": [folio, folio + 1] if trucks[i] else [folio, folio],
        })
        folio += 2 if trucks[i] else 1

    quality = FULL_Q
    while True:
        for i, full in enumerate(fulls):
            full.save(OUT_DIR / pages[i]["page"], "WEBP", quality=quality)
        total = sum(p.stat().st_size for p in OUT_DIR.iterdir() if p.suffix == ".webp")
        if total <= SIZE_CAP or quality <= 75:
            break
        quality = 75  # over budget: drop full pages to q75 and regenerate

    manifest = {
        "source": PDF_PATH.name,
        "pageCount": count,
        "printCount": folio - 1,
        "pages": pages,
    }
    (OUT_DIR / "manifest.json").write_text(json.dumps(manifest, indent=2) + "\n")

    total = sum(p.stat().st_size for p in OUT_DIR.iterdir())
    print(f"renderer: {engine}")
    print(f"{count} PDF pages, {folio - 1} print pages, "
          f"{sum(trucks)} double truck(s), full quality q{quality}")
    print(f"{OUT_DIR.name}/ total: {total / 1024 / 1024:.1f} MB")


if __name__ == "__main__":
    main()
