import random
from datetime import datetime

BIN_LOCATIONS = {
    "B1": "Library",
    "B2": "Hostel",
    "B3": "Cafeteria",
    "B4": "Parking",
    "B5": "Academic Block"
}

BIN_HEIGHT = 100


def generate_bin_data():

    records = []

    for bin_id, location in BIN_LOCATIONS.items():

        distance = random.randint(5, 100)

        fill_percentage = (
            (BIN_HEIGHT - distance)
            / BIN_HEIGHT
        ) * 100

        if fill_percentage < 40:
            status = "EMPTY"

        elif fill_percentage < 80:
            status = "HALF FULL"

        else:
            status = "FULL"

        records.append({
            "timestamp": datetime.now(),
            "bin_id": bin_id,
            "location": location,
            "distance": distance,
            "fill_percentage":
                round(fill_percentage, 2),
            "status": status
        })

    return records