#!/usr/bin/env python3
"""Copy report images into docs/proposal/figs and create placeholder images for missing figures.

Usage: .venv\Scripts\python.exe scripts/make_figs.py
"""
from pathlib import Path
from shutil import copy2
try:
    from PIL import Image, ImageDraw, ImageFont
except Exception:
    Image = None

ROOT = Path(__file__).resolve().parents[1]
REPORTS = ROOT / 'reports'
OUT_DIR = ROOT / 'docs' / 'proposal' / 'figs'
OUT_DIR.mkdir(parents=True, exist_ok=True)

copies = [
    ('class_distribution.png', 'figure_extra_class_distribution.png'),
    ('confusion_matrix.png', 'figure3_confusion.png'),
    ('training_performance.png', 'figure4_training.png'),
    ('loss_curve.png', 'figure4_loss.png'),
    ('train_val_gap.png', 'figure4_train_val_gap.png'),
]

for src, dst in copies:
    s = REPORTS / src
    if s.exists():
        copy2(s, OUT_DIR / dst)
        print('copied', s, '->', OUT_DIR / dst)
    else:
        print('missing report image:', s)

def make_placeholder(path: Path, text: str, size=(1200, 720), bgcolor=(240,240,240)):
    if Image is None:
        # create a tiny text file as fallback
        path.write_text(text)
        print('wrote placeholder text', path)
        return
    img = Image.new('RGB', size, color=bgcolor)
    d = ImageDraw.Draw(img)
    try:
        font = ImageFont.truetype('arial.ttf', 28)
    except Exception:
        font = ImageFont.load_default()
    try:
        # Pillow >=8: textbbox available
        bbox = d.textbbox((0, 0), text, font=font)
        w, h = bbox[2] - bbox[0], bbox[3] - bbox[1]
    except Exception:
        try:
            w, h = font.getsize(text)
        except Exception:
            w, h = (len(text) * 7, 14)
    d.text(((size[0]-w)/2, (size[1]-h)/2), text, fill='black', font=font)
    img.save(path)
    print('created', path)

placeholders = {
    'figure1_system.png': 'Figure 1: System architecture (placeholder)',
    'figure2_landmarks.png': 'Figure 2: Selected landmarks and engineered features (placeholder)',
    'figure5_demo.png': 'Figure 5: Real-time demo screenshot (placeholder)',
    'figure6_occlusion.png': 'Figure 6: Pose estimation failure examples (placeholder)',
    'figure7_latency.png': 'Figure 7: Latency breakdown chart (placeholder)',
}

for name, text in placeholders.items():
    p = OUT_DIR / name
    if not p.exists():
        make_placeholder(p, text)

print('done')
