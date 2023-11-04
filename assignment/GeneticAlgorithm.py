import random
import copy
import time

st = time.process_time()
n = int(input())
stones = list(map(int, input().split()))


def fitness(chrom):
    # Return fitness value of chromosome's chrom ch
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
    # parent = list of chromosome's chrom attributes
    x = random.randint(0, n - 1)  # [:x+1] and [x+1:]
    ch1 = parent[0][:x+1] + parent[1][x+1:]
    ch2 = parent[1][:x+1] + parent[0][x+1:]
    return ch1, ch2


def mutate(ch):
    # Mutate chromosome's chrom ch
    i = random.randint(0, n - 1)
    ch[i] = 1 - ch[i]  # Flip the bit (0 to 1 or 1 to 0)


def getKey(x):
    return x.fit


def sumfit(population):
    s = 0
    for ch in population:
        s += ch.fit
    return s


def select(population, total_fitness):
    parent = []
    for k in range(2):
        p = random.randint(0, n_pop - 1)
        accept_prob = population[p].fit / total_fitness
        r = random.random()
        while r > accept_prob:
            p = random.randint(0, n_pop - 1)
            accept_prob = population[p].fit / total_fitness
            r = random.random()
        parent.append(population[p].chrom)
    return parent


n_pop = 200  # Keep even to match double offsprings per crossover
mut_prob = 0.2  # Probability of mutation
max_gen = 50  # Max number of generations
plateau_count = 0  # Number of no improvements to stop searching

# Randomized at the beginning
population = [Chromosome() for _ in range(n_pop)]

population.sort(key=getKey, reverse=False)  # Lower fitness is preferred
old_min = 0
new_min = population[0].fit
total_fitness = sumfit(population)
# print(new_min)
gen = 1  # Generation count
while plateau_count < 5 and gen <= max_gen:
    old_min = new_min
    new_gen = []
    for j in range(n_pop // 2):
        parent = select(population, total_fitness)
        ch = list(crossover(parent))
        offspring = []
        for i in range(2):
            r = random.random()
            if r < mut_prob:
                mutate(ch[i])
            offspring.append(Chromosome(chrom=ch[i]))
        new_gen += offspring
    both_gen = population + new_gen
    both_gen.sort(key=getKey, reverse=False)
    population = both_gen[:n_pop]
    new_min = population[0].fit
    total_fitness = sumfit(population)
    # print(new_min)
    gen += 1
    if new_min < old_min:
        plateau_count = 0
    else:
        plateau_count += 1


et = time.process_time()
print(population[0].fit)
print("convergence speedgen:", gen)
print(et - st)
