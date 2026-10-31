
from fastapi import APIRouter, HTTPException

from src.retraining.candidate_training import train_candidate
from src.retraining.model_comparison import compare_metrics
from src.models.predict import load_model

router = APIRouter(
    prefix="/retraining",
    tags=["Retraining"],
)


@router.post("/evaluate")
def evaluate_candidate():
    try:
        current = load_model()
        candidate = train_candidate()

        comparison = compare_metrics(
            current.get("metrics", {}),
            candidate["metrics"],
        )

        return {
            "candidate": candidate,
            "comparison": comparison,
            "promoted": False,
            "message": (
                "Candidate evaluated only. "
                "The active model was not replaced."
            ),
        }

    except Exception as exc:
        raise HTTPException(
            status_code=400,
            detail=str(exc),
        )
