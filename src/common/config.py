
import os
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parents[2]

DATA_PATH = Path(
    os.getenv(
        "SALESGUARD_DATA_PATH",
        str(ROOT_DIR / "data/sample/sales_sample.csv")
    )
)

MODEL_PATH = Path(
    os.getenv(
        "SALESGUARD_MODEL_PATH",
        str(ROOT_DIR / "artifacts/models/sales_model.joblib")
    )
)

DB_PATH = Path(
    os.getenv(
        "SALESGUARD_DB_PATH",
        str(ROOT_DIR / "artifacts/salesguard.db")
    )
)

REFERENCE_PATH = ROOT_DIR / "data/reference/reference_features.csv"
REPORT_PATH = ROOT_DIR / "artifacts/reports"
