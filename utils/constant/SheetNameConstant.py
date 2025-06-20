from enum import StrEnum


class SheetNameConstant(StrEnum):
    """
    This class contains constants for sheet names used in the application.
    """

    # Sheet names
    SHEET_REQUIRY = "加油站需求量"
    SHEET_DEPOT = "油库信息"
    SHEET_VEHICLE = "油罐车信息"
    SHEET_STATION = "加油站信息"
    SHEET_OIL = "油品信息"
    SHEET_REMAIN = "加油站库存"
    SHEET_STORAGE = "油库库存"
    SHEET_DEPOT_STATION_DISTANCE = "库站运距"
    SHEET_STATION_STATION_DISTANCE = "站站运距"
