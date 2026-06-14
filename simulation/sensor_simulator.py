import random
import pandas as pd
from datetime import datetime

BIN_HEIGHT = 100

def generate_reading():

    distance = random.randint(5,100)

    fill_percentage = (
        (BIN_HEIGHT-distance)/BIN_HEIGHT
    )*100

    if fill_percentage < 40:
        status = "EMPTY"

    elif fill_percentage < 80:
        status = "HALF FULL"

    else:
        status = "FULL"

    return {
        "timestamp": datetime.now(),
        "distance": distance,
        "fill_percentage":
        round(fill_percentage,2),
        "status": status
    }

if __name__ == "__main__":

    reading = generate_reading()

    print(reading)