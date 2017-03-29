from math import log2
from collections import Counter

class Example:
	def __init__(self, attributes, values, classification):
		self.attributes = dict(zip(attributes, [value for value in map(float, values)]))
		self.classification = classification

	def __str__(self):
		return "Attributes: " + str(self.attributes) + "Classification: " + str(self.classification)

class DecisionTree:
	def __init__(self, attribute, threshold):
		self.attribute = attribute
		self.threshold = threshold
		# <= threhold down left
		self.left = None
		# > threshold down right
		self.right = None

	def __str__(self):
		retVal = "Attribute: " + str(self.attribute) + ", Threshold: " + str(self.threshold)
		retVal += "\nL: " + str(self.left)
		retVal += "\nR: " + str(self.right)
		return retVal

def entropy(p, n):
	pTerm = (p/(p+n))
	nTerm = (n/(p+n))
	if (pTerm == 0 or nTerm == 0):
		return 0
	return -pTerm*log2(pTerm) - nTerm*log2(nTerm)

def bestAttribute(attributes, examples, prevThresholds):
	bestIGFound = None
	bestAttribute = None
	bestThreshold = None
	bestLeftHalf = None
	bestRightHalf = None

	classList = [example.classification for example in examples]
	p = classList.count(positiveClass)
	n = classList.count(negativeClass)
	localEntropy = entropy(p, n)
	anyAvail = False
	for attribute in attributes:
		attributeValues = sorted(set([example.attributes[attribute] for example in examples]))
		thresholds = [((attributeValues[i] + attributeValues[i + 1]) / 2) for i in range(len(attributeValues) - 1)]
		for threshold in thresholds:
			if (threshold not in prevThresholds[attribute]):
				anyAvail = True
	for attribute in attributes:
		attributeValues = sorted(set([example.attributes[attribute] for example in examples]))
		thresholds = [((attributeValues[i] + attributeValues[i + 1]) / 2) for i in range(len(attributeValues) - 1)]
		for threshold in thresholds:
			leftHalf = [example for example in examples if example.attributes[attribute] <= threshold]
			rightHalf = [example for example in examples if example not in leftHalf]

			leftP = len([example for example in leftHalf if example.classification == positiveClass])
			leftN = len(leftHalf) - leftP

			rightP = len([example for example in rightHalf if example.classification == positiveClass])
			rightN = len(rightHalf) - rightP

			leftPartialRemainder = (len(leftHalf)/len(examples) * entropy((leftP/len(leftHalf)), (leftN/len(leftHalf))))
			rightPartialRemainder = (len(rightHalf)/len(examples) * entropy((rightP/len(rightHalf)), (rightN/len(rightHalf))))

			remainder = leftPartialRemainder + rightPartialRemainder

			informationGain = localEntropy - remainder
			if ((not bestIGFound or informationGain > bestIGFound) and threshold not in prevThresholds[attribute]):
				#print("IG Improved: ", bestIGFound, " To: ", informationGain)
				#print("Attribute: ", attribute)
				bestIGFound = informationGain
				bestAttribute = attribute
				bestThreshold = threshold
				bestLeftHalf = leftHalf
				bestRightHalf = rightHalf

	return bestAttribute, bestThreshold, bestLeftHalf, bestRightHalf

def traverseDecisionTree(example, decisionTree):
	if (decisionTree == positiveClass or decisionTree == negativeClass):
		return decisionTree
	else:
		if (example.attributes[decisionTree.attribute] <= decisionTree.threshold):
			return traverseDecisionTree(example, decisionTree.left)
		else:
			return traverseDecisionTree(example, decisionTree.right)

def getPathThroughTree(example, decisionTree):
	if (decisionTree == positiveClass or decisionTree == negativeClass):
		return str(decisionTree)
	retVal = "Attribute: " + str(decisionTree.attribute) + ", Threshold: " + str(decisionTree.threshold)
	if (example.attributes[decisionTree.attribute] <= decisionTree.threshold):
		retVal += ", <=:\n"
		retVal += getPathThroughTree(example, decisionTree.left)
	else:
		retVal += ", >:\n"
		retVal += getPathThroughTree(example, decisionTree.right)
	return retVal

def createDecisionTree(examples, attributes, default, prevThresholds):
	if (not examples):
		return default

	classList = [example.classification for example in examples]
	if (classList.count(classList[0]) == len(classList)):
		return classList[0]

	modeCounter = Counter(classList)
	mode = modeCounter.most_common(1)
	modeExamples = mode[0][0]

	bestAttrib, threshold, leftHalf, rightHalf = bestAttribute(attributes, examples, prevThresholds)
	# Because we aren't reducing attributes each time, this is how we check if we've exhausted all of them
	if (not bestAttrib):
		return modeExamples
	prevThresholds[bestAttrib].append(threshold)
	leftSubTree = createDecisionTree(leftHalf, attributes, modeExamples, prevThresholds)
	rightSubTree = createDecisionTree(rightHalf, attributes, modeExamples, prevThresholds)
	retVal = DecisionTree(bestAttrib, threshold)
	retVal.left = leftSubTree
	retVal.right = rightSubTree
	return retVal

# HORSE DECISION TREE

# GLOBAL
positiveClass = "healthy."
negativeClass = "colic."

horseAttributes = ["K", "Na", "CL", "HCO3",
				   "Endotoxin", "Aniongap", "PLA2", "SDH",
				   "GLDH", "TPP", "Breath rate", "PCV",
				   "Pulse rate", "Fibrinogen", "Dimer", "FibPerDim"]

horseTrainExamples = []
with open("horseTrain.txt") as file:
	for line in [line.strip().split(",") for line in file.readlines()]:
		horseTrainExamples.append(Example(horseAttributes, line[:-1], line[-1:][0]))

previousHorseThresholds = {attribute : [] for attribute in horseAttributes}

horseDecisionTree = createDecisionTree(horseTrainExamples, horseAttributes, DecisionTree(None, 0), previousHorseThresholds)
with open("horseDecisionTree.txt", "w") as file:
	file.write(str(horseDecisionTree))

####################################
# TRAINING CLASSIFICATION

print("HORSE TRAINING CLASSIFICATION")
totalRight = 0
totalWrong = 0
with open("horseTrainOutput.txt", "w") as file:
	for example in horseTrainExamples:
		classification = traverseDecisionTree(example, horseDecisionTree)
		path = getPathThroughTree(example, horseDecisionTree)
		file.write(path + "\n")
		file.write("\n")
		if (classification == example.classification):
			totalRight += 1
		else:
			totalWrong += 1
print("Percent Correct: ", totalRight/(totalRight + totalWrong))
print()

####################################
# TESTING CLASSIFICATION

horseTestExamples = []
with open("horseTest.txt") as file:
	for line in [line.strip().split(",") for line in file.readlines()]:
		horseTestExamples.append(Example(horseAttributes, line[:-1], line[-1:][0]))

print("HORSE TESTING CLASSIFICATION")
totalRight = 0
totalWrong = 0
with open("horseTestOutput.txt", "w") as file:
	for example in horseTestExamples:
		classification = traverseDecisionTree(example, horseDecisionTree)
		path = getPathThroughTree(example, horseDecisionTree)
		file.write(path + "\n")
		file.write("\n")
		if (classification == example.classification):
			totalRight += 1
		else:
			totalWrong += 1
print("Percent Correct: ", totalRight/(totalRight + totalWrong))
print()

# STUDENT PERFORMANCE DECISION TREE

# GLOBAL
positiveClass = "1"
negativeClass = "0"

studPerfAttributes = ["SchoolAttended", "Sex" , "Age" , "Neighbourhood",
				   "FamSize", "ParentsTogether", "MEdu", "FEdu",
				   "ParentGuard", "GuardGender", "CommuteTime", "WorkTime",
				   "PastFails", "ExtraSupport", "FamSupport", "ExtraPaidClasses",
				   "ExtraCurric", "NurserySchool", "HigherEd", "Internet",
				   "Romantic" , "FamRelQual" , "FreeTime" , "GoingOut",
				   "WdAlcohol", "WeAlcohol", "Health" , "Absences"]

studPerfTrainExamples = []
with open("porto_math_train.csv") as file:
	for line in [line.strip().split(",") for line in file.readlines()]:
		studPerfTrainExamples.append(Example(studPerfAttributes, line[:-1], line[-1:][0]))

previousStudPerfThresholds = {attribute : [] for attribute in studPerfAttributes}

studPerfDecisionTree = createDecisionTree(studPerfTrainExamples, studPerfAttributes, DecisionTree(None, 0), previousStudPerfThresholds)
with open("studPerfDecisionTree.txt", "w") as file:
	file.write(str(studPerfDecisionTree))

####################################
# TRAINING CLASSIFICATION

print("STUD PERF TRAINING CLASSIFICATION")
totalRight = 0
totalWrong = 0
with open("studPerfTrainOutput.txt", "w") as file:
	for example in studPerfTrainExamples:
		classification = traverseDecisionTree(example, studPerfDecisionTree)
		path = getPathThroughTree(example, studPerfDecisionTree)
		file.write(path + "\n")
		file.write("\n")
		if (classification == example.classification):
			totalRight += 1
		else:
			totalWrong += 1
print("Percent Correct: ", totalRight/(totalRight + totalWrong))
print()

####################################
# TESTING CLASSIFICATION

studPerfTestExamples = []
with open("porto_math_test.csv") as file:
	for line in [line.strip().split(",") for line in file.readlines()]:
		studPerfTestExamples.append(Example(studPerfAttributes, line[:-1], line[-1:][0]))

print("STUD PERF TESTING CLASSIFICATION")
totalRight = 0
totalWrong = 0
with open("studPerfTestOutput.txt", "w") as file:
	for example in studPerfTestExamples:
		classification = traverseDecisionTree(example, studPerfDecisionTree)
		path = getPathThroughTree(example, studPerfDecisionTree)
		file.write(path + "\n")
		file.write("\n")
		if (classification == example.classification):
			totalRight += 1
		else:
			totalWrong += 1
print("Percent Correct: ", totalRight/(totalRight + totalWrong))