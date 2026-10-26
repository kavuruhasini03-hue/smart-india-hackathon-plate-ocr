# Incomplete Number Plate Recognition

**Smart India Hackathon 2023 — Finalist**

An end-to-end deep learning system that reads Indian number plates — including damaged, occluded, and low-quality ones — and reconstructs the correct plate number.

> **Status:** Active build. Numbers below are targets. Verified results will replace them as each milestone completes.

---

## What it does

1. **Detects** the plate in a full vehicle photo (YOLOv8)
2. **Reads** the characters from the cropped plate (custom CNN + EasyOCR)
3. **Corrects** partial or garbled output using an LLM that knows Indian plate format rules
4. **Serves** predictions via a REST API with under 200 ms latency

---

## Results (to be measured — targets from resume)

| Metric | Target | Actual |
|---|---|---|
| Reconstruction accuracy on 2,000+ real test images | 90% | TBD |
| Error reduction vs baseline OCR | 30% | TBD |
| Improvement on occluded images | 40% | TBD |
| End-to-end inference latency | <200 ms | TBD |

*Every number in this table will come from a single reproducible run. See `docs/BUILD_LOG.md` for methodology.*

---

## Quick start

```bash
# 1. Clone and set up
git clone https://github.com/YOUR_USERNAME/smart-india-hackathon-plate-ocr.git
cd smart-india-hackathon-plate-ocr
pip install -r requirements.txt

# 2. Add your API keys
cp .env.example .env
# Edit .env — add ANTHROPIC_API_KEY, KAGGLE credentials, ROBOFLOW_API_KEY

# 3. Download data
python scripts/download_data.py

# 4. Preprocess
python scripts/preprocess.py

# 5. Train (or use pre-trained weights)
# See notebooks/ for Kaggle training notebooks

# 6. Run the API
uvicorn src.api.main:app --reload

# 7. Test with an image
curl -X POST http://localhost:8000/predict \
     -F "file=@your_plate_image.jpg"
```

---

## Project structure

```
├── data/                   # gitignored — rebuilt via scripts/download_data.py
├── docs/
│   ├── DATA_SOURCES.md     # every dataset: URL, license, image count, why it was chosen
│   ├── BUILD_LOG.md        # real-time log of decisions, failures, fixes
│   └── INTERVIEW_GUIDE.md  # plain-language explanation of every component
├── notebooks/              # Kaggle training notebooks (runnable end-to-end)
├── scripts/
│   ├── download_data.py    # fetch all datasets from Kaggle + Roboflow
│   ├── preprocess.py       # resize, split, build test set
│   ├── generate_synthetic.py  # create synthetic plates to fill dataset gaps
│   └── evaluate.py         # compute all metrics on the test set
├── src/
│   ├── detection/          # YOLOv8 plate detection
│   ├── ocr/                # OCR pipeline
│   ├── correction/         # LLM-based sequence correction
│   └── api/                # FastAPI server
├── .env.example
└── requirements.txt
```

---

## Indian number plate formats supported

| Type | Format | Example |
|---|---|---|
| Standard private | `SS NN X(X) NNNN` | `MH 12 AB 1234` |
| Bharat Series | `YY BH NNNN XX` | `22 BH 1234 AA` |
| Commercial | Yellow background, same format | `KA 01 A 5678` |
| Electric vehicle | Green background, same format | `TS 09 EA 1234` |

---

## License

Code: MIT  
Data: see `docs/DATA_SOURCES.md` for individual dataset licenses. The OCR training data (CC BY-NC-SA) means this project may not be used commercially without replacing that dataset.
