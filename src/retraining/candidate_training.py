
import json

from src.common.config import ROOT_DIR
from src.models.train import train_model


def train_candidate():
    candidate_path = (
        ROOT_DIR
        / "artifacts/models/candidate_sales_model.joblib"
    )

    metrics = train_model(
        model_path=candidate_path
    )

    report = {
        "candidate_path": str(candidate_path),
        "metrics": metrics,
        "status": "candidate_trained_not_promoted",
    }

    report_path = (
        ROOT_DIR
        / "artifacts/reports/candidate_evaluation.json"
    )

    report_path.parent.mkdir(
        parents=True, exist_ok=True
    )

    report_path.write_text(
        json.dumps(report, indent=2),
        encoding="utf-8",
    )

    return report
