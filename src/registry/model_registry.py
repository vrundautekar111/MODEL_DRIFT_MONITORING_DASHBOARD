
import json

from src.common.config import ROOT_DIR

REGISTRY_PATH = (
    ROOT_DIR / "artifacts/reports/model_registry.json"
)


def list_versions():
    if not REGISTRY_PATH.exists():
        return [{
            "version": "local-v1",
            "status": "production",
            "artifact": "artifacts/models/sales_model.joblib",
        }]

    return json.loads(
        REGISTRY_PATH.read_text(encoding="utf-8")
    )


def record_version(version, status, artifact, metrics):
    versions = list_versions()

    versions.append({
        "version": version,
        "status": status,
        "artifact": str(artifact),
        "metrics": metrics,
    })

    REGISTRY_PATH.parent.mkdir(
        parents=True, exist_ok=True
    )

    REGISTRY_PATH.write_text(
        json.dumps(versions, indent=2),
        encoding="utf-8",
    )

    return versions
