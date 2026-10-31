
from datetime import datetime, timezone


def create_incident(alert):
    return {
        "created_at": datetime.now(
            timezone.utc
        ).isoformat(),
        "status": "open",
        **alert,
    }
