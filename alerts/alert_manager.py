def generate_alert(fill_percentage):

    if fill_percentage >= 90:
        return "CRITICAL"

    elif fill_percentage >= 80:
        return "WARNING"

    return "NORMAL"