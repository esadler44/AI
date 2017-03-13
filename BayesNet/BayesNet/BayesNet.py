class Factor:
	def __init__(self):
		self.table = {}

	def addRow(self, setKey, prob):
		self.table[frozenset(setKey)] = prob
		
	def __str__(self):
		output = ""
		for key in sorted([sorted(list(x), key=lambda x: x[::-1]) for x in self.table.keys()]):
			output += ' '.join(keystr.rjust(2) for keystr in key)
			output += " : "
			output += str(self.table[frozenset(key)]) + '\n'
		return output

def negativeValue(value):
	if (value[0] == '~'):
		return value[1:]
	else:
		return '~' + value

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
	#Variable pass
	for frozenKey in factor.table.keys():
		if (variable in frozenKey):
			newFactor.addRow(frozenKey - {variable}, factor.table[frozenKey])
	#Negative variable pass
	negativeVariable = negativeValue(variable)
	for frozenKey in factor.table.keys():
		if (negativeVariable in frozenKey):
			newFactor.table[frozenKey - {negativeVariable}] += factor.table[frozenKey]
	return newFactor

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