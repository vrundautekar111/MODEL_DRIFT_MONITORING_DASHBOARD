
def build_alerts(monitoring_result):
    alerts = []

    for issue in monitoring_result.get(
        "quality", {}
    ).get("issues", []):
        alerts.append({
            "severity": issue["severity"],
            "title": issue["issue"],
            "details": issue["details"],
        })

    for item in monitoring_result.get("drift", []):
        if item.get("status") in {
            "warning", "drift", "critical"
        }:
            alerts.append({
                "severity": (
                    "critical"
                    if item["status"] in {"drift", "critical"}
                    else "warning"
                ),
                "title": (
                    f"Feature drift: {item['feature']}"
                ),
                "details": (
                    f"{item.get('method')} "
                    f"score={item.get('score')}"
                ),
            })

    return alerts
