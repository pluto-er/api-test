from math import radians, cos, sin, asin, sqrt


class GetGeo:

    def geodistance(self, lng1, lat1, lng2, lat2):
        lng1, lat1, lng2, lat2 = map(radians, [float(lng1), float(lat1), float(lng2), float(lat2)])
        dlon = lng2 - lng1
        dlat = lat2 - lat1
        a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
        distance = 2 * asin(sqrt(a)) * 6371 * 1000
        distance = round(distance / 1000, 3)
        return distance


if __name__ == '__main__':
    run = GetGeo()
    ret = run.geodistance("120.12802999999997", "30.28708", "115.86572000000001", "28.7427")
