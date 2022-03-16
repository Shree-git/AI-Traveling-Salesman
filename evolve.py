#  Evolve program for the CS 345/CS 372 TSP Genetic Algorithm homework 
#
#  This program comes with some example mutations.
#
# pop is a list of paths, e.g. 
#  [ [ city1, city2, ... city_n-1, city_n ],
#    [ city1, city3, city_n, ... city_2 ],
#    ... ]
#
# opts is a string containing user-defined options
#
import random     # Methods for creating random numbers, etc. (needed)
import tspdata    # Methods for finding distances (optionally useful)


def evolve(pop, opts):
    pathlen = len(pop[0]) 
    newpaths = [] 

    #  Random switching, mutating, etc, with results in new paths 
    #  Here is some skeleton example
    
    # Consider every path in the population
    for path in pop:

        # This newpath starts out as a copy of an existing path
        #   (Because we don't want to alter the existing path)
        newpath = path[:]

        #  Insert code here to give newpath a different order
        #  For example, swap two points.
        pt1 = random.randint(1,pathlen-1)
        pt2 = random.randint(1,pathlen-1)
        newpath[pt1], newpath[pt2] = newpath[pt2], newpath[pt1]

        #  Here is an example debugging option:
        if 'D' in opts:
           print(newpath)
        #
        # Save the new path we have created
        newpaths.append(newpath)  # save newpath

        # It is possible to create several new paths. Here
        # we create another one by shuffling between two points
        #   (No need to make a fresh copy, slicing does that)
        pt1, pt2 = min(pt1,pt2), max(pt1,pt2)  # Points in order
        part1 = path[:pt1]
        part2 = path[pt1:pt2]
        part3 = path[pt2:]
        random.shuffle(part2)     # Shuffle it
        newpaths.append(part1 + part2 + part3)    # save 

        #  ... but you will do something more sophisticated
    setOfCities = pop[0]
    for x in range(len(pop)-1):
        path1 = pop[x]
        path2 = pop[x+1]
        a = path1[:]
        b = path2[:]
        pt1 = random.randint(1, pathlen-1)
        pt2 = random.randint(1, pathlen-1)
        pt1, pt2 = min(pt1, pt2), max(pt1, pt2)
        donor = a[pt1:pt2+1]
        newPath = b[:pt1]+donor+b[pt2+1:]
        newPath = list(dict.fromkeys(newPath))
        for p in setOfCities:
            if p not in newPath:
                newPath.append(p)
        newpaths.append(newPath)


#   Finally combine the newpaths into the population with the existing paths
    pop.extend(newpaths)
    return pop
