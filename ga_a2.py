import random
import csv
import matplotlib.pyplot as plt
from typing import List, Tuple, Dict

Tareekh = Tuple[int, int, int]
TOTAL_CATEGORIES = 11

def leap_ka_jach(year: int) -> bool:
    return year % 4 == 0 and (year % 100 != 0 or year % 400 == 0)

def categorize_date(date: Tareekh) -> str:
    day, month, year = date
    if day < 1:
        return "Invalid_Day_LT1"
    if day > 31:
        return "Invalid_Day_GT31"
    if month < 1:
        return "Invalid_Month_LT1"
    if month > 12:
        return "Invalid_Month_GT12"
    if year < 0 or year > 9999:
        return "Invalid_Year"
    if day == 1 and month == 1 and year == 0:
        return "Boundary_Min"
    if day == 31 and month == 12 and year == 9999:
        return "Boundary_Max"
    if month == 2:
        if leap_ka_jach(year):
            if day == 29:
                return "Valid_Leap_Year"
            elif day > 29:
                return "Invalid_Feb_Day"
            else:
                return "Valid_NonLeap_Feb"
        else:
            if day == 29:
                return "Invalid_Feb29_NonLeap"
            elif day > 28:
                return "Invalid_Feb_Day"
            else:
                return "Valid_NonLeap_Feb"
    if month in [4, 6, 9, 11]:
        if day == 30:
            return "Valid_30Day"
        elif day == 31:
            return "Invalid_Day_For_30DayMonth"
        else:
            return "Valid_Date"
    if month in [1, 3, 5, 7, 8, 10, 12]:
        if day == 31:
            return "Valid_31Day"
        else:
            return "Valid_Date"
    return "Valid_Date"

def is_valid_date(date: Tareekh) -> bool:
    valid_cats = {"Boundary_Min", "Boundary_Max", "Valid_Leap_Year", "Valid_NonLeap_Feb", "Valid_30Day", "Valid_31Day", "Valid_Date"}
    return categorize_date(date) in valid_cats

def random_date() -> Tareekh:
    return (random.randint(1, 31), random.randint(1, 12), random.randint(0, 9999))

def initialize_population(size: int) -> List[Tareekh]:
    return [random_date() for _ in range(size)]

def fitness_function(population: List[Tareekh]) -> float:
    freq: Dict[str, int] = {}
    for date in population:
        cat = categorize_date(date)
        freq[cat] = freq.get(cat, 0) + 1
    unique = len(freq)
    redundancy = sum(count - 1 for count in freq.values())
    fitness = unique * 10 - redundancy
    return fitness

def rank_selection(population: List[Tareekh]) -> Tareekh:
    contenders = random.sample(population, 3)
    contenders.sort(key=lambda d: fitness_function([d]), reverse=True)
    return contenders[0]

def crossover(parent1: Tareekh, parent2: Tareekh) -> Tareekh:
    return (parent1[0] if random.random() < 0.5 else parent2[0],
            parent1[1] if random.random() < 0.5 else parent2[1],
            parent1[2] if random.random() < 0.5 else parent2[2])

def mutation(date: Tareekh, mutation_rate: float = 0.15) -> Tareekh:
    day, month, year = date
    if random.random() < mutation_rate:
        day += random.randint(-3, 3)
    if random.random() < mutation_rate:
        month += random.randint(-1, 1)
    if random.random() < mutation_rate:
        year += random.randint(-100, 100)
    return (day, month, year)

def evolve_population(population: List[Tareekh], mutation_rate: float = 0.15, elite_size: int = 2) -> List[Tareekh]:
    population.sort(key=lambda d: fitness_function([d]), reverse=True)
    new_population = population[:elite_size]
    while len(new_population) < len(population):
        parent1 = rank_selection(population)
        parent2 = rank_selection(population)
        child = crossover(parent1, parent2)
        child = mutation(child, mutation_rate)
        new_population.append(child)
    return new_population

def get_unique_categories(population: List[Tareekh]) -> int:
    return len({categorize_date(d) for d in population})

def ga_run(pop_size: int = 200, generations: int = 100, mutation_rate: float = 0.15, target_coverage: float = 0.95) -> Tuple[List[Tareekh], List[float]]:
    population = initialize_population(pop_size)
    coverage_history = []
    print("Chalo, GA shuru ho gaya! Population size:", pop_size)
    for gen in range(generations):
        population = evolve_population(population, mutation_rate)
        unique_cats = get_unique_categories(population)
        coverage = unique_cats / TOTAL_CATEGORIES
        coverage_history.append(coverage * 100)
        print(f"Gen {gen}: Unique Categories = {unique_cats}/{TOTAL_CATEGORIES}, Coverage = {coverage * 100:.2f}%, Fitness = {fitness_function(population):.2f}")
        freq: Dict[str, int] = {}
        for d in population:
            cat = categorize_date(d)
            freq[cat] = freq.get(cat, 0) + 1
        print("Category Frequencies:", freq)
        if coverage >= target_coverage:
            print(f"Target coverage {target_coverage*100:.2f}% reached at Gen {gen}!")
            break
    return population, coverage_history

def select_final_test_cases(population: List[Tareekh]) -> Tuple[List[str], List[str]]:
    valid_cases = [d for d in population if is_valid_date(d)]
    invalid_cases = [d for d in population if not is_valid_date(d)]
    while len(valid_cases) < 10:
        cand = random_date()
        if is_valid_date(cand):
            valid_cases.append(cand)
    while len(invalid_cases) < 10:
        cand = random_date()
        if not is_valid_date(cand):
            invalid_cases.append(cand)
    boundary_candidates = [(1, 1, 0), (31, 12, 9999), (29, 2, 2020), (31, 1, 2023), (1, 12, 0)]
    for b in boundary_candidates:
        if is_valid_date(b) and b not in valid_cases:
            valid_cases.append(b)
        elif not is_valid_date(b) and b not in invalid_cases:
            invalid_cases.append(b)
    valid_strings = [f"{d[0]:02d}/{d[1]:02d}/{d[2]:04d}" for d in valid_cases[:10]]
    invalid_strings = [f"{d[0]:02d}/{d[1]:02d}/{d[2]:04d}" for d in invalid_cases[:10]]
    return valid_strings, invalid_strings

def save_test_cases_csv(valid: List[str], invalid: List[str], filename: str = "test_cases.csv") -> None:
    with open(filename, mode="w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["Test Case", "Category"])
        for case in valid:
            d = tuple(map(int, case.split('/')))
            writer.writerow([case, categorize_date(d)])
        for case in invalid:
            d = tuple(map(int, case.split('/')))
            writer.writerow([case, categorize_date(d)])
    print("Test cases saved to", filename)

def plot_coverage(coverage_history: List[float]) -> None:
    plt.plot(range(len(coverage_history)), coverage_history, marker='o', linestyle='-')
    plt.title("GA Coverage Improvement Over Generations")
    plt.xlabel("Generation")
    plt.ylabel("Coverage (%)")
    plt.grid(True)
    plt.savefig("coverage_graph.png")
    plt.show()

def main():
    print("GA ke liye Date Validation Test Cases generate karna shuru!")
    population, coverage_history = ga_run(pop_size=200, generations=100, mutation_rate=0.15, target_coverage=0.95)
    print("GA complete ho gaya!")
    valid, invalid = select_final_test_cases(population)
    print("Final Test Cases (DD/MM/YYYY):")
    print("Valid Cases:")
    for case in valid:
        d = tuple(map(int, case.split('/')))
        print(case, "-", categorize_date(d))
    print("Invalid Cases:")
    for case in invalid:
        d = tuple(map(int, case.split('/')))
        print(case, "-", categorize_date(d))
    overall_coverage = len({categorize_date(d) for d in population}) / TOTAL_CATEGORIES * 100
    print(f"Overall Category Coverage: {overall_coverage:.2f}%")
    save_test_cases_csv(valid, invalid)
    plot_coverage(coverage_history)

if __name__ == "__main__":
    main()
