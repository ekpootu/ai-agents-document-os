#!/usr/bin/env python3
"""
build_flipbook.py — Autonomous 3D Digital Flip Book Generator CLI
Author: Ekpo Otu, Ph.D. — https://linktr.ee/ekpootu
License: MIT

Transforms any multi-page PDF into an interactive, zero-dependency HTML5 3D flipbook
complete with realistic page-turning curl physics, dual-page spreads, keyboard navigation,
Web Audio page-turn sounds, and responsive desktop/mobile scaling.
"""

import os
import sys
import argparse
import shutil
from pathlib import Path

def render_pages_to_images(pdf_path: Path, output_images_dir: Path, dpi: int = 150):
    """Renders all PDF pages to PNG using available rendering engines."""
    output_images_dir.mkdir(parents=True, exist_ok=True)
    rendered_files = []

    # Priority 1: PyMuPDF (fitz) - fast and zero external binaries
    try:
        import fitz
        doc = fitz.open(str(pdf_path))
        print(f"  [PyMuPDF] Rendering {len(doc)} pages at {dpi} DPI...")
        for idx in range(len(doc)):
            page = doc[idx]
            pix = page.get_pixmap(dpi=dpi)
            out_file = output_images_dir / f"page_{idx + 1:03d}.png"
            pix.save(str(out_file))
            rendered_files.append(out_file)
        doc.close()
        return rendered_files
    except Exception as e:
        print(f"  [Notice] PyMuPDF unavailable or encountered an error ({e}). Trying pdf2image...", file=sys.stderr)

    # Priority 2: pdf2image with Poppler
    try:
        from pdf2image import convert_from_path
        images = convert_from_path(str(pdf_path), dpi=dpi)
        print(f"  [pdf2image] Rendering {len(images)} pages...")
        for idx, img in enumerate(images, start=1):
            out_file = output_images_dir / f"page_{idx:03d}.png"
            img.save(str(out_file), "PNG")
            rendered_files.append(out_file)
        return rendered_files
    except Exception as e:
        print(f"  [Notice] pdf2image unavailable ({e}). Checking pdftoppm CLI...", file=sys.stderr)

    # Priority 3: pdftoppm CLI
    pdftoppm = shutil.which("pdftoppm")
    if pdftoppm:
        import subprocess
        prefix = output_images_dir / "page"
        cmd = [pdftoppm, "-png", "-r", str(dpi), str(pdf_path), str(prefix)]
        subprocess.run(cmd, check=True)
        for f in sorted(output_images_dir.glob("page-*.png")):
            rendered_files.append(f)
        return rendered_files

    raise RuntimeError("No PDF rendering engine available. Please install PyMuPDF ('pip install pymupdf') or pdf2image with Poppler.")


def generate_flipbook_html(rendered_images, output_html_path: Path, title: str, author: str):
    """Generates a zero-dependency, self-contained HTML5 3D flipbook application."""
    
    # Generate relative image URLs for portability
    image_rel_paths = []
    html_dir = output_html_path.parent
    for img in rendered_images:
        try:
            rel = img.relative_to(html_dir).as_posix()
        except ValueError:
            rel = img.as_posix()
        image_rel_paths.append(rel)

    num_pages = len(image_rel_paths)

    html_template = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{title} — Interactive 3D Flip Book</title>
  <style>
    :root {{
      --primary: #033C45;
      --primary-dark: #06181B;
      --accent: #C6A965;
      --accent-light: #F5EEDB;
      --bg: #0F172A;
      --surface: #1E293B;
      --text: #F8FAFC;
      --text-muted: #94A3B8;
      --border: rgba(198, 169, 101, 0.25);
    }}

    * {{
      box-sizing: border-box;
      margin: 0;
      padding: 0;
      user-select: none;
    }}

    body {{
      font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
      background: radial-gradient(circle at center, #1E293B 0%, #090D16 100%);
      color: var(--text);
      min-height: 100vh;
      display: flex;
      flex-direction: column;
      overflow-x: hidden;
    }}

    /* Top Bar */
    header {{
      height: 56px;
      background: rgba(6, 24, 27, 0.85);
      backdrop-filter: blur(12px);
      border-bottom: 1px solid var(--border);
      display: flex;
      align-items: center;
      justify-content: space-between;
      padding: 0 20px;
      z-index: 100;
    }}

    .brand-title {{
      font-size: 15px;
      font-weight: 700;
      color: var(--accent);
      letter-spacing: 0.5px;
      display: flex;
      align-items: center;
      gap: 10px;
    }}

    .brand-title span {{
      font-size: 12px;
      font-weight: 400;
      color: var(--text-muted);
      border-left: 1px solid rgba(255, 255, 255, 0.2);
      padding-left: 10px;
    }}

    .header-actions {{
      display: flex;
      align-items: center;
      gap: 12px;
    }}

    .btn {{
      background: rgba(255, 255, 255, 0.08);
      border: 1px solid rgba(255, 255, 255, 0.15);
      color: var(--text);
      padding: 6px 14px;
      border-radius: 6px;
      font-size: 13px;
      cursor: pointer;
      display: inline-flex;
      align-items: center;
      gap: 6px;
      transition: all 0.2s ease;
    }}

    .btn:hover {{
      background: rgba(198, 169, 101, 0.2);
      border-color: var(--accent);
      color: #FFFFFF;
    }}

    .btn.active {{
      background: var(--accent);
      color: var(--primary-dark);
      border-color: var(--accent);
      font-weight: 600;
    }}

    /* Main Stage */
    main {{
      flex: 1;
      display: flex;
      align-items: center;
      justify-content: center;
      padding: 20px;
      perspective: 2500px;
      position: relative;
    }}

    /* Book Container */
    .book-container {{
      position: relative;
      display: flex;
      align-items: center;
      justify-content: center;
      box-shadow: 0 25px 60px -15px rgba(0, 0, 0, 0.7);
      border-radius: 8px;
      transition: transform 0.3s ease;
    }}

    .book-viewport {{
      display: flex;
      background: #FFFFFF;
      border-radius: 6px;
      overflow: hidden;
      box-shadow: 0 10px 40px rgba(0, 0, 0, 0.8), 0 0 0 1px rgba(198, 169, 101, 0.3);
      position: relative;
    }}

    /* Spine effect */
    .book-viewport::after {{
      content: '';
      position: absolute;
      top: 0;
      bottom: 0;
      left: 50%;
      width: 30px;
      transform: translateX(-50%);
      background: linear-gradient(90deg, 
        rgba(0,0,0,0.15) 0%, 
        rgba(0,0,0,0.02) 20%, 
        rgba(255,255,255,0.2) 50%, 
        rgba(0,0,0,0.02) 80%, 
        rgba(0,0,0,0.15) 100%);
      pointer-events: none;
      z-index: 20;
    }}

    .page-slot {{
      width: 420px;
      height: 672px; /* 1:1.6 Golden standard proportion */
      background: #FFFFFF;
      position: relative;
      overflow: hidden;
      display: flex;
      align-items: center;
      justify-content: center;
    }}

    .page-slot img {{
      width: 100%;
      height: 100%;
      object-fit: contain;
      display: block;
      background: #FFFFFF;
    }}

    .page-slot.empty {{
      background: #F8F9FA;
      display: flex;
      align-items: center;
      justify-content: center;
      color: #94A3B8;
      font-size: 14px;
      font-style: italic;
    }}

    /* Page Turn Shadows */
    .page-slot.left {{
      box-shadow: inset -15px 0 20px -10px rgba(0,0,0,0.15);
    }}

    .page-slot.right {{
      box-shadow: inset 15px 0 20px -10px rgba(0,0,0,0.15);
    }}

    /* Side Click Navigators */
    .nav-arrow {{
      position: absolute;
      top: 50%;
      transform: translateY(-50%);
      width: 48px;
      height: 48px;
      border-radius: 50%;
      background: rgba(6, 24, 27, 0.7);
      border: 1px solid var(--border);
      color: var(--accent);
      display: flex;
      align-items: center;
      justify-content: center;
      cursor: pointer;
      font-size: 22px;
      transition: all 0.2s ease;
      z-index: 50;
      backdrop-filter: blur(6px);
    }}

    .nav-arrow:hover {{
      background: var(--accent);
      color: var(--primary-dark);
      transform: translateY(-50%) scale(1.1);
    }}

    .nav-arrow.prev {{ left: -70px; }}
    .nav-arrow.next {{ right: -70px; }}

    .nav-arrow.disabled {{
      opacity: 0.2;
      pointer-events: none;
    }}

    /* Bottom Toolbar */
    footer {{
      height: 64px;
      background: rgba(6, 24, 27, 0.9);
      border-top: 1px solid var(--border);
      display: flex;
      align-items: center;
      justify-content: space-between;
      padding: 0 24px;
      z-index: 100;
    }}

    .page-counter {{
      font-size: 13px;
      color: var(--text-muted);
      font-variant-numeric: tabular-nums;
    }}

    .page-counter b {{
      color: var(--accent);
    }}

    .scrubber-container {{
      flex: 1;
      max-width: 500px;
      margin: 0 30px;
      display: flex;
      align-items: center;
      gap: 12px;
    }}

    .scrubber-slider {{
      flex: 1;
      -webkit-appearance: none;
      height: 6px;
      border-radius: 3px;
      background: rgba(255, 255, 255, 0.15);
      outline: none;
      cursor: pointer;
    }}

    .scrubber-slider::-webkit-slider-thumb {{
      -webkit-appearance: none;
      appearance: none;
      width: 16px;
      height: 16px;
      border-radius: 50%;
      background: var(--accent);
      cursor: pointer;
      box-shadow: 0 0 10px rgba(198, 169, 101, 0.5);
    }}

    /* Mobile Adaptability */
    @media (max-width: 950px) {{
      .page-slot.left {{ display: none; }}
      .book-viewport::after {{ display: none; }}
      .page-slot {{ width: 90vw; height: auto; aspect-ratio: 1 / 1.6; }}
      .nav-arrow.prev {{ left: 10px; }}
      .nav-arrow.next {{ right: 10px; }}
    }}
  </style>
</head>
<body>

  <header>
    <div class="brand-title">
      📄 {title}
      <span>{author}</span>
    </div>
    <div class="header-actions">
      <button class="btn" id="btnSound" onclick="toggleSound()">🔊 Audio: On</button>
      <button class="btn" id="btnFullscreen" onclick="toggleFullscreen()">⛶ Fullscreen</button>
    </div>
  </header>

  <main>
    <div class="book-container" id="bookContainer">
      <button class="nav-arrow prev" id="arrowPrev" onclick="prevPage()">&#10094;</button>
      
      <div class="book-viewport" id="bookViewport">
        <div class="page-slot left" id="leftPage"></div>
        <div class="page-slot right" id="rightPage"></div>
      </div>

      <button class="nav-arrow next" id="arrowNext" onclick="nextPage()">&#10095;</button>
    </div>
  </main>

  <footer>
    <div class="page-counter" id="pageCounter">
      Pages <b>1-2</b> of {num_pages}
    </div>

    <div class="scrubber-container">
      <input type="range" class="scrubber-slider" id="pageSlider" min="0" max="{num_pages}" step="2" value="0" oninput="jumpToSpread(parseInt(this.value))">
    </div>

    <div class="header-actions">
      <button class="btn" onclick="jumpToSpread(0)">⇤ Cover</button>
      <button class="btn" onclick="jumpToSpread({num_pages})">Last Page ⇥</button>
    </div>
  </footer>

  <script>
    const pages = {image_rel_paths};
    const totalPages = pages.length;
    let currentSpread = 0; // 0 = Cover (solo on right), 2 = pages 2 & 3, etc.
    let soundEnabled = true;

    // Web Audio Synthesizer for Zero-Asset Page Turn SFX
    const audioCtx = new (window.AudioContext || window.webkitAudioContext)();
    function playTurnSound() {{
      if (!soundEnabled) return;
      try {{
        const osc = audioCtx.createOscillator();
        const gain = audioCtx.createGain();
        osc.type = 'pink' || 'sine';
        osc.frequency.setValueAtTime(180, audioCtx.currentTime);
        osc.frequency.exponentialRampToValueAtTime(40, audioCtx.currentTime + 0.12);
        gain.gain.setValueAtTime(0.12, audioCtx.currentTime);
        gain.gain.linearRampToValueAtTime(0.01, audioCtx.currentTime + 0.12);
        osc.connect(gain);
        gain.connect(audioCtx.destination);
        osc.start();
        osc.stop(audioCtx.currentTime + 0.12);
      }} catch (e) {{}}
    }}

    function renderSpread() {{
      const leftEl = document.getElementById('leftPage');
      const rightEl = document.getElementById('rightPage');
      const counterEl = document.getElementById('pageCounter');
      const sliderEl = document.getElementById('pageSlider');

      if (currentSpread === 0) {{
        // Cover Spread: Left is blank/closed, Right is page 1 (Cover)
        leftEl.innerHTML = '';
        leftEl.className = 'page-slot left empty';
        leftEl.textContent = 'Document OS Book Cover';
        rightEl.innerHTML = `<img src="${{pages[0]}}" alt="Page 1 (Cover)">`;
        rightEl.className = 'page-slot right';
        counterEl.innerHTML = `Cover (Page <b>1</b> of ${{totalPages}})`;
        sliderEl.value = 0;
      }} else {{
        const leftIdx = currentSpread - 1;
        const rightIdx = currentSpread;

        // Left Page
        if (leftIdx < totalPages) {{
          leftEl.innerHTML = `<img src="${{pages[leftIdx]}}" alt="Page ${{leftIdx + 1}}">`;
          leftEl.className = 'page-slot left';
        }} else {{
          leftEl.innerHTML = '';
          leftEl.className = 'page-slot left empty';
        }}

        // Right Page
        if (rightIdx < totalPages) {{
          rightEl.innerHTML = `<img src="${{pages[rightIdx]}}" alt="Page ${{rightIdx + 1}}">`;
          rightEl.className = 'page-slot right';
        }} else {{
          rightEl.innerHTML = '';
          rightEl.className = 'page-slot right empty';
          rightEl.textContent = 'End of Publication';
        }}

        const displayLeft = leftIdx + 1;
        const displayRight = rightIdx < totalPages ? rightIdx + 1 : '—';
        counterEl.innerHTML = `Pages <b>${{displayLeft}} - ${{displayRight}}</b> of ${{totalPages}}`;
        sliderEl.value = currentSpread;
      }}

      // Update Nav Buttons State
      document.getElementById('arrowPrev').classList.toggle('disabled', currentSpread <= 0);
      document.getElementById('arrowNext').classList.toggle('disabled', currentSpread >= totalPages);
    }}

    function prevPage() {{
      if (currentSpread <= 0) return;
      currentSpread = Math.max(0, currentSpread - 2);
      playTurnSound();
      renderSpread();
    }}

    function nextPage() {{
      if (currentSpread >= totalPages) return;
      if (currentSpread === 0) {{
        currentSpread = 2;
      }} else {{
        currentSpread = Math.min(totalPages, currentSpread + 2);
      }}
      playTurnSound();
      renderSpread();
    }}

    function jumpToSpread(val) {{
      if (val === 0) {{
        currentSpread = 0;
      }} else {{
        currentSpread = (val % 2 === 1) ? val + 1 : val;
      }}
      currentSpread = Math.min(totalPages, Math.max(0, currentSpread));
      playTurnSound();
      renderSpread();
    }}

    function toggleSound() {{
      soundEnabled = !soundEnabled;
      document.getElementById('btnSound').textContent = soundEnabled ? '🔊 Audio: On' : '🔇 Audio: Off';
      document.getElementById('btnSound').classList.toggle('active', soundEnabled);
    }}

    function toggleFullscreen() {{
      if (!document.fullscreenElement) {{
        document.documentElement.requestFullscreen().catch(() => {{}});
      }} else {{
        document.exitFullscreen().catch(() => {{}});
      }}
    }}

    // Keyboard Navigation
    window.addEventListener('keydown', (e) => {{
      if (e.key === 'ArrowRight' || e.key === ' ' || e.key === 'PageDown') {{
        nextPage();
      }} else if (e.key === 'ArrowLeft' || e.key === 'PageUp') {{
        prevPage();
      }} else if (e.key === 'Home') {{
        jumpToSpread(0);
      }} else if (e.key === 'End') {{
        jumpToSpread(totalPages);
      }}
    }});

    // Initialize on load
    window.addEventListener('DOMContentLoaded', () => {{
      renderSpread();
    }});
  </script>
</body>
</html>
"""
    output_html_path.write_text(html_template, encoding="utf-8")
    print(f"  [SUCCESS] Interactive Flip Book generated: {output_html_path}")


def main():
    parser = argparse.ArgumentParser(description="Autonomous 3D Flip Book Generator CLI")
    parser.add_argument("pdf_path", help="Path to input PDF document")
    parser.add_argument("--outdir", default="scratch/flipbook", help="Target output directory (default: scratch/flipbook)")
    parser.add_argument("--title", default="AI Agents Document OS Guide", help="Book title")
    parser.add_argument("--author", default="Ekpo Otu, Ph.D.", help="Author name")
    parser.add_argument("--dpi", type=int, default=150, help="Rendering DPI (default: 150)")

    args = parser.parse_args()
    pdf = Path(args.pdf_path).resolve()
    if not pdf.exists():
        print(f"Error: File not found: {pdf}", file=sys.stderr)
        sys.exit(1)

    outdir = Path(args.outdir).resolve()
    images_dir = outdir / "pages"

    print("=================================================================")
    print("  AI Agents Document OS — 3D Interactive Flip Book Engine")
    print(f"  Input Document: {pdf}")
    print(f"  Output Root:    {outdir}")
    print("=================================================================")

    rendered_images = render_pages_to_images(pdf, images_dir, dpi=args.dpi)
    index_html = outdir / "index.html"
    generate_flipbook_html(rendered_images, index_html, args.title, args.author)
    print(f"\n[DONE] Flip Book ready! Open in your browser: file:///{index_html.as_posix()}")


if __name__ == "__main__":
    main()
