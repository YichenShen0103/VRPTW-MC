from utils.DataLoader import DataLoader
from utils.constant.HyperParamConstant import HyperParamConstant
from collections import Counter
from src.GenericAlgorithm import GeneticAlgorithm
from utils.Task import Task

from utils.DataLoader import DataLoader


def get_cost_from_matrix(solution: list[int], data_loader: DataLoader):
    """
    根据给定的解和数据加载器计算代价。
    :param solution: 解，表示每个任务谁来做。
    :param data_loader: 数据加载器，用于获取距离矩阵。
    :return: 计算得到的代价。
    """
    distance_matrix = data_loader.getDistanceMatrix()
    total_cost = 0.0

    vehicles = data_loader.getVehicles()
    tasks = data_loader.getTasks()

    for i in range(len(solution)):
        vehicles[int(solution[i])].addTask(tasks[i])

    for vehicle in vehicles:
        cost = vehicle.plan(distance_matrix)
        total_cost += cost

    return total_cost, vehicles


def solve(dataLoader: DataLoader):
    # 初始化并运行算法
    ga = GeneticAlgorithm(
        cost_function=get_cost_from_matrix,
        num_tasks=HyperParamConstant.NUM_TASKS.value,
        num_people=HyperParamConstant.NUM_PEOPLE.value,
        max_tasks_per_person=HyperParamConstant.MAX_TASKS_PER_PERSON.value,
        population_size=HyperParamConstant.POPULATION_SIZE.value,
        num_generations=HyperParamConstant.NUM_GENERATIONS.value,
        crossover_rate=HyperParamConstant.CROSSOVER_RATE.value,
        mutation_rate=HyperParamConstant.MUTATION_RATE.value,
        tournament_size=HyperParamConstant.TOURNAMENT_SIZE.value,
        elitism_rate=HyperParamConstant.ELITISM_RATE.value,
        initial_max_tasks_per_person=HyperParamConstant.INITIAL_MAX_TASKS_PER_PERSON.value,
        dataLoader=dataLoader,
    )

    best_solution, best_cost = ga.run()
    _, vehicles = get_cost_from_matrix(best_solution, dataLoader)

    # 打印最终结果
    print(f"\n找到的最优代价: {best_cost:.2f}")

    # 验证最终解的有效性
    final_counts = Counter(best_solution)
    print("\n最优解中每辆车的任务数量 (只显示有任务的车):")
    for vehicle_id, count in sorted(final_counts.items()):
        print(f"  车辆 {vehicle_id}: {count} 个任务, 任务顺序: ", end="")
        best_order: list[Task] = vehicles[vehicle_id].tasks
        for task in best_order:
            station_id: str = (
                str(task.station.id)
                if task.station.id >= 1
                else chr(ord("A") + task.station.id + 1)
            )
            print(station_id + f" (油种: {task.oil_type})", end=" ")
        print()

    is_valid = all(
        count <= HyperParamConstant.MAX_TASKS_PER_PERSON.value
        for count in final_counts.values()
    )
    print(f"\n最终解是否满足约束? {'是' if is_valid else '否'}")
