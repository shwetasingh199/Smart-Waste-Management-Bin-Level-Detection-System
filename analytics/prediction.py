import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression


def predict_fill_level(df, bin_id):

    bin_df = df[
        df["bin_id"] == bin_id
    ]

    if len(bin_df) < 3:
        return "Insufficient Data"

    X = np.arange(
        len(bin_df)
    ).reshape(-1, 1)

    y = bin_df["fill_percentage"]

    model = LinearRegression()

    model.fit(X, y)

    prediction = model.predict(
        [[len(bin_df) + 5]]
    )[0]

    prediction = max(
        0,
        min(100, prediction)
    )

    return round(prediction, 2)