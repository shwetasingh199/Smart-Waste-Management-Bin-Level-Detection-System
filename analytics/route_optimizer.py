import pandas as pd


def optimize_route(df):

    latest = (
        df.sort_values("timestamp")
        .groupby("bin_id")
        .tail(1)
    )

    return latest.sort_values(
        by="fill_percentage",
        ascending=False
    )