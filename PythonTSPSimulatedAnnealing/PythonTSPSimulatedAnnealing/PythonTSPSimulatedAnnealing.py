from glob import glob
from math import exp
from math import sqrt
from os.path import join

import random
import statistics

########
# CITIES
########
class City(object):
	def __init__(self, name, locX, locY):
		self.name = name
		self.locX = float(locX)
		self.locY = float(locY)

	def __repr__(self):
		return self.name

#########################
# DISTANCE BETWEEN CITIES
#########################
def distance(cityA, cityB):
	return sqrt((cityA.locX - cityB.locX)**2 + (cityA.locY - cityB.locY)**2)

####################
# GET VALUE OF ROUTE
####################
def getValue(route):
	totalDist = 0
	i = 0
	while i < len(route) - 1:
		totalDist += distance(route[i], route[i + 1])
		i += 1
	# Return from last City to first City
	totalDist += distance(route[i], route[0])
	return totalDist

#######################
# GENERATES THE MOVESET
#######################
def generateMoveSet(route):
	moveSet = []
	# Generate 5 possible two-swap options
	if (len(route) > 1):
		for i in range(5):
			randomIndex = random.randrange(1, len(route))
			randomIndex2 = random.randrange(1, len(route))
			newRoute = route.copy()
			newRoute[randomIndex], newRoute[randomIndex2] = newRoute[randomIndex2], newRoute[randomIndex]
			moveSet.append(newRoute)
	return moveSet


#####################################
# CALCAULTES T FOR ANNEALING SCHEDULE
#####################################
def recomputeT(currentT, originalT, currentDeltaV, percentageCompleted):
	#if (currentDeltaV > 0):
		return currentT * 0.99 #Exponential decrease when we're good
	#else:
		#return originalT * (1 - percentageCompleted) #Linear when not, to maybe help it start improving again

######################
# FINDS THE BEST ROUTE
######################
def getTSPRoute(initialRoute, initialT, maxIterations, outputFile, printInterval):
	currentRoute = initialRoute
	currentValue = getValue(currentRoute)
	originalT = initialT;
	T = initialT
	interval = 1
	for run in range(1, maxIterations + 1):
		moveSet = generateMoveSet(currentRoute)
		if (not moveSet): 
			break;
		randomMove = random.choice(moveSet)
		value = getValue(randomMove)
		deltaV = currentValue - value
		useNewPath = False
		if (deltaV > 0):
			useNewPath = True
		else:
			try:
				prob = exp(deltaV/T)
			except OverflowError:
				prob = float('-inf')
			randomFloat = random.random()
			if (randomFloat < prob):
				useNewPath = True
		if (useNewPath == True):
			currentRoute = randomMove;
			currentValue = value
		if (interval >= printInterval):
			interval = 0
			outputFile.write("{}, {}\n".format(run, currentValue))
			print(run, currentValue)
		T = recomputeT(T, originalT, deltaV, run / float(maxIterations))
		interval += 1
	return currentRoute, currentValue

###############
# PARSES CITIES
###############
def parseCities(filename):
	with open(filename) as file:
		numCities = int(file.readline())
		cities = []
		for line in file:
			args = line.split()
			city = City(*args)
			cities.append(city)
	return cities

######################
# RUNNING MAIN PROGRAM
######################
outputFileName = "totalDistance362.txt"
outputFile = open(outputFileName, "w")
#folders = range(1, 17)
#for folder in folders:
#print("Folder: {}".format(folder))
filenames = glob(join("randTSP", "*.txt"))

initialT = 10000000
maxIterations = 10000
printInterval = 10
random.seed()

results = []
outputFile.write("Run, Cost\n")
for filename in filenames:
	cities = parseCities(filename)
	outputFile.write("{}, {}\n".format(0, getValue(cities)))
	shortestPath, value = getTSPRoute(cities, initialT, maxIterations, outputFile, printInterval)
	results.append(value)
print(shortestPath)
print(value)