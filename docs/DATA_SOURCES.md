# Data Sources

Research conducted: 2026-10-26  
Purpose: Indian number plate detection and OCR for the Smart India Hackathon plate-recognition project.

---

## Selected Datasets

### Primary: Plate Detection (bounding boxes)

#### Roboflow Universe — Indian License Plate Detection
| Field | Value |
|---|---|
| URL | https://universe.roboflow.com/indian-lp/indian-license-plate-detection |
| Owner | Community contributors (Roboflow Universe) |
| License | CC BY 4.0 — research and commercial use allowed with attribution |
| Images | ~3,500–5,000 (version 3 as of mid-2025) |
| Labels | Bounding boxes in YOLO, COCO JSON, and Pascal VOC formats |
| Image quality | Day and night; highway, urban, toll booths; cars, autorickshaws, trucks, motorcycles |
| States covered | KA, MH, TN, DL, UP, RJ (North, South, West India dominant) |
| Why trusted | Version-controlled on Roboflow; ~5,000+ downloads; used in multiple GitHub ANPR projects |
| Role in project | **Detection training** — locating the plate region in a full vehicle image |

---

### Primary: Plate OCR (cropped plates + text labels)

#### Kaggle — Indian Number Plate OCR (Rohit Saha)
| Field | Value |
|---|---|
| URL | https://www.kaggle.com/datasets/rohitsahay05/indian-number-plate |
| Owner | Rohit Saha (individual contributor) |
| License | CC BY-NC-SA 4.0 — **non-commercial** research and portfolio use only |
| Images | ~5,000 cropped plate images |
| Labels | Ground-truth text strings in a CSV file (one label per image) |
| Image quality | Mostly daytime; some night (~15%); cars and two-wheelers; North and West India states |
| Why trusted | ~2,000+ downloads; widely cited in student and academic projects; CSV labels are machine-readable and clean |
| Role in project | **OCR training** — reading the text from a cropped plate |

**License note:** CC BY-NC-SA means this data cannot be used in a commercial product. Fine for a portfolio/research project. If you ever commercialise, replace this dataset with a commercially-licensed one.

---

### Supplementary: Detection + OCR

#### Kaggle — Indian License Plate Dataset (Shivank Sharma)
| Field | Value |
|---|---|
| URL | https://www.kaggle.com/datasets/shivank856/indianlicenseplate |
| Owner | Shivank Sharma |
| License | CC0 1.0 (Public Domain) — no restrictions whatsoever |
| Images | ~3,000 real photos |
| Labels | Bounding boxes in YOLO format; some images include plate text in filename/CSV |
| Image quality | Mostly daylight; highway and road; multi-state; cars and two-wheelers; 480p–1080p |
| Why trusted | CC0 is the strongest open license possible; images are real photos not renders |
| Role in project | **Supplementary detection** and validation set; text labels where available used for OCR fine-tuning |

---

### Synthetic Gap-Fill

#### indian-license-plate-gen (GitHub)
| Field | Value |
|---|---|
| URL | https://github.com/ankandrew/indian-license-plate-gen |
| License | MIT — fully open |
| Capability | Generates synthetic plate images using Square 721 BT font and correct Indian formats |
| Use case | Fill gaps: BH-series plates, electric vehicle green plates, North-East states, night conditions |
| Role in project | **Synthetic training/augmentation only** — test set will contain real images only |

**Important:** All reported accuracy numbers use the real-image test set. Synthetic data is for training only and is called out clearly in results.

---

## Test Set Strategy

Target: 2,000+ real plate images, held out from all training.

| Source | Count | Split |
|---|---|---|
| Roboflow detection set (held out) | ~700 | Test |
| Kaggle Rohit Saha (held out) | ~1,000 | Test |
| Kaggle Shivank Sharma (held out) | ~300 | Test |
| **Total** | **~2,000** | **Test only** |

Stratification: where image quality metadata is available (day/night, vehicle type), the test set is stratified to match real-world distribution. Where not available, random stratified split by source.

---

## Datasets Evaluated But Not Selected

| Dataset | Reason not selected |
|---|---|
| IITB-Vehicle Dataset (IIT Bombay) | Access gated — requires institutional email approval (2–4 week wait); included if access granted |
| ANLPR-India (NIT Warangal) | Academic research only; limited online availability |
| HuggingFace keremberke/license-plate-object-detection | Multi-country set; Indian subset too small (~200 images) |
| Kaggle andrewmvd/car-plate-detection | Only ~100–150 Indian plates; used as a small supplementary validation set |

---

## Indian Number Plate Format Rules

Source: Ministry of Road Transport and Highways (MoRTH), HSRP guidelines, and the Motor Vehicles Act 1988.  
Reference: https://en.wikipedia.org/wiki/Vehicle_registration_plates_of_India

### Standard Private Vehicle Format (HSRP, post-2005)
```
Format:    SS NN X(X) NNNN
Example:   MH 12 AB 1234
           KA 01 A  5678
           TS 09 EA 1234

SS   = State/UT code (2 letters)
NN   = District RTO number (01–99)
X(X) = Series letter(s): 1 letter (A–Z) then 1–2 more (AA–ZZ), cycling
NNNN = Unique 4-digit number (0001–9999)
```

### Bharat Series Format (post-2021, transferable plates)
```
Format:    YY BH NNNN XX
Example:   22 BH 1234 AA
           23 BH 5678 BC

YY   = Year of first registration (21, 22, 23 ...)
BH   = Fixed literal "BH"
NNNN = 4-digit number
XX   = 2-letter series
```

### Special Plate Types by Color
| Category | Background | Text color | Notes |
|---|---|---|---|
| Private vehicle | White | Black | Most common |
| Commercial (taxi/truck) | Yellow | Black | Auto-rickshaws, trucks |
| Electric vehicle | Green | White | Introduced 2019 |
| Government/Central | White | Blue | Central govt vehicles |
| Defense | Black | White/Yellow | Army, Navy, Air Force |
| Diplomatic | White | Blue | "CD" prefix, embassy |

### Valid State / UT Codes
```
AN  Andaman & Nicobar     AP  Andhra Pradesh         AR  Arunachal Pradesh
AS  Assam                 BR  Bihar                  CH  Chandigarh
CG  Chhattisgarh          DD  Daman & Diu            DL  Delhi
DN  Dadra & Nagar Haveli  GA  Goa                    GJ  Gujarat
HP  Himachal Pradesh      HR  Haryana                JH  Jharkhand
JK  Jammu & Kashmir       KA  Karnataka              KL  Kerala
LA  Ladakh                LD  Lakshadweep            MH  Maharashtra
ML  Meghalaya             MN  Manipur                MP  Madhya Pradesh
MZ  Mizoram               NL  Nagaland               OD  Odisha
PB  Punjab                PY  Puducherry             RJ  Rajasthan
SK  Sikkim                TN  Tamil Nadu             TR  Tripura
TS  Telangana             UK  Uttarakhand            UP  Uttar Pradesh
WB  West Bengal
```

### Common OCR Confusions (used in LLM correction prompt)
| Correct | Often misread as | Context |
|---|---|---|
| 0 | O, D | Zero looks like letter O or D at low res |
| O | 0 | Letter O looks like zero |
| 1 | I, L | One looks like letter I or L |
| I | 1 | Letter I looks like numeral 1 |
| 8 | B | Eight looks like B on dirty plates |
| B | 8 | B looks like 8 |
| 5 | S | Five looks like S |
| S | 5 | S looks like 5 |
| 2 | Z | Two looks like Z |
| Z | 2 | Z looks like 2 |
| 6 | G | Six looks like G at low resolution |
| 4 | A | Four can look like A on worn plates |

### Font
- **Standard font:** Square 721 BT (Bitstream) — legally mandated for HSRP plates since 2005
- Used in synthetic plate generation to match real-world appearance
