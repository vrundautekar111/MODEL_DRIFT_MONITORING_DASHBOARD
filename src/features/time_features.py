
import pandas as pd


def add_calendar_features(df):
    frame = df.copy()

    frame["date"] = pd.to_datetime(frame["date"])
    frame["day_of_week"] = frame["date"].dt.dayofweek
    frame["is_weekend"] = (
        frame["day_of_week"] >= 5
    ).astype(int)

    return frame
