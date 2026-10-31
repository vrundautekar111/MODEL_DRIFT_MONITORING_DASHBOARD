
from fastapi import APIRouter

from src.common.config import MODEL_PATH
from src.models.predict import load_model
from src.registry.model_registry import list_versions

router = APIRouter(
    prefix="/models",
    tags=["Models"],
)


@router.get("")
def model_status():
    bundle = load_model()

    return {
        "active_model": bundle.get(
            "version", "local-v1"
        ),
        "artifact_exists": MODEL_PATH.exists(),
        "metrics": bundle.get("metrics", {}),
        "versions": list_versions(),
    }
