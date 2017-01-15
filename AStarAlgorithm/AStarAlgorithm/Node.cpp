#include "stdafx.h"
#include "Node.h"

Node::Node(std::string id, double gN, double hN, std::vector<std::string> ancestors) : id(id), gN(gN), hN(hN), ancestors(ancestors) {}

std::string Node::getID() const {
	return this->id;
}

double Node::getCost() const {
	return this->gN;
}

double Node::getEstimateToGoal() const {
	return this->hN;
}

double Node::getPriority() const {
	return this->gN + this->hN;
}

bool Node::isGoalNode() const {
	return (hN == 0.0f);
}

std::vector<std::string> Node::getAncestors() const {
	return this->ancestors;
}