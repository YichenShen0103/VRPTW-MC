from enum import StrEnum


class ColumnNameConstant(StrEnum):
    """
    This class contains constants for column names used in the application.
    """

    # Column names for 加油站库存 sheet
    COL_STATION_ID = "加油站编码"
    COL_REMAIN = "库存（升）"
    COL_OIL_ID = "油品编码"
    COL_REQUIRE_AVERAGE = "最可能需求量（升）"
    COL_REQUIRE_UPPER_BOUND = "需求量上限（升）"
    COL_REQUIRE_LOWER_BOUND = "需求量下限（升）"
    COL_STATION_ID_1 = "加油站1编码"
    COL_STATION_ID_2 = "加油站2编码"
    COL_DISTANCE = "运距"
    COL_DEPOT_ID = "油库编码"
    COL_VEHICLE_CAPACITY = "车仓1（升）"
    COL_VEHICLE_ID = "编码"
    COL_VEHICLE_VELOCITY = "车速（km/hr）"
    COL_VEHICLE_COST = "单位距离运输成本"
