"""
Download all datasets required for the Indian number plate recognition project.

Usage:
    python scripts/download_data.py

Prerequisites:
    pip install kaggle roboflow python-dotenv tqdm requests

    Set in .env (see .env.example):
        KAGGLE_USERNAME=...
        KAGGLE_KEY=...
        ROBOFLOW_API_KEY=...

    OR export KAGGLE_USERNAME and KAGGLE_KEY before running.

What this script downloads:
    1. Kaggle — Shivank Sharma plate detection dataset   (~3,000 images)
    2. Kaggle — Rohit Saha OCR dataset                   (~5,000 cropped plates)
    3. Roboflow — Indian License Plate Detection v3      (~5,000 images)
    4. Synthetic plate generator (clones GitHub repo)

Everything lands in data/raw/ (gitignored).
Run this script to reproduce the dataset from scratch.
"""

import os
import sys
import subprocess
import zipfile
import shutil
from pathlib import Path

# ── Load .env if present ────────────────────────────────────────────────────
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass  # dotenv optional; env vars can be set in shell

# ── Paths ────────────────────────────────────────────────────────────────────
ROOT = Path(__file__).resolve().parent.parent
DATA_RAW = ROOT / "data" / "raw"
DATA_RAW.mkdir(parents=True, exist_ok=True)


def run(cmd: list[str], cwd: Path | None = None) -> None:
    """Run a shell command and raise if it fails."""
    print(f"  $ {' '.join(cmd)}")
    result = subprocess.run(cmd, cwd=cwd, capture_output=True, text=True)
    if result.returncode != 0:
        print(result.stderr)
        raise RuntimeError(f"Command failed: {' '.join(cmd)}")
    if result.stdout.strip():
        print(result.stdout.strip())


def check_env(keys: list[str]) -> bool:
    missing = [k for k in keys if not os.environ.get(k)]
    if missing:
        print(f"  [SKIP] Missing environment variables: {', '.join(missing)}")
        print(f"         Set them in .env or export them in your shell.")
        return False
    return True


# ── Step 1: Kaggle datasets ──────────────────────────────────────────────────

def download_kaggle_dataset(dataset_slug: str, dest: Path) -> None:
    """Download a Kaggle dataset by its slug (owner/dataset-name)."""
    dest.mkdir(parents=True, exist_ok=True)
    run(["kaggle", "datasets", "download", "-d", dataset_slug, "--unzip", "-p", str(dest)])
    print(f"  Saved to: {dest}")


def step1_kaggle() -> None:
    print("\n[Step 1] Kaggle datasets")
    if not check_env(["KAGGLE_USERNAME", "KAGGLE_KEY"]):
        return

    # Write kaggle.json to ~/.kaggle/ so the CLI picks it up
    kaggle_dir = Path.home() / ".kaggle"
    kaggle_dir.mkdir(exist_ok=True)
    kaggle_json = kaggle_dir / "kaggle.json"
    if not kaggle_json.exists():
        import json
        creds = {
            "username": os.environ["KAGGLE_USERNAME"],
            "key": os.environ["KAGGLE_KEY"],
        }
        kaggle_json.write_text(json.dumps(creds))
        kaggle_json.chmod(0o600)

    # Dataset 1: Shivank Sharma — plate detection (CC0)
    print("  Downloading: shivank856/indianlicenseplate ...")
    download_kaggle_dataset(
        "shivank856/indianlicenseplate",
        DATA_RAW / "kaggle_shivank_detection",
    )

    # Dataset 2: Rohit Saha — OCR (CC BY-NC-SA 4.0)
    print("  Downloading: rohitsahay05/indian-number-plate ...")
    download_kaggle_dataset(
        "rohitsahay05/indian-number-plate",
        DATA_RAW / "kaggle_rohit_ocr",
    )


# ── Step 2: Roboflow dataset ─────────────────────────────────────────────────

def step2_roboflow() -> None:
    print("\n[Step 2] Roboflow — Indian License Plate Detection")
    if not check_env(["ROBOFLOW_API_KEY"]):
        return

    try:
        from roboflow import Roboflow
    except ImportError:
        print("  [SKIP] roboflow package not installed. Run: pip install roboflow")
        return

    dest = DATA_RAW / "roboflow_detection"
    dest.mkdir(parents=True, exist_ok=True)

    rf = Roboflow(api_key=os.environ["ROBOFLOW_API_KEY"])

    # Workspace and project slugs from Roboflow Universe URL:
    # https://universe.roboflow.com/indian-lp/indian-license-plate-detection
    # Verify these are current at the URL above — they can change if the owner renames the project.
    try:
        project = rf.workspace("indian-lp").project("indian-license-plate-detection")
        version = project.version(3)  # v3 as of mid-2025; bump if a newer version exists
        dataset = version.download("yolov8", location=str(dest))
        print(f"  Saved to: {dest}")
    except Exception as e:
        print(f"  [WARN] Roboflow download failed: {e}")
        print("         Try visiting the URL and downloading manually:")
        print("         https://universe.roboflow.com/indian-lp/indian-license-plate-detection")


# ── Step 3: Synthetic plate generator ────────────────────────────────────────

def step3_synthetic_generator() -> None:
    print("\n[Step 3] Synthetic plate generator (MIT license)")
    gen_dir = ROOT / "data" / "synthetic_gen_repo"

    if gen_dir.exists():
        print(f"  Already cloned at {gen_dir}. Pulling latest ...")
        run(["git", "pull"], cwd=gen_dir)
    else:
        print("  Cloning ankandrew/indian-license-plate-gen ...")
        run([
            "git", "clone",
            "https://github.com/ankandrew/indian-license-plate-gen.git",
            str(gen_dir),
        ])

    print(f"  Generator ready at: {gen_dir}")
    print("  Run scripts/generate_synthetic.py to produce synthetic plates.")


# ── Step 4: Verify downloads ─────────────────────────────────────────────────

def step4_verify() -> None:
    print("\n[Step 4] Verification — counting downloaded images")

    image_exts = {".jpg", ".jpeg", ".png", ".bmp", ".webp"}
    total = 0

    for source_dir in DATA_RAW.iterdir():
        if not source_dir.is_dir():
            continue
        count = sum(
            1 for f in source_dir.rglob("*")
            if f.suffix.lower() in image_exts
        )
        print(f"  {source_dir.name}: {count:,} images")
        total += count

    print(f"\n  Total images in data/raw/: {total:,}")

    if total < 5_000:
        print("  [WARN] Fewer than 5,000 images. Check API keys and re-run.")
    else:
        print("  [OK] Enough images to proceed.")


# ── Main ─────────────────────────────────────────────────────────────────────

def main() -> None:
    print("=" * 60)
    print("Indian Number Plate — Dataset Download Script")
    print("=" * 60)
    print(f"Output directory: {DATA_RAW}")

    # Install deps if missing
    required = ["kaggle", "roboflow", "dotenv", "tqdm", "requests"]
    for pkg in required:
        try:
            __import__(pkg.replace("-", "_"))
        except ImportError:
            print(f"\n[INFO] Installing missing package: {pkg}")
            run([sys.executable, "-m", "pip", "install", pkg, "--quiet"])

    step1_kaggle()
    step2_roboflow()
    step3_synthetic_generator()
    step4_verify()

    print("\n" + "=" * 60)
    print("Done. Next step: python scripts/preprocess.py")
    print("=" * 60)


if __name__ == "__main__":
    main()
