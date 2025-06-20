from itertools import permutations
from utils.Task import Task
from utils.Station import Station

from utils.constant.ParamConstant import ParamConstant


class Vehicle:
    def __init__(self, id: int, capacity: int, velocity: float, cost: float):
        self.id: int = id
        self.capacity: int = capacity
        self.velocity: float = velocity
        self.cost: float = cost
        self.tasks: list[Task] = []

    def addTask(self, task: Task):
        self.tasks.append(task)

    def plan(self, distance_matrix: list[list[float]]) -> float:
        task_count = len(self.tasks)
        if task_count > 4:
            return ParamConstant.INFINITY_COST  # 超过4个任务不处理
        if task_count == 0:
            return 0.0
        total_cost: float = ParamConstant.INFINITY_COST
        best_order: list[Task] = []

        def route_available(tasks: list[Task]) -> bool:
            if len(tasks) < 2:
                return True

            p: int = 0
            current_time: float = 0.0
            current_location: int = 0

            while p < len(tasks):
                task = tasks[p]
                destination = task.station.id + 1

                if current_location == destination:
                    p += 1
                    continue

                if distance_matrix[current_location][destination] == float("inf"):
                    return False

                travel_time = (
                    distance_matrix[current_location][destination] / self.velocity
                )
                current_time += travel_time
                current_location = destination

                if current_time > max(task.station.getLatestTime(task.oil_type)):
                    return False

                if current_time > 9.0:  # 超过下午5点
                    return False

                earliest = min(
                    task.station.getEarliestTime(task.oil_type, self.capacity)
                )
                if current_time < earliest:
                    current_time = earliest

                if task.station.id >= 2:  # 不是油库
                    current_time += 0.5

                p += 1

            return True

        def calculate_cost(task_sequence: list[Task]) -> float:
            cost = 0.0
            current_location = 0  # 起点为油库A，编号0
            for task in task_sequence:
                destination = task.station.id + 1
                if current_location != destination:
                    d = distance_matrix[current_location][destination]
                    cost += d * self.cost
                    current_location = destination
            # 回到油库A（编号0）
            cost += distance_matrix[current_location][0] * self.cost
            return cost

        # 遍历所有任务顺序排列
        virtual_task_a = Task(Station(-1), 0)  # 油库A
        virtual_task_b = Task(Station(0), 0)  # 油库B
        for perm in permutations(self.tasks):
            perms = []

            # 中转逻辑，以中转点为虚拟任务
            if task_count == 4:
                perms.append(list(perm)[:2] + [virtual_task_a] + list(perm)[2:])
                perms.append(list(perm)[:2] + [virtual_task_b] + list(perm)[2:])
            elif task_count == 3:
                perms.append(list(perm)[:1] + [virtual_task_a] + list(perm)[1:])
                perms.append(list(perm)[:1] + [virtual_task_b] + list(perm)[1:])
                perms.append(list(perm)[:2] + [virtual_task_a] + list(perm)[2:])
                perms.append(list(perm)[:2] + [virtual_task_b] + list(perm)[2:])
            elif task_count == 2:
                perms.append(list(perm))
                perms.append(list(perm)[:1] + [virtual_task_a] + list(perm)[1:])
                perms.append(list(perm)[:1] + [virtual_task_b] + list(perm)[1:])
            elif task_count == 1:
                perms.append(list(perm))

            for perm in perms:
                if route_available(list(perm)):
                    cost = calculate_cost(list(perm))
                    if cost < total_cost:
                        total_cost = cost
                        best_order = list(perm)

        # 可以选填保存最佳任务顺序用于调度
        self.tasks = best_order

        return (
            total_cost
            if total_cost < ParamConstant.INFINITY_COST
            else ParamConstant.INFINITY_COST
        )
