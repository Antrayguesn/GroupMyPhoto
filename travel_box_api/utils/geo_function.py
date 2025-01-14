from math import cos, asin, sqrt, pi


def DMStoDD(degrees, minutes, seconds, hemisphere):
    """ Convert DMS (Degrees, Minutes, Seconds) to DD (Decimal Degrees)."""
    dd = degrees + (minutes / 60) + (seconds / 3600)
    return -dd if hemisphere in ['S', 'W'] else dd


def distance(coord1, coord2):
    # https://en.wikipedia.org/wiki/Haversine_formula
    r = 6371  # km
    p = pi / 180

    lat1, lon1 = coord1
    lat2, lon2 = coord2

    a = 0.5 - cos((lat2 - lat1) * p) / 2 + cos(lat1 * p) * cos(lat2 * p) * (1 - cos((lon2 - lon1) * p)) / 2
    return 2 * r * asin(sqrt(a))
