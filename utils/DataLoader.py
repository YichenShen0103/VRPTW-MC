import pandas as pd
import os

from utils.constant.SheetNameConstant import SheetNameConstant
from utils.constant.ColumnNameConstant import ColumnNameConstant
from utils.Station import Station
from utils.Vehicle import Vehicle
from utils.Task import Task


class DataLoader:
    def __init__(self, data_root: str, oil_types: int = 3, tank_count: int = 4):
        self.data_path = os.path.join(data_root, "data_v2.0.xlsx")
        self.dfs = pd.read_excel(self.data_path, sheet_name=None)
        self.stations = self.__loadStations()
        self.station_count = len(self.stations)
        self.oil_types = oil_types
        self.tank_count = tank_count

    def __loadStations(self) -> dict[int, Station]:
        remain_df = self.__getDataFrame(SheetNameConstant.SHEET_REMAIN)
        requiry_df = self.__getDataFrame(SheetNameConstant.SHEET_REQUIRY)
        stations: dict[int, Station] = {}

        for _, row in remain_df.iterrows():
            station_id = row[ColumnNameConstant.COL_STATION_ID] % 100
            oil_type = row[ColumnNameConstant.COL_OIL_ID] % 10

            if station_id not in stations:
                stations[station_id] = Station(id=station_id)

            if stations[station_id].addRemain(
                oil_type, row[ColumnNameConstant.COL_REMAIN]
            ):
                stations[station_id].extra_tank_oil = oil_type

        for _, row in requiry_df.iterrows():
            station_id = row[ColumnNameConstant.COL_STATION_ID] % 100
            oil_type = row[ColumnNameConstant.COL_OIL_ID] % 10

            if station_id not in stations:
                stations[station_id] = Station(id=station_id)

            stations[station_id].setRequire(
                oil_type,
                row[ColumnNameConstant.COL_REQUIRE_AVERAGE],
                row[ColumnNameConstant.COL_REQUIRE_UPPER_BOUND],
                row[ColumnNameConstant.COL_REQUIRE_LOWER_BOUND],
            )

        return stations

    def __getDataFrame(self, sheet_name: str) -> pd.DataFrame:
        if sheet_name not in self.dfs:
            raise ValueError(f"Sheet '{sheet_name}' not found in the Excel file.")
        return self.dfs[sheet_name]

    def getDistanceMatrix(self) -> list[list[float]]:
        ss_distance_df = self.__getDataFrame(
            SheetNameConstant.SHEET_STATION_STATION_DISTANCE
        )
        ds_distance_df = self.__getDataFrame(
            SheetNameConstant.SHEET_DEPOT_STATION_DISTANCE
        )
        distance_matrix: list[list[float]] = [
            [float("inf") for _ in range(self.station_count + 2)]
            for _ in range(self.station_count + 2)
        ]

        for _, row in ss_distance_df.iterrows():
            station_id_1 = row[ColumnNameConstant.COL_STATION_ID_1] % 100 + 1
            station_id_2 = row[ColumnNameConstant.COL_STATION_ID_2] % 100 + 1
            distance_matrix[station_id_2][station_id_1] = distance_matrix[station_id_1][
                station_id_2
            ] = row[ColumnNameConstant.COL_DISTANCE]

        for _, row in ds_distance_df.iterrows():
            depot_id = row[ColumnNameConstant.COL_DEPOT_ID] % 100 - 1
            station_id = row[ColumnNameConstant.COL_STATION_ID] % 100 + 1
            distance_matrix[depot_id][station_id] = distance_matrix[station_id][
                depot_id
            ] = row[ColumnNameConstant.COL_DISTANCE]

        return distance_matrix

    def getVehicles(self) -> list[Vehicle]:
        """
        获取所有车辆（油库）。
        :return: 车辆列表。
        """
        vehicle_df = self.__getDataFrame(SheetNameConstant.SHEET_VEHICLE)
        vehicles: list[Vehicle] = []

        for _, row in vehicle_df.iterrows():
            vehicle_id = row[ColumnNameConstant.COL_VEHICLE_ID] % 100 - 1
            capacity = row[ColumnNameConstant.COL_VEHICLE_CAPACITY]
            velocity = row[ColumnNameConstant.COL_VEHICLE_VELOCITY]
            cost = row[ColumnNameConstant.COL_VEHICLE_COST]

            vehicles.append(Vehicle(vehicle_id, capacity, velocity, cost))

        return vehicles

    def getTasks(self) -> list[Task]:
        """
        获取所有任务（加油站）。
        :return: 任务列表。
        """
        tasks: list[Task] = []
        require_df = self.__getDataFrame(SheetNameConstant.SHEET_REQUIRY)

        for _, row in require_df.iterrows():
            station_id = row[ColumnNameConstant.COL_STATION_ID] % 100
            oil_type = row[ColumnNameConstant.COL_OIL_ID] % 10

            if station_id not in self.stations:
                continue

            station = self.stations[station_id]
            task = Task(
                station=station,
                oil_type=oil_type,
            )
            tasks.append(task)

        return tasks
