#!/usr/bin/python
#
#  Data for travelling salesman problem.
#
#  The data file 'miles.dat' and the code for absorbing
#  this file were cribbed from the Stanford GraphBase project.
#
#  tspdata.input()  Absorb the miles.dat file
#  tspdata.cities   A list of city names
#  tspdata.dist(city1, city2)  Ahe integer distance between 2 cities
#  tspdata.pathcheck(path)  Where path is a list of cities, verifies
#             that all the cities are in the list and the length is OK
#  tspdata.loc(city)  Returns (latitude, longitude) tuple for city
#  tspdata.scaledloc(city)  Returns (x-pos, y-pos) coordinates tuple
#                           scaled to the interval [0.0, 1.0]
#
import sys
import re

#  List of city names (strings)
#
cities = []
original_cities = []

#  Matrix of distances: dists[city_1][city_2] = distance
#  It is a dictionary of dictionaries of integers
#
dists = {}

#  Saved, sorted copy of city names for checking path validity 
#
saved_cities = []

#  Locations: a dictionary of (latitude, longitude) of cities
#  indexed by city name.  The position is coded as 
#
locs = {}
scaledlocs = {}

#  Return the distance between two cities
#
def dist(c1, c2):
    return dists[c1][c2]

#  Return the latitude and longitude of a city.
#
def loc(c): return locs[c]
def scaledloc(c):  return scaledlocs[c]

#--------------------------------------------------------------------
# Calculate pathlen (summed distance) of one proposed path.
# (We calculate the whole circuit, from starting city back to start.)
# 
#  z = ((city_0, city_1), (city_1, city_2), ... (city_n, city_0))
#  The lambda accumulates the distance between successive city pairs
#
def pathlen(path):
    z = list(zip(path, path[1:]+path[:1]))
    return reduce(lambda t, c: t + dist(*c), z, 0)

#--------------------------------------------------------------------
# Calculate the length (summed distance) of a segment of a path.
# (This differs from pathlen() by not looping back to start point)
#
# z = ((city_i, city_i+1), (city_i+1, city_i+2), ... (city_j-1, city_j))
#
def seglen(seg):
    z = list(zip(seg[:-1], seg[1:]))
    return reduce(lambda t, c: t + dist(*c), z, 0)


#  Truncate the list of cities
#
def ncities(n):
    global cities, saved_cities, original_cities
    cities = original_cities[:n]
    saved_cities = cities[:]
    saved_cities.sort()
    
#  Read the city names and distances into the global variables
#
def input():
    global cities, dists, saved_cities, original_cities

    #  Read city and distances
    if len(cities) > 0: return
    fname = open("miles.dat", 'r')
    cityfind = re.compile(r'(?P<city>\D[^[]*)\[(?P<lat>\d*).(?P<lon>\d*)')
    for line in fname:
        if line.isspace() or line.startswith("*"): # skip comments
            continue
        m = cityfind.match(line)
        if m:   # Line has city name 
            i = 1
            city, lat, lon = m.group('city', 'lat', 'lon')
            cities.insert(0,city)
            dists[city]={ city : 0 }
            locs[city]=(int(lat), int(lon)) 
        else:                         # Line has distances to previous cities 
            for d in line.split():
                dists[city][cities[i]] = int(d)
                dists[cities[i]][city] = int(d)
                i=i+1
    fname.close()

    # Save a copy of the cities list for error checking
    saved_cities = cities[:]
    saved_cities.sort()

    # Save another copy because sometimes we will truncate the list
    original_cities = cities[:]

    # Find minimum and maximum latitude and longitude
    #
    lats, lons = list(zip(*list(locs.values())))
    minlat, maxlat = degmin(min(lats)), degmin(max(lats))
    minlon, maxlon = degmin(min(lons)), degmin(max(lons))
    latspan = float(maxlat - minlat)
    lonspan = float(maxlon - minlon)

    #  Save scaled location for each city
    for (city, latlon) in locs.items():
        lat, lon = latlon
        scaledlocs[city] = ( (degmin(lat)-minlat)/latspan,  \
                             (degmin(lon)-minlon)/lonspan )

#  Convert degrees and minutes into a single integer
#
def degmin(x):  return (x/100)*60+(x%60)

#  Check that a proposed path has all the cities in it.
#
def pathcheck(path):
    global saved_cities
    p = path[:]
    p.sort()
    return p == saved_cities

#  Quick and dirty main program to absorb the city data and
#  manually check.
#
if __name__ == '__main__':

    eval(input())
    print("Index of cities")
    for city in cities: 
        print(city)
    while True:
        print("Type a city:")
        c1 = sys.stdin.readline().strip()
        if not c1: break
        print("Type another city:")
        c2 = sys.stdin.readline().strip()
        if not c2: break
        print('c1=', loc(c1), ' c2=', loc(c2), ' dist=', dist(c1,c2))
        print('Scaled Loc', c1, '=', scaledloc(c1))
            
