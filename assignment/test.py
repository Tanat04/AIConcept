import random
import copy


def solve_stone_pile(n, stones):
    def fitness(chrom):
        pile_a_weight = 0
        pile_b_weight = 0
        for i in range(n):
            if chrom[i] == 0:
                pile_a_weight += stones[i]
            else:
                pile_b_weight += stones[i]
        return abs(pile_a_weight - pile_b_weight)

    class Chromosome:
        def __init__(self, chrom=None):
            if chrom is None:
                self.chrom = [random.randint(0, 1) for _ in range(n)]
            else:
                self.chrom = copy.deepcopy(chrom)
            self.fit = fitness(self.chrom)

    def crossover(parent):
        x = random.getrandbits(n - 1)  # Generate random bitmask
        mask = [int(bit) for bit in format(x, '0' + str(n - 1) + 'b')]

        ch1 = [parent[0][i] if mask[i] else parent[1][i] for i in range(n - 1)]
        ch2 = [parent[1][i] if mask[i] else parent[0][i] for i in range(n - 1)]
        return ch1 + [parent[0][-1]], ch2 + [parent[1][-1]]

    def mutate(ch):
        i = random.randint(0, n - 1)
        ch[i] = 1 - ch[i]  # Flip the bit (0 to 1 or 1 to 0)

    def getKey(x):
        return x.fit

    def sumfit(population):
        return sum(ch.fit for ch in population)

    def select(population, total_fitness):
        parent = []
        for _ in range(2):
            p = random.choices(population, weights=[
                               ch.fit for ch in population])[0]
            parent.append(p.chrom)
        return parent

    n_pop = 200
    mut_prob = 0.2
    max_gen = 50
    plateau_count = 0

    population = [Chromosome() for _ in range(n_pop)]
    population.sort(key=getKey, reverse=False)
    old_min = 0
    new_min = population[0].fit
    total_fitness = sumfit(population)

    gen = 1
    while plateau_count < 5 and gen <= max_gen:
        old_min = new_min
        new_gen = []
        for _ in range(n_pop // 2):
            parent = select(population, total_fitness)
            ch = list(crossover(parent))
            offspring = []
            for i in range(2):
                r = random.random()
                if r < mut_prob:
                    mutate(ch[i])
                offspring.append(Chromosome(chrom=ch[i]))
            new_gen += offspring
        population = new_gen
        population.sort(key=getKey, reverse=False)
        new_min = population[0].fit
        total_fitness = sumfit(population)
        gen += 1
        if new_min < old_min:
            plateau_count = 0
        else:
            plateau_count += 1

    return population[0].fit


# Test cases
# Test cases
test_cases = [
    [8, [6, 7, 9, 13, 18, 24, 31, 50], 0],
    [5, [5, 5, 4, 3, 3], 0],
    [5, [3, 3, 4, 5, 5], 0],
    [1, [1], 1],
    [1, [2], 2],
    [6, [1, 4, 5, 6, 7, 9], 0],
    [5, [5, 8, 13, 27, 14], 3],
    [5, [5, 4, 3, 3, 3], 0],
    [5, [11, 10, 8, 7, 6], 0],
    [6, [1, 4, 5, 6, 7, 9], 0],
    [6, [9, 7, 6, 5, 4, 1], 0],
    [7, [1, 2, 3, 4, 5, 6, 6], 1],
    [3, [1, 1, 5], 3],
    [6, [1, 2, 3, 4, 100, 100], 0],
    [5, [5, 8, 13, 14, 15], 1],
    [5, [4, 6, 6, 7, 9], 0],
    [7, [36, 25, 12, 10, 8, 7, 1], 1],
    [6, [101, 51, 51, 3, 2, 2], 0],
    [6, [1, 4, 5, 6, 7, 9], 0],
    [4, [1, 3, 9, 27], 14],
    [6, [6, 6, 5, 4, 3, 2], 0],
    [20, [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20], 0],
]

for i, (n, stones, expected_output) in enumerate(test_cases):
    output = solve_stone_pile(n, stones)
    print(
        f"Test case {i+1}: {output}, Expected: {expected_output} test cases: {stones}")
