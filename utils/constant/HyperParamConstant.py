from enum import Enum


class HyperParamConstant(Enum):
    # 问题参数
    NUM_TASKS = 75
    NUM_PEOPLE = 40
    MAX_TASKS_PER_PERSON = 4

    # GA 超参数
    POPULATION_SIZE = 200
    NUM_GENERATIONS = 10_000
    CROSSOVER_RATE = 0.8
    MUTATION_RATE = 0.03  # 变异率可以调高一些以增加多样性
    TOURNAMENT_SIZE = 5
    ELITISM_RATE = 0.1
    INITIAL_MAX_TASKS_PER_PERSON = 2
