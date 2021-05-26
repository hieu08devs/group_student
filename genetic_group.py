
import random
import pandas as pd

POPULATION_SIZE = 30
LOOP = 100

class Individual(object):
    '''
    Class representing individual in population
    genes: 1	2	3	1	4	6	6	2 (list of group student)
    students[row][column]:
        row: list students
        column: list scores
    '''
    def __init__(self, genes, students, group_size):
        self.genes = genes
        self.students = students
        self.group_size = group_size
        self.num_of_student = students.shape[0]
        self.fitness = self.cal_fitness()
  
    @classmethod
    def create_first_individual(cls, students, group_size):
        '''
        Create first individual
        '''
        genes = []
        num_students = students.shape[0]
        for i in range(num_students):
            group_id = (i // group_size + 1)
            group_name = f'{group_id}'
            genes.append(group_name)
        return Individual(genes, students, group_size)
  
    def cal_fitness(self):
        '''
        Calculate fittness score
        '''
        fitness = 0
        groups = {}
        for index_student in range(self.num_of_student):
            group_name = self.genes[index_student]
            student_scores = self.students[index_student]
            group_scores = groups.get(group_name)
            # print(f'group_scores: {group_scores}')
            if group_scores is None:
                groups[group_name] = student_scores.copy()
                # print(f'groups {group_name}: {groups[group_name]}')
            else:
                for i in range(len(group_scores)):
                    group_scores[i] = min(10.0, group_scores[i] + student_scores[i])
                # print(f'groups exist {group_name}: {groups[group_name]}')

        for group_scores in groups.values():
            fitness += sum(group_scores)
        
        return fitness

    def mutated(self):
        '''
        Create new individual by mutated genes
        '''
        new_genens = self.genes.copy()
        num_pair_mutated = random.randint(1, len(self.genes)//2)
        for _ in range(num_pair_mutated):
            chromosome1 = random.randint(0, len(self.genes)-1)
            chromosome2 = random.randint(0, len(self.genes)-1)
            if chromosome1 != chromosome2:
                temp = new_genens[chromosome1]
                new_genens[chromosome1] = new_genens[chromosome2]
                new_genens[chromosome2] = temp
        return Individual(new_genens, self.students, self.group_size)
    
    def mate(self, partner):
        '''
        Perform mating and produce new offspring
        '''
        len_of_genes = len(self.genes)
        cut_offset = len_of_genes // 2
        new_genes = partner.genes[:cut_offset]
        
        for i in range(len_of_genes):
            index = (i + cut_offset) % len_of_genes
            chromosome = self.genes[index]
            valid_chromosome = new_genes.count(chromosome) < self.group_size
            if valid_chromosome:
                new_genes.append(chromosome)
                if len(new_genes) == len_of_genes:
                    break
        return Individual(new_genes, self.students, self.group_size)
    
    def mate2(self, partner):
        '''
        Perform mating and produce new offspring version 2
        '''
        len_of_genes = len(self.genes)

        cut_size = len_of_genes // 3
        cut_start = random.randint(0, len_of_genes - cut_size)
        
        new_genes = partner.genes[cut_start:cut_start + cut_size]
        new_genes_offset = 0
        
        for i in range(len_of_genes):
            chromosome = self.genes[i]
            valid_chromosome = new_genes.count(chromosome) < self.group_size
            if valid_chromosome:
                if new_genes_offset < cut_start:
                    new_genes.insert(new_genes_offset, chromosome)
                    new_genes_offset += 1
                else:
                    new_genes.append(chromosome)
                if len(new_genes) == len_of_genes:
                    break

        return Individual(new_genes, self.students, self.group_size)

# main function

def group_student_by_ga(dataset, group_size=3, max_score=10.0):

    # calc lower_bound
    num_students = dataset.shape[0]
    num_scores = dataset.shape[1]
    num_groups = num_students // group_size
    if num_students % group_size > 0:
        num_groups += 1
    
    
    lower_bound = num_groups * num_scores * max_score
    
    # create first individual
    first_individual = Individual.create_first_individual(dataset, group_size)
    print(f'first_individual: {first_individual.genes}')

    # create initial population
    population = []
    for _ in range(POPULATION_SIZE):
        mutated_individual = first_individual.mutated()
        print(f'mutated_individual: {mutated_individual.genes}')
        population.append(mutated_individual)
    
    population = sorted(population, key = lambda x:x.fitness, reverse=True)

    # main genetic algorithm
    generation = 1
    reached_LB = population[0].fitness == lower_bound
    while generation < LOOP and not reached_LB:

        # generate new offsprings for new generation
        new_generation = []
    
        # 20% of fittest population goes to the next generation
        s = int((20*POPULATION_SIZE)/100)
        new_generation.extend(population[:s])
    
        # mutaion to produce offspring
        s = int((40*POPULATION_SIZE)/100)
        for _ in range(s):
            parent = random.choice(population[:POPULATION_SIZE//2])
            child = parent.mutated()
            new_generation.append(child)
        
        # crossover to produce offspring
        s = int((40*POPULATION_SIZE)/100)
        for _ in range(s):
            parent1 = random.choice(population[:POPULATION_SIZE//2])
            parent2 = random.choice(population[:POPULATION_SIZE//2])
            child = parent1.mate2(parent2)
            new_generation.append(child)

        population = new_generation
        population = sorted(population, key = lambda x:x.fitness, reverse=True)
        generation += 1

        reached_LB = population[0].fitness == lower_bound

        # track generation
        print(f"Generation: {generation}")
        print(f"[{0}/{len(population)}] - Fitness: {population[0].fitness}, Genes: {population[0].genes}")
        print(f"[{2}/{len(population)}] - Fitness: {population[2].fitness}, Genes: {population[2].genes}")
        print(" ")
        

    print(f'num_groups: {num_groups}')
    print(f'reached lower-bound ({lower_bound}): {reached_LB}')
    
    gap = (lower_bound - population[0].fitness) / lower_bound
    print(f'%LB: {gap}')
    
    population = sorted(population, key = lambda x:x.fitness, reverse=True)
    return population[0]