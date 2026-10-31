
from src.retraining.trigger_rules import (
    evaluate_retraining_trigger,
)

from src.retraining.approval import deployment_decision


def test_warning_does_not_trigger_high_severity_retraining():
    result = evaluate_retraining_trigger({
        "status": "warning"
    })

    assert not result["recommended"]


def test_human_approval_required():
    result = deployment_decision(
        {"eligible": True},
        human_approved=False,
    )

    assert not result["deploy"]
