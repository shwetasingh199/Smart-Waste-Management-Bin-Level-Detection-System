import pandas as pd
import os

FILE = "data/waste_data.csv"


def save_records(records):

    df = pd.DataFrame(records)

    if os.path.exists(FILE):

        df.to_csv(
            FILE,
            mode="a",
            header=False,
            index=False
        )

    else:

        df.to_csv(
            FILE,
            index=False
        )