
import json

from database.connection import connect


def save_prediction(record):
    with connect() as conn:
        cursor = conn.execute(
            """
            INSERT INTO predictions(
                target_date,
                product_id,
                store_id,
                predicted_units,
                model_version
            )
            VALUES (?, ?, ?, ?, ?)
            """,
            (
                record["target_date"],
                record["product_id"],
                record["store_id"],
                record["predicted_units"],
                record.get("model_version", "local-v1"),
            ),
        )

        return cursor.lastrowid


def add_actual(
    target_date,
    product_id,
    store_id,
    actual_units,
):
    with connect() as conn:
        cursor = conn.execute(
            """
            UPDATE predictions
            SET actual_units = ?
            WHERE target_date = ?
              AND product_id = ?
              AND store_id = ?
            """,
            (
                actual_units,
                target_date,
                product_id,
                store_id,
            ),
        )

        return cursor.rowcount


def get_labeled_predictions():
    with connect() as conn:
        rows = conn.execute(
            """
            SELECT predicted_units, actual_units
            FROM predictions
            WHERE actual_units IS NOT NULL
            """
        ).fetchall()

        return [dict(row) for row in rows]


def save_monitoring(result):
    with connect() as conn:
        cursor = conn.execute(
            """
            INSERT INTO monitoring_runs(status, result_json)
            VALUES (?, ?)
            """,
            (
                result["status"],
                json.dumps(result),
            ),
        )

        run_id = cursor.lastrowid

        for alert in result.get("alerts", []):
            conn.execute(
                """
                INSERT INTO alerts(severity, title, details)
                VALUES (?, ?, ?)
                """,
                (
                    alert["severity"],
                    alert["title"],
                    alert.get("details", ""),
                ),
            )

        return run_id


def list_monitoring(limit=20):
    with connect() as conn:
        rows = conn.execute(
            """
            SELECT id, created_at, status, result_json
            FROM monitoring_runs
            ORDER BY id DESC
            LIMIT ?
            """,
            (limit,),
        ).fetchall()

        return [
            {
                "id": row["id"],
                "created_at": row["created_at"],
                "status": row["status"],
                "result": json.loads(row["result_json"]),
            }
            for row in rows
        ]


def list_alerts(limit=100):
    with connect() as conn:
        rows = conn.execute(
            """
            SELECT *
            FROM alerts
            ORDER BY id DESC
            LIMIT ?
            """,
            (limit,),
        ).fetchall()

        return [dict(row) for row in rows]


def resolve_alert(alert_id):
    with connect() as conn:
        cursor = conn.execute(
            """
            UPDATE alerts
            SET status = 'resolved'
            WHERE id = ?
            """,
            (alert_id,),
        )

        return cursor.rowcount


def get_prediction_summary():
    with connect() as conn:
        row = conn.execute(
            """
            SELECT
                COUNT(*) AS n,
                AVG(predicted_units) AS avg_pred,
                SUM(
                    CASE
                        WHEN actual_units IS NOT NULL THEN 1
                        ELSE 0
                    END
                ) AS labeled
            FROM predictions
            """
        ).fetchone()

        return dict(row)
