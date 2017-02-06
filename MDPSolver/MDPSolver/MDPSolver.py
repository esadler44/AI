from functools import partial
from statistics import mean

class Edge(object):
	def __init__(self, prob, node):
		self.prob = prob
		self.node = node

class Node(object):
	def __init__(self, name, value):
		self.name = name
		self.value = value
		self.edges = {}

	def addEdge(self, action, edge):
		if (action in self.edges):
			self.edges[action].append(edge)
		else:
			self.edges[action] = [edge]

def solveMDP(nodes, discountFactor, epsilon):
	rewards = {}
	prevValues = {}
	optimalPolicy = {}
	avgValueChange = float("inf")
	while avgValueChange > epsilon:
		if (not prevValues):
			for node in nodes:
				prevValues[node.name] = node.value
			rewards = prevValues.copy()
		else:
			newValues = prevValues.copy()
			for node in nodes: #Si
				bestDecision = None
				bestDecisionValue = None
				for decision in node.edges.keys(): #k
					expectedFutureValue = 0
					for edge in node.edges[decision]: #j
						expectedFutureValue += (edge.prob * prevValues[edge.node.name])
					value = rewards[node.name] + (discountFactor*expectedFutureValue)
					if (not bestDecisionValue or value > bestDecisionValue):
						bestDecision = decision
						bestDecisionValue = value
				optimalPolicy[node.name] = bestDecision
				newValues[node.name] = bestDecisionValue
			avgValueChange = mean([abs(new-old) for new, old in zip(newValues.values(), prevValues.values())])
			print(avgValueChange)
			prevValues = newValues
	return prevValues, optimalPolicy

epsilon = 0.0001

y = 0.95
ps = 0.2
pr = 0.01898858

s1 = Node("s1", 0)
s2 = Node("s2", 0)
s3 = Node("s3", 0)
s4 = Node("s4", 10)
s5 = Node("s5", -10)

s1.addEdge("a", Edge(0.9, s2))
s1.addEdge("a", Edge(0.1, s1))
s1.addEdge("b", Edge(0.9, s3))
s1.addEdge("b", Edge(0.1, s1))

s2.addEdge("d", Edge(ps, s2))
s2.addEdge("d", Edge(1 - ps, s4))

s3.addEdge("d", Edge(pr, s5))
s3.addEdge("d", Edge(0.9 - pr, s4))
s3.addEdge("d", Edge(0.1, s3))

s4.addEdge("d", Edge(0.9, s1))
s4.addEdge("d", Edge(0.1, s4))

s5.addEdge("d", Edge(0.9, s1))
s5.addEdge("d", Edge(0.1, s5))

nodes = [s1, s2, s3, s4, s5]

#I think there's a race condition because when stepped through there isn't a problem, and some runs will not converge to 0
valueFunction, optimalPolicy = solveMDP(nodes, y, epsilon)
print(valueFunction)
print(optimalPolicy)