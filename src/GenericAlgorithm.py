import numpy as np
from collections import Counter
import time
import random
from tqdm import tqdm


class GeneticAlgorithm:
    """
    用于解决复杂任务分配问题的遗传算法。
    (已加入针对稀疏图的启发式初始化功能)
    """

    def __init__(
        self,
        cost_function,
        num_tasks,
        num_people,
        max_tasks_per_person,
        population_size=100,
        num_generations=500,
        crossover_rate=0.8,
        mutation_rate=0.02,
        tournament_size=5,
        elitism_rate=0.1,
        dataLoader=None,
        initial_max_tasks_per_person=None,  # <--- NEW: 新增参数，用于启发式初始化
    ):

        self.cost_function = cost_function
        self.num_tasks = num_tasks
        self.num_people = num_people
        self.max_tasks_per_person = max_tasks_per_person

        # --- MODIFIED BLOCK START ---
        # 接受并设置初始化的特殊限制
        # 如果未提供，则默认为最终的硬限制
        self.initial_max_tasks = (
            initial_max_tasks_per_person
            if initial_max_tasks_per_person is not None
            else self.max_tasks_per_person
        )

        # 检查初始限制是否可行，防止无法分配所有任务
        if self.num_people * self.initial_max_tasks < self.num_tasks:
            raise ValueError(
                f"初始任务限制过严 ({self.initial_max_tasks})，"
                f"无法为所有 {self.num_tasks} 个任务找到分配!"
            )
        # --- MODIFIED BLOCK END ---

        self.population_size = population_size
        self.num_generations = num_generations
        self.crossover_rate = crossover_rate
        self.mutation_rate = mutation_rate
        self.tournament_size = tournament_size
        self.elitism_count = int(population_size * elitism_rate)
        self.dataLoader = dataLoader

        self.population = []
        self.fitness_cache = {}

    def _chromosome_to_matrix(self, chromosome):
        """将列表形式的染色体转换为矩阵形式。(保留此方法以备调试)"""
        matrix = np.zeros((self.num_people, self.num_tasks), dtype=int)
        for task_id, person_id in enumerate(chromosome):
            matrix[person_id, task_id] = 1
        return matrix

    def _repair_chromosome(self, chromosome):
        """
        修复不满足最终硬约束的染色体 (保证每个人任务数 <= max_tasks_per_person)。
        此函数逻辑保持不变，因为它处理的是进化过程中产生的后代。
        """
        task_counts = Counter(chromosome)

        while True:
            overloaded_people = {
                p: c for p, c in task_counts.items() if c > self.max_tasks_per_person
            }
            if not overloaded_people:
                break

            person_to_fix = random.choice(list(overloaded_people.keys()))
            available_people = [
                p
                for p in range(self.num_people)
                if task_counts.get(p, 0) < self.max_tasks_per_person
            ]
            if not available_people:
                raise RuntimeError("无法修复染色体，没有可用的接收人员！")

            receiver = random.choice(available_people)
            tasks_of_fixer = [i for i, p in enumerate(chromosome) if p == person_to_fix]
            task_to_move = random.choice(tasks_of_fixer)
            chromosome[task_to_move] = receiver
            task_counts[person_to_fix] -= 1
            task_counts[receiver] = task_counts.get(receiver, 0) + 1

        return chromosome

    # --- METHOD REPLACED ---
    def _create_individual(self):
        """
        创建一个随机个体，但满足初始化的特殊限制 (initial_max_tasks)。
        这是一个启发式的初始化，旨在为稀疏图问题提供更好的起点。
        """
        # 1. 创建所有可用的“任务槽位”
        # 例如，40个人，每人最多2个任务，则有 [0,0, 1,1, ..., 39,39]
        slots = []
        for person_id in range(self.num_people):
            slots.extend([person_id] * self.initial_max_tasks)

        # 2. 随机打乱所有槽位
        random.shuffle(slots)

        # 3. 从打乱的槽位中为每个任务分配一个负责人
        # 由于 self.num_people * self.initial_max_tasks >= self.num_tasks,
        # 所以 slots 列表的长度肯定足够
        chromosome = slots[: self.num_tasks]

        # 4. 再次打乱染色体，确保任务到人员的分配是随机的
        # （否则任务0,1会倾向于分配给同一个人, 打乱后则完全随机）
        random.shuffle(chromosome)

        return chromosome

    def _calculate_fitness(self, chromosome):
        """计算个体的适应度，并使用缓存避免重复计算。(您的版本)"""
        chromo_tuple = tuple(chromosome)
        if chromo_tuple in self.fitness_cache:
            return self.fitness_cache[chromo_tuple]

        cost, _ = self.cost_function(chromosome, self.dataLoader)

        fitness = -cost
        self.fitness_cache[chromo_tuple] = fitness
        return fitness

    def _selection(self, population_with_fitness):
        """锦标赛选择。"""
        tournament = random.sample(population_with_fitness, self.tournament_size)
        tournament.sort(key=lambda x: x[1], reverse=True)
        return tournament[0][0]

    def _crossover(self, parent1, parent2):
        """单点交叉。"""
        if random.random() < self.crossover_rate:
            # 确保交叉点不会在列表的两端
            if self.num_tasks > 2:
                point = random.randint(1, self.num_tasks - 2)
                child1 = parent1[:point] + parent2[point:]
                child2 = parent2[:point] + parent1[point:]
                return child1, child2
        return parent1, parent2

    def _mutate(self, chromosome):
        """变异操作。"""
        mutated_chromosome = list(chromosome)
        for i in range(self.num_tasks):
            if random.random() < self.mutation_rate:
                mutated_chromosome[i] = random.randint(0, self.num_people - 1)
        return mutated_chromosome

    def run(self):
        """执行遗传算法的主循环。"""
        print("--- 开始遗传算法 (已启用稀疏图优化初始化) ---")  # <--- MODIFIED
        start_time = time.time()

        # 1. 初始化种群
        print(
            f"正在创建初始种群 (每人最多 {self.initial_max_tasks} 个任务)..."
        )  # <--- MODIFIED
        self.population = [
            self._create_individual() for _ in range(self.population_size)
        ]

        best_overall_chromosome = list()
        best_overall_fitness = -float("inf")

        # 2. 迭代指定的代数 (使用您的tqdm)
        for generation in tqdm(range(self.num_generations), desc="遗传算法迭代"):
            pop_with_fitness = [
                (ind, self._calculate_fitness(ind)) for ind in self.population
            ]

            current_best_chromosome, current_best_fitness = max(
                pop_with_fitness, key=lambda x: x[1]
            )

            if current_best_fitness > best_overall_fitness:
                best_overall_fitness = current_best_fitness
                best_overall_chromosome = current_best_chromosome

            if (generation + 1) % 50 == 0 or generation == 0:
                tqdm.write(
                    f"代 {generation+1:>4}: 当前最优代价 = {-best_overall_fitness:.2f}"
                )

            # 3. 创建下一代种群
            next_generation = []
            pop_with_fitness.sort(key=lambda x: x[1], reverse=True)
            elites = [item[0] for item in pop_with_fitness[: self.elitism_count]]
            next_generation.extend(elites)

            while len(next_generation) < self.population_size:
                parent1 = self._selection(pop_with_fitness)
                parent2 = self._selection(pop_with_fitness)
                child1, child2 = self._crossover(parent1, parent2)
                child1 = self._mutate(child1)
                # 修复时使用的是最终硬约束 self.max_tasks_per_person
                child1 = self._repair_chromosome(child1)
                next_generation.append(child1)

            self.population = next_generation[: self.population_size]

        end_time = time.time()
        print("\n--- 遗传算法结束 ---")
        print(f"总耗时: {end_time - start_time:.2f} 秒")

        final_cost = -best_overall_fitness
        return best_overall_chromosome, final_cost
