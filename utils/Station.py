from utils.constant.ParamConstant import ParamConstant


class Station:
    def __init__(self, id, oil_types: int = 3, tank_count: int = 4):
        self.id: int = id
        self.oil_types: int = oil_types
        self.remain: list[float] = [0.0 for _ in range(oil_types)]
        self.require_upper_bound: list[float] = [0.0 for _ in range(oil_types)]
        self.require_average: list[float] = [0.0 for _ in range(oil_types)]
        self.require_lower_bound: list[float] = [0.0 for _ in range(oil_types)]
        self.tank_count: int = tank_count
        self.extra_tank_oil: int = 0

    def addRemain(self, oil_type: int, amount: float) -> bool:
        if 0 < oil_type <= self.oil_types:
            self.remain[oil_type - 1] += amount
            return self.remain[oil_type - 1] - amount > 0
        else:
            raise IndexError("Oil type index out of range.")

    def setRequire(
        self,
        oil_type: int,
        average_require: float,
        upper_bound: float,
        lower_bound: float,
    ):
        if 0 < oil_type <= self.oil_types:
            self.require_average[oil_type - 1] = average_require
            self.require_upper_bound[oil_type - 1] = upper_bound
            self.require_lower_bound[oil_type - 1] = lower_bound
        else:
            raise IndexError("Oil type index out of range.")

    def getLatestTime(self, oil_type: int) -> list[float]:
        if self.id < 1:
            return [float("inf"), float("inf"), float("inf")]
        if 0 < oil_type <= self.oil_types:
            window = [0.0] * self.tank_count
            require_average = self.require_average[oil_type - 1]
            require_upper_bound = self.require_upper_bound[oil_type - 1]
            require_lower_bound = self.require_lower_bound[oil_type - 1]
            remain = self.remain[oil_type - 1]

            window[0] = 24.0 * min(1.0, remain / require_upper_bound)
            window[1] = 24.0 * min(1.0, remain / require_average)
            window[2] = 24.0 * min(1.0, remain / require_lower_bound)

            return window
        else:
            raise IndexError("Oil type index out of range.")

    def getEarliestTime(self, oil_type: int, vehicle_capacity: int) -> list[float]:
        if self.id < 1:
            return [0.0, 0.0, 0.0]
        if 0 < oil_type <= self.oil_types:
            window = [0.0] * self.tank_count
            require_average = self.require_average[oil_type - 1]
            require_upper_bound = self.require_upper_bound[oil_type - 1]
            require_lower_bound = self.require_lower_bound[oil_type - 1]
            remain = self.remain[oil_type - 1]
            residual = vehicle_capacity + remain - ParamConstant.TANK_CAPACITY

            window[0] = 24.0 * max(0.0, residual / require_upper_bound)
            window[1] = 24.0 * max(0.0, residual / require_average)
            window[2] = 24.0 * max(0.0, residual / require_lower_bound)

            return window
        else:
            raise IndexError("Oil type index out of range.")
