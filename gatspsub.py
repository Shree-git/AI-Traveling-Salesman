#!/usr/bin/env python 
#
#  Driver subroutine for Travelling Salesman genetic algorithm HW.
#
#  External modules:
#    tspdata:   provides the data
#    evolve:    evolve.evolve(population, opts) produces the
#               next generation.  This module is student-supplied.
#
import sys
import random
from operator import itemgetter
from importlib import reload
from functools import reduce

import tspdata          # Travelling salesman problem data
import evolve as ev     # User-supplied evolve subroutine



class Gatspsub:
    #  Main Program Data
    #
    #  The population is a list of paths, where each path is an
    #  ordered list of the names of the cities.
    #
    def __init__(self, ngens=100, popsize=50, evolveopts='', ncities=0):
        reload(ev)        # User may have edited module
        tspdata.input()         #  Read in cities and distance matrix
        self.restart(ngens=ngens, popsize=popsize, evolveopts=evolveopts, \
                        ncities=ncities)

    def restart(self, ngens=100, popsize=50, evolveopts='', ncities=0):
        self.popsize = popsize  # Default population size
        self.ngens   = ngens    # Default number of generations
        self.evolve_opts = evolveopts # Evolve options
        self.genno = 0          # Generation number
        random.seed(1)          # Start random numbers at fixed place
        if ncities > 1:
            tspdata.ncities(ncities)
        self.ncities = len(tspdata.cities)
        self.initiate_pop(popsize)

    #--------------------------------------------------------------------
    #  Create initial population of paths (each path is a list of cities).
    #  Each path starts with the same city, the remainder are shuffled.
    #
    def initiate_pop(self, popsize):
        self.population = []
        for i in range(popsize):
            path = tspdata.cities[1:]
            random.shuffle(path)
            self.population.append(tspdata.cities[:1] + path)
        self.population=self.sort_pop(self.population)
   
    #--------------------------------------------------------------------
    # Calculate pathlen (summed distance) of one proposed path.
    # (We calculate the whole circuit, from starting city back to start.)
    # 
    #  z = ((city_0, city_1), (city_1, city_2), ... (city_n, city_0))
    #  The lambda accumulates the distance between successive city pairs
    #
    def pathlen(self, path):
        z = list(zip(path, path[1:]+path[:1]))
        return reduce(lambda t, c: t + tspdata.dist(*c), z, 0)

    # Calculate fitness.  Lower numbers are better.
    #
    # Right now fitness = pathlen
    #
    # (An alternate computation was the sum of the squares of the
    #  the distances, the idea being to penalize long jumps.)
    #
  
    def fitness(self, path):
        return self.pathlen(path)
        # Alternate computation:
        z = list(zip(path, path[1:]+path[:1]))
        jumps = [tspdata.dist(*c) for c in z]
        return reduce(lambda t, d: t + d*d, jumps, 0)

    #--------------------------------------------------------------------
    # Calculate the length (summed distance) of a segment of a path.
    # (This differs from pathlen() by not looping back to start point)
    #
    # z = ((city_i, city_i+1), (city_i+1, city_i+2), ... (city_j-1, city_j))
    #
    def seglen(self, seg):
        z = list(zip(seg[:-1], seg[1:]))
        return reduce(lambda t, c: t + tspdata.dist(*c), z, 0)
        
    #--------------------------------------------------------------------
    #  Sort population by fitness
    #
    def sort_pop(self, population):
        # l = [ (city1, fit1), (city2, fit2), (city3, fit3) ]
        l = [(city, self.fitness(city)) for city in population]
        # Put l in order of fitness
        l.sort(key=itemgetter(1))
        # Extract the city from each tuple, return as a list
        return [city_fit[0] for city_fit in l]
    
    #--------------------------------------------------------------------
    #  Remove duplicates in the population (may disorder the list)
    #  -- Join each path in the population into a single $-delimited string
    #  -- Collapse the population into a set of strings (removing duplicates)
    #  -- Expand population back to a list, sort it so we have a repeatable 
    #           ordering.
    #  -- Split each path back into a list of cities.
    #
    def uniq(self, population):
        if len(population) < 2: 
            return population
        strpop = list(set(map('$'.join, population)))
        strpop.sort()
        return [s.split('$')  for s in strpop]
    
    #--------------------------------------------------------------------
    #  Run the genetic algorithm for the requested number of generations
    #
    def run_ga(self, ngens):
        for generationNumber in range(self.genno, self.genno+ngens):
            self.population = \
                self.sort_pop( \
                    self.uniq( \
                        ev.evolve(self.population, self.evolve_opts)))
            if len(self.population) > self.popsize:
                self.population = self.population[:self.popsize]
        self.genno += ngens
        best_path = self.population[0]
        best_pathlen = self.pathlen(best_path)
        worst_pathlen = self.pathlen(self.population[-1])
        print(self.genno, best_pathlen, worst_pathlen)
        return (self.genno, best_path, best_pathlen, worst_pathlen)
    
