
import numpy as np
import pandas as pd


def psi(reference, current, bins=10):
    """
    Population Stability Index (PSI).

    Typical heuristic:
      PSI < 0.10: relatively stable
      0.10-0.25: investigate
      >= 0.25: substantial distribution shift

    These thresholds must be calibrated for the business.
    """
    ref = pd.to_numeric(
        pd.Series(reference), errors="coerce"
    ).dropna().to_numpy()

    cur = pd.to_numeric(
        pd.Series(current), errors="coerce"
    ).dropna().to_numpy()

    if len(ref) < 10 or len(cur) < 10:
        return None

    edges = np.unique(
        np.quantile(
            ref,
            np.linspace(0, 1, bins + 1),
        )
    )

    if len(edges) < 3:
        return 0.0

    edges[0] = -np.inf
    edges[-1] = np.inf

    ref_counts, _ = np.histogram(ref, bins=edges)
    cur_counts, _ = np.histogram(cur, bins=edges)

    ref_pct = np.clip(
        ref_counts / max(ref_counts.sum(), 1),
        1e-4,
        None,
    )

    cur_pct = np.clip(
        cur_counts / max(cur_counts.sum(), 1),
        1e-4,
        None,
    )

    return float(
        np.sum(
            (cur_pct - ref_pct)
            * np.log(cur_pct / ref_pct)
        )
    )


def detect_drift(
    reference: pd.DataFrame,
    current: pd.DataFrame,
):
    results = []

    for column in reference.columns:
        if column not in current.columns:
            results.append({
                "feature": column,
                "score": None,
                "method": "schema",
                "status": "critical",
                "message": "Feature missing",
            })
            continue

        if pd.api.types.is_numeric_dtype(
            reference[column]
        ):
            score = psi(
                reference[column],
                current[column],
            )

            if score is None:
                status = "insufficient_data"
            elif score >= 0.25:
                status = "drift"
            elif score >= 0.10:
                status = "warning"
            else:
                status = "stable"

            results.append({
                "feature": column,
                "score": score,
                "method": "PSI",
                "status": status,
            })

        else:
            ref = (
                reference[column]
                .fillna("MISSING")
                .astype(str)
            )

            cur = (
                current[column]
                .fillna("MISSING")
                .astype(str)
            )

            categories = (
                set(ref.unique()) | set(cur.unique())
            )

            ref_pct = ref.value_counts(
                normalize=True
            )

            cur_pct = cur.value_counts(
                normalize=True
            )

            score = float(
                sum(
                    abs(
                        ref_pct.get(category, 0)
                        - cur_pct.get(category, 0)
                    )
                    for category in categories
                ) / 2
            )

            if score >= 0.25:
                status = "drift"
            elif score >= 0.10:
                status = "warning"
            else:
                status = "stable"

            results.append({
                "feature": column,
                "score": score,
                "method": "categorical total variation",
                "status": status,
            })

    return results
