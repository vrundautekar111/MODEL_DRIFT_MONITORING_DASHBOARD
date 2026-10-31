
def deployment_decision(
    comparison,
    data_quality_ok=True,
    human_approved=False,
):
    if not data_quality_ok:
        return {
            "deploy": False,
            "reason": "Data quality gate failed",
        }

    if not comparison.get("eligible"):
        return {
            "deploy": False,
            "reason": comparison.get(
                "reason",
                "Model comparison failed",
            ),
        }

    if not human_approved:
        return {
            "deploy": False,
            "reason": "Awaiting explicit human approval",
        }

    return {
        "deploy": True,
        "reason": "Evaluation gates passed and approval recorded",
    }
