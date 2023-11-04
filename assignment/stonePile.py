import random


def calculate_weight_difference(pile1, pile2):
    return abs(sum(pile1) - sum(pile2))


def fitness(individual, stones):
    pile1 = []
    pile2 = []
    for i in range(len(individual)):
        if individual[i] == '0':
            pile1.append(stones[i])
        else:
            pile2.append(stones[i])
    return calculate_weight_difference(pile1, pile2)


def create_initial_population(num_stones):
    population = []
    for _ in range(10):  # Adjust population size as needed
        individual = ''.join(random.choice(['0', '1'])
                             for _ in range(num_stones))
        population.append(individual)
    return population


def selection(population, stones):
    selected = []
    for _ in range(len(population)):
        parent1 = random.choice(population)
        parent2 = random.choice(population)
        fitness_parent1 = fitness(parent1, stones)
        fitness_parent2 = fitness(parent2, stones)
        selected.append(parent1 if fitness_parent1 <
                        fitness_parent2 else parent2)
    return selected


def crossover(population):
    offspring = []
    for i in range(0, len(population), 2):
        parent1 = population[i]
        parent2 = population[i+1]
        crossover_point = random.randint(1, len(parent1)-1)
        child1 = parent1[:crossover_point] + parent2[crossover_point:]
        child2 = parent2[:crossover_point] + parent1[crossover_point:]
        offspring.extend([child1, child2])
    return offspring


def mutation(population, mutation_rate):
    mutated_population = []
    for individual in population:
        mutated_individual = ''
        for bit in individual:
            mutated_bit = bit
            if random.random() < mutation_rate:
                mutated_bit = '1' if bit == '0' else '0'
            mutated_individual += mutated_bit
        mutated_population.append(mutated_individual)
    return mutated_population


def genetic_algorithm(stones, num_generations):
    population = create_initial_population(len(stones))
    mutation_rate = 0.1  # Adjust mutation rate as needed

    for _ in range(num_generations):
        population = selection(population, stones)
        population = crossover(population)
        population = mutation(population, mutation_rate)

    best_individual = min(population, key=lambda ind: fitness(ind, stones))
    weight_difference = fitness(best_individual, stones)
    return weight_difference


# Example usage
n = int(input())
stones = list(map(int, input().split()))

num_generations = 100
result = genetic_algorithm(stones, num_generations)
print(result)
