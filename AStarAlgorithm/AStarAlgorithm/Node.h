#pragma once
#include <string>
#include <vector>

class Node {
private:
	std::string id;
	bool isGoal;
	double gN;
	double hN;
	std::vector<std::string> ancestors;

public:
	Node(std::string id, double gN, double hN, std::vector<std::string> ancestors);

	virtual std::string getID() const;
	virtual double getCost() const;
	virtual double getEstimateToGoal() const;
	virtual double getPriority() const;
	virtual bool isGoalNode() const;
	virtual std::vector<std::string> getAncestors() const;
};

class NodePriorityCompare {
public:
	bool operator() (const Node* lhs, const Node* rhs) const {
		double lhsPriority = lhs->getPriority();
		double rhsPriority = rhs->getPriority();
		if (lhsPriority == rhsPriority) {
			return lhs->getID() < rhs->getID();
		}
		return lhs->getPriority() < rhs->getPriority();
	}
};