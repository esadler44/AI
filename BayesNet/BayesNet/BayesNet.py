from functools import reduce

class Factor:
	def __init__(self):
		self.table = {}

	def addRow(self, setKey, prob):
		self.table[frozenset(setKey)] = prob
		
	def __str__(self):
		output = ""
		for key in sorted([sorted(list(x), key=lambda x: x[::-1]) for x in self.table.keys()]):
			output += ' '.join(keystr.rjust(4) for keystr in key)
			output += " : "
			output += str(self.table[frozenset(key)]) + '\n'
		return output

def negativeValue(value):
	if (value[0] == '~'):
		return value[1:]
	else:
		return '~' + value

def containsVariable(factor, variable):
	keyList = [x for x in factor.table.keys()]
	for key in keyList:
		if (variable in key or negativeValue(variable) in key):
			return True
	return False

def restrict(factor, value):
	newFactor = Factor()
	for frozenKey in factor.table.keys():
		if (value in frozenKey):
			newFactor.addRow(frozenKey - {value}, factor.table[frozenKey])
	return newFactor

def multiply(factor1, factor2):
	newFactor = Factor()
	for frozenKey1 in factor1.table.keys():
		for frozenKey2 in factor2.table.keys():
			if (not (frozenset(map(negativeValue, frozenKey2)) & frozenKey1)):
				newFactor.addRow(frozenKey1 | frozenKey2, factor1.table[frozenKey1] * factor2.table[frozenKey2])
	return newFactor

def sumout(factor, variable):
	newFactor = Factor()
	# Variable pass
	for frozenKey in factor.table.keys():
		if (variable in frozenKey):
			newFactor.addRow(frozenKey - {variable}, factor.table[frozenKey])
	# Negative variable pass
	negativeVariable = negativeValue(variable)
	for frozenKey in factor.table.keys():
		if (negativeVariable in frozenKey):
			newFactor.table[frozenKey - {negativeVariable}] += factor.table[frozenKey]
	return newFactor

def normalize(factor):
	totalProb = sum(factor.table.values())
	for frozenKey in factor.table.keys():
		factor.table[frozenKey] /= totalProb
	return factor

def inference(factorList, queryVariable, evidenceList, orderedListOfHiddenVariables):
	print("Evidence:", evidenceList)
	# Restricting factors based on evidence
	for evidence in evidenceList:
		for i in range(len(factorList)):
			if containsVariable(factorList[i], evidence):
				restriction = restrict(factorList[i], evidence)
				factorList[i] = restriction # We only want tables with data in them
	# Removing any flattened factors
	factorList = [factor for factor in factorList if len(factor.table) > 1]

	print("Restricted factors:")
	for factor in factorList:
		print(factor)

	for hiddenVar in orderedListOfHiddenVariables:
		containingFactors = [factor for factor in factorList if containsVariable(factor, hiddenVar)]
		productReductionFactor = reduce((lambda f1, f2: multiply(f1, f2)), containingFactors)
		summationReductionFactor = sumout(productReductionFactor, hiddenVar)
		factorList.append(summationReductionFactor)
		for usedFactor in containingFactors:
			factorList.remove(usedFactor)
		print("Eliminated variable: ", hiddenVar)
		for factor in factorList:
			print(factor)

	print("Final product and normalization:")
	finalFactor = reduce((lambda f1, f2: multiply(f1, f2)), factorList)
	normalize(finalFactor)
	print(finalFactor)
	return finalFactor

### TESTING

'''
f1 = Factor()
f1.addRow({'a', 'b'}, 0.9)
f1.addRow({'a', '~b'}, 0.1)
f1.addRow({'~a', 'b'}, 0.4)
f1.addRow({'~a', '~b'}, 0.6)

f2 = Factor()
f2.addRow({'b', 'c'}, 0.7)
f2.addRow({'b', '~c'}, 0.3)
f2.addRow({'~b', 'c'}, 0.8)
f2.addRow({'~b', '~c'}, 0.2)

print(f1)
print(f2)

print(multiply(f1, f2))
print(sumout(f1, 'a'))
print(restrict(f1, 'a'))
'''

### A4

f1 = Factor()
f1.addRow({'na'}, 3/10)
f1.addRow({'~na'}, 7/10)

f2 = Factor()
f2.addRow({'fm'}, 1/28)
f2.addRow({'~fm'}, 27/28)

f3 = Factor()
f3.addRow({'fs'}, 0.05)
f3.addRow({'~fs'}, 0.95)

f4 = Factor()
f4.addRow({'fb', 'fs'}, 0.6)
f4.addRow({'fb', '~fs'}, 0.1)
f4.addRow({'~fb', 'fs'}, 0.4)
f4.addRow({'~fb', '~fs'}, 0.9)

f5 = Factor()
f5.addRow({'ndg', 'fm', 'na'}, 0.8)
f5.addRow({'ndg', 'fm', '~na'}, 0.4)
f5.addRow({'ndg', '~fm', 'na'}, 0.5)
f5.addRow({'ndg', '~fm', '~na'}, 0)
f5.addRow({'~ndg', 'fm', 'na'}, 0.2)
f5.addRow({'~ndg', 'fm', '~na'}, 0.6)
f5.addRow({'~ndg', '~fm', 'na'}, 0.5)
f5.addRow({'~ndg', '~fm', '~na'}, 1)

f6 = Factor()
f6.addRow({'fh', 'fs', 'fm', 'ndg'}, 0.99)
f6.addRow({'fh', 'fs', 'fm', '~ndg'}, 0.9)
f6.addRow({'fh', 'fs', '~fm', 'ndg'}, 0.75)
f6.addRow({'fh', 'fs', '~fm', '~ndg'}, 0.5)
f6.addRow({'fh', '~fs', 'fm', 'ndg'}, 0.65)
f6.addRow({'fh', '~fs', 'fm', '~ndg'}, 0.40)
f6.addRow({'fh', '~fs', '~fm', 'ndg'}, 0.2)
f6.addRow({'fh', '~fs', '~fm', '~ndg'}, 0)
f6.addRow({'~fh', 'fs', 'fm', 'ndg'}, 0.01)
f6.addRow({'~fh', 'fs', 'fm', '~ndg'}, 0.1)
f6.addRow({'~fh', 'fs', '~fm', 'ndg'}, 0.25)
f6.addRow({'~fh', 'fs', '~fm', '~ndg'}, 0.5)
f6.addRow({'~fh', '~fs', 'fm', 'ndg'}, 0.35)
f6.addRow({'~fh', '~fs', 'fm', '~ndg'}, 0.6)
f6.addRow({'~fh', '~fs', '~fm', 'ndg'}, 0.8)
f6.addRow({'~fh', '~fs', '~fm', '~ndg'}, 1)

print("Pr(FH)")
inference([f1, f2, f3, f4, f5, f6], 'fh', [], ['na', 'fm', 'fs', 'fb', 'ndg'])

print("Pr(FS | FH, FM)")
inference([f1, f2, f3, f4, f5, f6], 'fs', ['fh', 'fm'], ['na', 'fb', 'ndg'])

print("Pr(FS | FH, FM, FB)")
inference([f1, f2, f3, f4, f5, f6], 'fs', ['fh', 'fm', 'fb'], ['na', 'ndg'])

print("Pr(FS | FH, FM, FB, NA)")
inference([f1, f2, f3, f4, f5, f6], 'fs', ['fh', 'fm', 'fb', 'na'], ['ndg'])