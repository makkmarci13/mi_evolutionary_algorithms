import csv
import random
import statistics
from itertools import product


class EightQueensGA:
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


def print_board(solution):
    n = len(solution)
    for row in range(n):
        line = ""
        for col in range(n):
            line += "Q " if solution[col] == row else ". "
        print(line)


def run_single_example(n=8):
    print("\n--- Egyetlen példafutás - n =", n, "---")
    ga = EightQueensGA(n=n)
    result = ga.run(seed=12345)

    print("Legjobb megoldás:", result["best_solution"])
    print("Fitness:", result["best_fitness"])
    print("Konfliktusok száma:", result["best_conflicts"])
    print("Megoldás generációja:", result["best_generation"])

    if result["best_solution"] is not None:
        print("\nSakktábla:")
        print_board(result["best_solution"])


def evaluate_config(n, population_size, mutation_rate, elite_size, runs=30, generations=300,
                    crossover_rate=0.95, tournament_size=4):
    successful_generations = []
    best_conflicts_all_runs = []

    for seed in range(runs):
        ga = EightQueensGA(
            n=n,
            population_size=population_size,
            generations=generations,
            crossover_rate=crossover_rate,
            mutation_rate=mutation_rate,
            elite_size=elite_size,
            tournament_size=tournament_size
        )
        result = ga.run(seed=seed)
        best_conflicts_all_runs.append(result["best_conflicts"])

        if result["best_conflicts"] == 0:
            successful_generations.append(result["best_generation"])

    success_count = len(successful_generations)
    success_rate = success_count / runs

    return {
        "n": n,
        "population_size": population_size,
        "mutation_rate": mutation_rate,
        "elite_size": elite_size,
        "crossover_rate": crossover_rate,
        "tournament_size": tournament_size,
        "generations": generations,
        "runs": runs,
        "success_count": success_count,
        "success_rate": success_rate,
        "avg_generation_successful": statistics.mean(successful_generations) if successful_generations else None,
        "median_generation_successful": statistics.median(successful_generations) if successful_generations else None,
        "avg_best_conflicts": statistics.mean(best_conflicts_all_runs),
        "min_best_conflicts": min(best_conflicts_all_runs),
        "max_best_conflicts": max(best_conflicts_all_runs),
    }


def benchmark_parameters():
    n_values = [8, 10, 12, 14]
    population_sizes = [50, 100, 200]
    mutation_rates = [0.05, 0.10, 0.30, 0.50]
    elite_sizes = [0, 2, 4, 10]

    runs = 30
    generations = 300
    crossover_rate = 0.95
    tournament_size = 4

    results = []
    total = len(n_values) * len(population_sizes) * len(mutation_rates) * len(elite_sizes)

    print("\n--- Paraméterhangolás indítása ---")
    print(f"Összes konfiguráció: {total}")
    print(f"Futtatások konfigurációnként: {runs}")

    counter = 0
    for n, population_size, mutation_rate, elite_size in product(
            n_values, population_sizes, mutation_rates, elite_sizes
    ):
        counter += 1
        print(
            f"[{counter}/{total}] "
            f"N={n}, pop={population_size}, mutation={mutation_rate}, elite={elite_size}",
            flush=True
        )

        row = evaluate_config(
            n=n,
            population_size=population_size,
            mutation_rate=mutation_rate,
            elite_size=elite_size,
            runs=runs,
            generations=generations,
            crossover_rate=crossover_rate,
            tournament_size=tournament_size
        )
        results.append(row)

    results.sort(
        key=lambda r: (
            -r["success_rate"],
            r["avg_generation_successful"] if r["avg_generation_successful"] is not None else float("inf"),
            r["avg_best_conflicts"]
        )
    )

    save_results_to_csv(results, "benchmark_results.csv")
    print_best_results(results)
    print_best_result_per_n(results)


def save_results_to_csv(results, filename):
    fieldnames = [
        "n",
        "population_size",
        "mutation_rate",
        "elite_size",
        "crossover_rate",
        "tournament_size",
        "generations",
        "runs",
        "success_count",
        "success_rate",
        "avg_generation_successful",
        "median_generation_successful",
        "avg_best_conflicts",
        "min_best_conflicts",
        "max_best_conflicts",
    ]

    with open(filename, "w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(results)

    print(f"\nEredmények mentve ide: {filename}")


def print_best_results(results, limit=10):
    print("\n--- Legjobb konfigurációk összesítve ---")
    print(
        "Hely | N | Pop | Mutáció | Elite | Siker | Átlag gen. | Átlag konfliktus"
    )
    print("-" * 85)

    for index, row in enumerate(results[:limit], start=1):
        avg_gen = row["avg_generation_successful"]
        avg_gen_text = f"{avg_gen:.3f}" if avg_gen is not None else "-"

        print(
            f"{index:>4} | "
            f"{row['n']:>2} | "
            f"{row['population_size']:>3} | "
            f"{row['mutation_rate']:>7.2f} | "
            f"{row['elite_size']:>5} | "
            f"{row['success_count']:>2}/{row['runs']:<2} | "
            f"{avg_gen_text:>10} | "
            f"{row['avg_best_conflicts']:.3f}"
        )


def print_best_result_per_n(results):
    print("\n--- Legjobb konfiguráció külön-külön minden N értékre ---")
    print(
        "N | Pop | Mutáció | Elite | Siker | Átlag gen. | Átlag konfliktus"
    )
    print("-" * 75)

    for n in sorted(set(row["n"] for row in results)):
        filtered = [row for row in results if row["n"] == n]
        best = filtered[0]
        avg_gen = best["avg_generation_successful"]
        avg_gen_text = f"{avg_gen:.3f}" if avg_gen is not None else "-"

        print(
            f"{best['n']:>2} | "
            f"{best['population_size']:>3} | "
            f"{best['mutation_rate']:>7.2f} | "
            f"{best['elite_size']:>5} | "
            f"{best['success_count']:>2}/{best['runs']:<2} | "
            f"{avg_gen_text:>10} | "
            f"{best['avg_best_conflicts']:.3f}"
        )


def run():
    run_single_example(8)
    benchmark_parameters()


if __name__ == "__main__":
    run()
