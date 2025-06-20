from enum import IntEnum


class ParamConstant(IntEnum):
    """
    Constant parameters used in the problem.
    """

    OIL_TYPES = 3  # Number of oil types
    TANK_COUNT = 4  # Number of tanks per station
    STATION_COUNT = 25  # Number of stations
    VEHICLE_COUNT = 40  # Number of vehicles
    TANK_CAPACITY = 30000  # Capacity of each tank in liters

    SMALL_VEHICLE_COUNT = 10  # Capacity of small vehicles in liters
    MID_VEHICLE_COUNT = 15  # Capacity of large vehicles in liters
    LARGE_VEHICLE_COUNT = 15  # Capacity of large vehicles in liters

    SMALL_VEHICLE_CAPACITY = 10000  # Capacity of small vehicles in liters
    MID_VEHICLE_CAPACITY = 12000  # Capacity of mid vehicles in liters
    LARGE_VEHICLE_CAPACITY = 14000  # Capacity of large vehicles in liters

    SMALL_VEHICLE_VELOCITY = 60  # Velocity of small vehicles in km/h
    MID_VEHICLE_VELOCITY = 60  # Velocity of mid vehicles in km/h
    LARGo_VEHICLE_VELOCITY = 55  # Velocity of large vehicles in km/h

    INFINITY_COST = 10_000
