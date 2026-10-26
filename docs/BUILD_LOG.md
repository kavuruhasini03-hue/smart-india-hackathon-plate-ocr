# Build Log

This log is written in real time as the project is built.  
It answers: what was done, why, what broke, and how it was fixed.  
Written for a future reader who wants to understand every decision.

---

## 2026-10-26 — Project Kickoff

### Context
Rebuilding the "Incomplete Number Plate Recognition" project from Smart India Hackathon 2023. The goal is working code on GitHub that I can explain in every interview detail.

Resume claims to hit:
- 90% reconstruction accuracy on 2,000+ test images
- 30% fewer errors vs baseline OCR
- 40% better on occluded inputs
- <200 ms inference latency

Ground rule: every number in the README must come from a real run. Targets, not givens.

### Environment decisions
- **GPU:** Kaggle Notebooks (Pro) — free T4/P100 GPUs, no timeout limit on Pro
- **Why Kaggle over Colab:** Kaggle Pro offers longer sessions and more consistent GPU availability than Colab free tier. All training notebooks are checkpointed so a session restart doesn't lose work.
- **Python:** 3.10 (default on Kaggle 2025 kernels)
- **Frameworks:** PyTorch (detection), EasyOCR + custom CNN (OCR), Anthropic SDK (LLM correction), FastAPI (API)

### Repository structure chosen

```
smart-india-hackathon-plate-ocr/
├── data/                    # gitignored — download via scripts/download_data.py
│   ├── raw/                 # original downloaded datasets
│   ├── processed/           # cleaned, resized, split
│   ├── synthetic/           # synthetically generated plates
│   └── test/                # held-out test set (2000+ real images)
├── docs/                    # documentation
│   ├── DATA_SOURCES.md      # dataset research and format rules
│   ├── BUILD_LOG.md         # this file
│   └── INTERVIEW_GUIDE.md   # beginner-friendly explanation (written last)
├── notebooks/               # Kaggle/Colab training notebooks
├── scripts/                 # download, preprocess, evaluate scripts
├── src/
│   ├── detection/           # YOLOv8 plate detection
│   ├── ocr/                 # OCR engine (EasyOCR + custom)
│   ├── correction/          # LLM-based sequence correction
│   └── api/                 # FastAPI inference server
├── .env.example             # template for secrets
└── requirements.txt         # pinned dependencies
```

### Why this architecture?
The pipeline has three distinct stages, each with a different failure mode:
1. **Detection** — misses or mis-frames the plate (spatial problem → CNN/YOLO)
2. **OCR** — misreads characters (visual similarity → trained OCR)
3. **Correction** — OCR output doesn't match any valid plate pattern (knowledge problem → LLM with constraints)

Keeping them separate means we can measure, improve, and swap each stage independently.

---

## Step 0 — Data Research (2026-10-26)

### What was searched
- Kaggle: "indian number plate dataset", "india license plate OCR"
- Roboflow Universe: "indian license plate"
- HuggingFace Datasets: "indian number plate"
- Papers with Code: "indian license plate recognition"
- Known IIT/NIT datasets

### Datasets selected
See `docs/DATA_SOURCES.md` for full details. Summary:

1. **Roboflow — Indian License Plate Detection** — ~3,500–5,000 images, CC BY 4.0, YOLO format. Primary detection training set.
2. **Kaggle — Rohit Saha OCR** — ~5,000 cropped plates with text labels, CC BY-NC-SA 4.0. Primary OCR training set.
3. **Kaggle — Shivank Sharma** — ~3,000 images, CC0, YOLO boxes. Supplementary detection and validation.
4. **Synthetic generation** — MIT-licensed tool to fill BH-series, EV plates, rare state codes.

### Test set plan
Hold out ~2,000 real images across all three real datasets. Stratified by image quality (day/night/occluded) where metadata is available.

### Gaps identified
- BH-series plates are nearly absent from open datasets — will fill synthetically
- North-East state codes (AR, MZ, NL, SK, MN) are underrepresented — synthetic fill
- Night/low-light: ~15% coverage in best dataset — augmentation + synthetic

### Next steps
- [x] Write `scripts/download_data.py`
- [ ] Run download script, verify file counts
- [ ] Build preprocessing pipeline (resize, normalize, split)
- [ ] Verify test set has 2,000+ real images

---

*(entries added as each milestone completes)*
