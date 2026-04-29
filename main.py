import statistics
from NQueensGA import NQueensGA


def print_board(solution):
    n = len(solution)
    for row in range(n):
        line = ""
        for col in range(n):
            if solution[col] == row:
                line += "Q "
            else:
                line += ". "
        print(line)


def run_for_n(n):
    print("\n--- Egyetlen futás - n =", n, "---")
    ga = NQueensGA(
        n=n
    )
    result = ga.run(seed=12345)

    print("Legjobb megoldás:", result["best_solution"])
    print("Fitness:", result["best_fitness"])
    print("Konfliktusok száma:", result["best_conflicts"])
    print("Megoldás generációja:", result["best_generation"])

    print("\nSakktábla:")
    print_board(result["best_solution"])

    print("\n--- Többszöri futtatás - n =", n, "---")
    runs = 30
    generations_to_solution = []
    success_count = 0

    for i in range(runs):
        result = ga.run(seed=i)
        if result["best_conflicts"] == 0:
            success_count += 1
            generations_to_solution.append(result["best_generation"])

    print(f"Sikeres futások száma: {success_count}/{runs}")
    if generations_to_solution:
        print("Átlagos generációszám sikeres futásoknál:", statistics.mean(generations_to_solution))


def run():
    run_for_n(8)
    run_for_n(10)
    run_for_n(12)
    run_for_n(14)


if __name__ == "__main__":
    run()
