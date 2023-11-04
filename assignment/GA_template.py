import random
import copy

k = 8  # range of possible values
n = 8  # size of chromosome

def fitness(ch):
    # Return fitness value of chromosome's chrom ch
    pass

class chromosome:
    def __init__(self, chrom=None):
        if chrom == None:
            self.chrom = []
            for i in range(n): 
                self.chrom.append(random.randint(0,10000)%k)
        else:
            self.chrom = copy.deepcopy(chrom)
        self.fit = fitness(self.chrom)

def crossover(parent):
    # parent = list of chromosome's chrom attributes
    
    x = random.randint(0,10000)%(n-1)   # [:x+1] and [x+1:]
    ch1 = parent[0][:x+1] + parent[1][x+1:]
    ch2 = parent[1][:x+1] + parent[0][x+1:]
    return ch1, ch2

def mutate(ch):
    # Mutate chromosome's chrom ch
    i = random.randint(0,10000)%n
    ch[i] = random.randint(0,10000)%k

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
        p = random.randint(0,10000)%n_pop
        accept_prob = population[p].fit / total_fitness
        r = random.randint(0,10000)/10000
        while r > accept_prob:
            p = random.randint(0,10000)%n_pop
            accept_prob = population[p].fit / total_fitness
            r = random.randint(0,10000)/10000
        parent.append(population[p].chrom)
    return parent

n_pop = 200      # Keep even to match double offsprings per crossover
mut_prob = 0.2   # probability of mutation
max_gen = 50     # Max number of generations
plateau_count = 0  # Number of no improvements to stop searching

population = []
for i in range(n_pop):
    population.append(chromosome())   # Randomized at the beginning

population.sort(key=getKey, reverse=True)  # higher fitness is preferred
old_max = 0
new_max = population[0].fit
total_fitness = sumfit(population)
print(new_max)
gen = 1     # generation count
while plateau_count < 5 and gen <= max_gen:
    old_max = new_max
    new_gen = []
    for j in range(n_pop//2):
        parent = select(population, total_fitness)
        ch = list(crossover(parent))
        offspring = []
        for i in range(2):
            r = random.randint(0,10000)/10000
            if r < mut_prob:
                mutate(ch[i])
            offspring.append(chromosome(chrom=ch[i]))
        new_gen += offspring
    both_gen = population + new_gen
    both_gen.sort(key=getKey, reverse=True)
    population = both_gen[:n_pop]
    new_max = population[0].fit
    total_fitness = sumfit(population)
    print(new_max)
    gen += 1
    if new_max > old_max:
        plateau_count = 0
    else:
        plateau_count += 1

print(population[0].chrom)
