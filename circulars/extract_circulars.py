"""
Extract text from NHAI circular PDFs (run on the DESKTOP, costs no Claude usage).

Usage (Windows example):
    pip install pymupdf
    python extract_circulars.py "F:\\path\\to\\NHAI_circulars" "F:\\path\\to\\out"

Output in <out>:
    text/<name>.txt        full cleaned text of each PDF (page markers included)
    index.csv              name, pages, chars, needs_ocr, guessed circular no/date, subject
    batches/batch_NNN.md   ~100 circulars each: only the first ~1800 chars of each
                           (this is what Claude reads to write the digest - cheap)
    needs_ocr.txt          scanned PDFs with no text layer (OCR these separately)

Safe to re-run: files already extracted are skipped.
"""
import sys, re, csv, hashlib
from pathlib import Path
try:
    import pymupdf as fitz
except ImportError:
    import fitz  # PyMuPDF

HEAD_CHARS = 1800
BATCH_SIZE = 100

def clean(t):
    t = t.replace("\x00", "")
    t = re.sub(r"[ \t]+", " ", t)
    t = re.sub(r"\n{3,}", "\n\n", t)
    return t.strip()

def guess(text):
    head = text[:3000]
    no = re.search(r"(?:Circular|Letter|File)\s*(?:No\.?|Number)?\s*[:\-]?\s*([A-Za-z0-9\-\./\(\)]*\d[A-Za-z0-9\-\./\(\)]*)", head, re.I)
    if not no:
        no = re.search(r"\bNo\.?\s*[:\-]?\s*([A-Za-z0-9\-\./\(\)]*\d[A-Za-z0-9\-\./\(\)]*)", head)
    date = re.search(r"\b(\d{1,2}[./-]\d{1,2}[./-]\d{2,4}|\d{1,2}(?:st|nd|rd|th)?\s+[A-Z][a-z]+,?\s+\d{4})", head)
    subj = re.search(r"(?:Subject|Sub|Ref)\s*[:\-]\s*(.{10,300}?)(?:\n\n|\n[A-Z][a-z]+:|$)", head, re.I | re.S)
    return (no.group(1) if no else ""), (date.group(1) if date else ""), \
           (re.sub(r"\s+", " ", subj.group(1)) if subj else "")

def main(src, out):
    src, out = Path(src), Path(out)
    (out / "text").mkdir(parents=True, exist_ok=True)
    (out / "batches").mkdir(exist_ok=True)
    pdfs = sorted(p for p in src.rglob("*") if p.suffix.lower() == ".pdf")
    print(f"{len(pdfs)} PDFs found")
    rows, ocr_needed, used = [], [], set()
    for i, p in enumerate(pdfs, 1):
        stem = re.sub(r"[^\w\-\.]+", "_", p.stem)[:120]
        if stem in used:
            stem += "_" + hashlib.md5(str(p).encode()).hexdigest()[:6]
        used.add(stem)
        tp = out / "text" / f"{stem}.txt"
        pages = 0
        try:
            if tp.exists():
                text = tp.read_text(encoding="utf-8")
                pages = text.count("\n=== page ") or 0
            else:
                with fitz.open(p) as d:
                    pages = len(d)
                    text = "\n".join(f"\n=== page {n+1} ===\n" + pg.get_text() for n, pg in enumerate(d))
                text = clean(text)
                tp.write_text(text, encoding="utf-8")
        except Exception as e:
            print("FAILED", p, e); ocr_needed.append(f"{p}\tERROR {e}"); continue
        body = re.sub(r"=== page \d+ ===", "", text).strip()
        scanned = len(body) < 80 * max(pages, 1) * 0.3 or len(body) < 100
        if scanned:
            ocr_needed.append(str(p))
        no, date, subj = guess(body)
        rows.append([stem, str(p.relative_to(src)), pages, len(text), int(scanned), no, date, subj])
        if i % 100 == 0:
            print(f"{i}/{len(pdfs)}")
    with open(out / "index.csv", "w", newline="", encoding="utf-8-sig") as f:
        w = csv.writer(f)
        w.writerow(["name", "source_path", "pages", "chars", "needs_ocr", "guess_no", "guess_date", "guess_subject"])
        w.writerows(rows)
    (out / "needs_ocr.txt").write_text("\n".join(ocr_needed), encoding="utf-8")
    # batches for the digest pass
    for old in (out / "batches").glob("batch_*.md"):
        old.unlink()
    good = [r for r in rows if not r[4]]
    for b in range(0, len(good), BATCH_SIZE):
        chunk = good[b:b + BATCH_SIZE]
        parts = [f"# Batch {b // BATCH_SIZE + 1:03d} ({len(chunk)} circulars)\n"]
        for r in chunk:
            t = (out / "text" / f"{r[0]}.txt").read_text(encoding="utf-8")
            t = re.sub(r"=== page \d+ ===", "", t).strip()
            parts.append(f"\n---\n## [{r[0]}]  pages={r[2]}  chars={r[3]}\n{t[:HEAD_CHARS]}\n")
        (out / "batches" / f"batch_{b // BATCH_SIZE + 1:03d}.md").write_text("".join(parts), encoding="utf-8")
    tot = sum(f.stat().st_size for f in (out / "text").glob("*.txt")) / 1e6
    print(f"Done. {len(rows)} processed, {len(ocr_needed)} need OCR, text total {tot:.0f} MB")

if __name__ == "__main__":
    if len(sys.argv) != 3:
        sys.exit(__doc__)
    main(sys.argv[1], sys.argv[2])
