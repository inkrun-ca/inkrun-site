#!/usr/bin/env python3
"""Render the sample edition PDF to pre-rendered page images for the viewer.

Usage (from the repo root):  python3 tools/pdf-to-pages.py
Renderer, checked in this order: pypdfium2 (pip install pypdfium2),
pdftoppm (poppler), Ghostscript — all three need Pillow for WebP output
(pypdfium2 wheels usually bundle it as a dependency; otherwise pip install
Pillow). If none is found, install pypdfium2.

Outputs, into sample-pages/:
  page-NN.webp   full pages, 2600px wide, WebP q82 (dropped to q75 if the
                 folder tops ~12MB)
  thumb-NN.webp  thumbnails, 300px wide, WebP q75
  manifest.json  per PDF page: files, pixel size, double-truck flag, print
                 page range (a truck counts as two print pages)

This is the seed of the future upload pipeline (see inkrun-md/DECISIONS.md).
"""
import json
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PDF_PATH = ROOT / "Sample" / "EDGJun26_2026.pdf"
OUT_DIR = ROOT / "sample-pages"
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
    print(f"sample-pages/ total: {total / 1024 / 1024:.1f} MB")


if __name__ == "__main__":
    main()
