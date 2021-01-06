import time
import random
import statistics

# constants, replace with class variables later

GOAL = 50000 #target weight, 50kg
NUM_RATS = 20#lab capacity for rats
INIT_MIN_WT = 200 #init minWeight in g
INIT_MAX_WT = 600 #init maxWeight in g
INIT_MODE_WT = 300 #init midWeight in g
MUTATE_ODDS = 0.01 #chance
MUTATE_MIN = 0.5 #grams
MUTATE_MAX = 1.2 #grams
LITTER_SIZE = 8 #new rats per generation per rat in lab
LITTERS_PER_YR = 10
GENERATION_LIMIT = 1000 #max generations


if NUM_RATS % 2 != 0:
    NUM_RATS += 1


def populate(num_rats, min_wt, max_wt, mode_wt):
    """ init pop w/ triangular distribution of wt"""
    return[int(random.triangular(min_wt, max_wt, mode_wt))
           for i in range(num_rats)]


def fitness(population, goal):
    """Measure popFitness based on attribute of mean vs target"""
    ave = statistics.mean(population)
    return ave / goal


def select(population, to_retain):
    #cull pop to maxNumRats
    sorted_population = sorted(population)
    to_retain_by_sex = to_retain//2
    members_per_sex = len(sorted_population)//2
    females = sorted_population[:members_per_sex]
    males = sorted_population[members_per_sex:]
    selected_females = females[-to_retain_by_sex:]
    selected_males = males[-to_retain_by_sex:]
    return selected_males, selected_females


def breed(males, females, litter_size):
    """crossover genes among members of pop"""
    random.shuffle(males)
    random.shuffle(females)
    children = []
    for male, female in zip(males, females):
        for child in range(litter_size):
            child = random.randint(female, male)
            children.append(child)
    return children

def mutate(children, mutate_odds, mutate_min, mutate_max):
    """randomly alter rat weight via input odds & fractional changes"""
    for index, rat in enumerate(children):
        if mutate_odds >= random.random():
            children[index] = round(rat * random.uniform(mutate_min, mutate_max))
    return children

def main():
    """Init pop, select, breed, mutate, display results"""
    generations = 0
    parents = populate(NUM_RATS, INIT_MIN_WT, INIT_MAX_WT, INIT_MODE_WT)
    print("initial population weights = {}".format(parents))
    popl_fitness = fitness(parents, GOAL)
    print("initial population fitness = {}".format(popl_fitness))
    print("number to retain = {}".format(NUM_RATS))

    ave_wt = []

    while popl_fitness < 1 and generations < GENERATION_LIMIT:
        selected_males, selected_females = select(parents, NUM_RATS)
        children = breed(selected_males, selected_females, LITTER_SIZE)
        children = mutate(children, MUTATE_ODDS, MUTATE_MIN, MUTATE_MAX)
        parents = selected_males + selected_females + children
        popl_fitness = fitness(parents, GOAL)
        print("Generation {} fitness = {:.4f}".format(generations, popl_fitness))
        ave_wt.append(int(statistics.mean(parents)))
        generations += 1
    print("average weight per generation = {}".format(ave_wt))
    print("\nnumber of generations = {}".format(generations))
    print("number of years = {}".format(int(generations / LITTERS_PER_YR)))

if __name__ == '__main__':
    start_time = time.time()
    main()
    end_time = time.time()
    duration = end_time - start_time
    print("\nRuntime for this program was {} seconds.".format(duration))


