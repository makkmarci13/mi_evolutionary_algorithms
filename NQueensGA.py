import random


class NQueensGA:
    def __init__(
            self,
            n=8,  # Sakktábla mérete, királynők száma
            population_size=100,  # Ennyi megoldást vizsgálunk egyszerre
            generations=300,  # Ennyiszer fut le az evolúció
            crossover_rate=0.95,  # Ennyi %-os eséllyel keresztezzük a szülőket
            mutation_rate=0.30,  # Ennyi %-os eséllyel változtatunk random egy megoldásban
            elite_size=4,  # Ennyi megoldást őrzünk meg változtatás nélkül
            tournament_size=4  # Ennyi megoldást választ ki, majd ebből a legjobbat
    ):
        self.n = n
        self.population_size = population_size
        self.generations = generations
        self.crossover_rate = crossover_rate
        self.mutation_rate = mutation_rate
        self.elite_size = elite_size
        self.tournament_size = tournament_size
        self.max_fitness = n * (n - 1) // 2

        if self.elite_size >= self.population_size:
            raise ValueError("Az elite_size nem lehet nagyobb vagy egyenlő a population_size értékével.")
        if self.tournament_size > self.population_size:
            raise ValueError("A tournament_size nem lehet nagyobb a population_size értékénél.")

    def random_individual(self):
        individual = list(range(self.n))
        random.shuffle(individual)
        return individual

    def conflicts(self, individual):
        conflicts = 0
        for i in range(self.n):
            for j in range(i + 1, self.n):
                if individual[i] == individual[j]:
                    conflicts += 1
                elif abs(individual[i] - individual[j]) == abs(i - j):
                    conflicts += 1
        return conflicts

    def fitness(self, individual):
        return self.max_fitness - self.conflicts(individual)

    def tournament_selection(self, population, fitnesses):
        indices = random.sample(range(len(population)), self.tournament_size)
        best_index = max(indices, key=lambda i: fitnesses[i])
        return population[best_index][:]

    def order_crossover(self, parent1, parent2):
        a, b = sorted(random.sample(range(self.n), 2))

        child = [None] * self.n
        child[a:b + 1] = parent1[a:b + 1]

        remaining = [x for x in parent2 if x not in child]
        pointer = 0

        for i in list(range(0, a)) + list(range(b + 1, self.n)):
            child[i] = remaining[pointer]
            pointer += 1

        return child

    def mutate(self, individual):
        mutated = individual[:]
        if random.random() < self.mutation_rate:
            i, j = random.sample(range(self.n), 2)
            mutated[i], mutated[j] = mutated[j], mutated[i]
        return mutated

    def run(self, seed=None):
        if seed is not None:
            random.seed(seed)

        population = [self.random_individual() for _ in range(self.population_size)]

        best_solution = None
        best_fitness = -1
        best_generation = 0
        history = []

        for generation in range(self.generations + 1):
            fitnesses = [self.fitness(ind) for ind in population]

            generation_best = max(fitnesses)
            generation_avg = sum(fitnesses) / len(fitnesses)
            history.append((generation, generation_best, generation_avg))

            if generation_best > best_fitness:
                best_index = max(range(len(population)), key=lambda i: fitnesses[i])
                best_solution = population[best_index][:]
                best_fitness = generation_best
                best_generation = generation

            if best_fitness == self.max_fitness:
                break

            elite_indices = sorted(
                range(len(population)),
                key=lambda i: fitnesses[i],
                reverse=True
            )[:self.elite_size]

            new_population = [population[i][:] for i in elite_indices]

            while len(new_population) < self.population_size:
                parent1 = self.tournament_selection(population, fitnesses)
                parent2 = self.tournament_selection(population, fitnesses)

                if random.random() < self.crossover_rate:
                    child1 = self.order_crossover(parent1, parent2)
                    child2 = self.order_crossover(parent2, parent1)
                else:
                    child1 = parent1[:]
                    child2 = parent2[:]

                child1 = self.mutate(child1)
                child2 = self.mutate(child2)

                new_population.append(child1)
                if len(new_population) < self.population_size:
                    new_population.append(child2)

            population = new_population

        return {
            "best_solution": best_solution,
            "best_fitness": best_fitness,
            "best_conflicts": self.max_fitness - best_fitness,
            "best_generation": best_generation,
            "history": history
        }
