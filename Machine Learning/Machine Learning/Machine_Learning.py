from math import log2
from collections import Counter

class Example:
	def __init__(self, attributes, values, classification):
		self.attributes = dict(zip(attributes, [value for value in map(float, values)]))
		self.classification = classification

class DecisionTree:
	def __init__(self, attribute, threshold):
		self.attribute = attribute
		self.threshold = threshold
		# <= threhold down left
		self.left = None
		# > threshold down right
		self.right = None

	def __str__(self):
		retVal = "Attribute: " + str(self.attribute) + " Threshold: " + str(self.threshold)
		retVal += " L: " + str(self.left)
		retVal += " R: " + str(self.right)
		return retVal

def entropy(p, n):
	pTerm = (p/(p+n))
	nTerm = (n/(p+n))
	if (pTerm == 0 or nTerm == 0):
		return 0
	return -pTerm*log2(pTerm) - nTerm*log2(nTerm)

def remainder(attributeValues):
	pass

def informationGain(attribute, example):
	pass

def bestAttribute(attributes, examples):
	bestIGFound = None
	bestAttribute = None
	bestThreshold = None
	bestLeftHalf = None
	bestRightHalf = None

	classList = [example.classification for example in examples]
	p = classList.count(positiveClass)
	n = classList.count(negativeClass)
	localEntropy = entropy(p, n)
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
			if (not bestIGFound or informationGain > bestIGFound):
				#print("IG Improved: ", bestIGFound, " To: ", informationGain)
				#print("Attribute: ", attribute)
				bestIGFound = informationGain
				bestAttribute = attribute
				bestThreshold = threshold
				bestLeftHalf = leftHalf
				bestRightHalf = rightHalf

	return bestAttribute, bestThreshold, bestLeftHalf, bestRightHalf


def createDecisionTree(examples, attributes, default):
	if (not examples):
		return default

	classList = [example.classification for example in examples]
	if (classList.count(classList[0]) == len(classList)):
		return classList[0]

	modeCounter = Counter([example.classification for example in examples])
	mode = modeCounter.most_common(1)
	modeExamples = mode[0]
	if (not attributes):
		return modeExamples

	bestAttrib, threshold, leftHalf, rightHalf = bestAttribute(attributes, examples)
	leftSubTree = createDecisionTree(leftHalf, attributes, modeExamples)
	rightSubTree = createDecisionTree(leftHalf, attributes, modeExamples)
	retVal = DecisionTree(bestAttrib, threshold)
	retVal.left = leftSubTree
	retVal.right = rightSubTree
	return retVal

horseAttributes = ["K", "Na", "CL", "HCO3",
				   "Endotoxin", "Aniongap", "PLA2", "SDH",
				   "GLDH", "TPP", "Breath rate", "PCV",
				   "Pulse rate", "Fibrinogen", "Dimer", "FibPerDim"]

examples = []
with open("horseTrain.txt") as file:
	for line in [line.strip().split(",") for line in file.readlines()]:
		examples.append(Example(horseAttributes, line[:-1], line[-1:][0]))

positiveClass = "healthy."
negativeClass = "colic."

result = createDecisionTree(examples, horseAttributes, DecisionTree(None, 0))
print(str(result))