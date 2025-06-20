from utils.Station import Station


class Task:
    def __init__(self, station: Station, oil_type: int):
        self.station = station
        self.oil_type = oil_type
        self.latest_time = station.getLatestTime(oil_type)

    def getEarliestTime(self, vehicle_capacity: int) -> list[float]:
        return self.station.getEarliestTime(self.oil_type, vehicle_capacity)
