
from population import Population
from fitness import Fitness
from random import randint

class GeneticAlgorithm:
    def __init__(self):
        return None

    def run(self, population_size, generations, mutation_rate, crossover_rate):
        population = Population(population_size)
        fitness = Fitness(population.dates)

        for generation in range(generations):
            print(f"Generation {generation}")
            # select parents
            parents = population.dates[:int(len(population.dates) * crossover_rate)]
            # select random children
            children = [self.__select_child(parents) for i in range(len(parents))]
            # mutate children
            children = [self.__mutate(child, mutation_rate) for child in children]
            # replace parents with children
            population.dates = children
            # compute fitness
            fitness.compute_fitness(children)
            print(fitness.dates)

        return population

    def __select_child(self, parents):
        return parents[randint(0, len(parents) - 1)]

    def __mutate(self, child, mutation_rate):
        return child

population = Population(100).dates
Fitness(population).compute_fitness([
        (31, 12, 2023), (29, 2, 2024),
        (31, 12, 2023), (30, 4, 2025), 
        (15, 5, 2027), (29, 2, 1900), 
        (32, 1, 2024), (31, 4, 2025), 
        (30, 2, 2024), (-1, 10, 2022),
        (12, 13, 2022)]
    )