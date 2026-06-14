from simulation.multi_bin_simulator import generate_bin_data

import pandas as pd
import os
import time

FILE = "data/waste_data.csv"

for _ in range(10):

    records = generate_bin_data()

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

    print("New waste data recorded")

    time.sleep(5)
print("Simulation Completed")    