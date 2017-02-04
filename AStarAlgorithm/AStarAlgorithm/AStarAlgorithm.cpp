// AStarAlgorithm.cpp : Defines the entry point for the console application.
//

#include "stdafx.h"
#include "Node.h"

#include <cmath>
#include <ctime>
#include <iostream>
#include <fstream>
#include <queue>
#include <string>
#include <unordered_map>
#include <vector>

using namespace std;

struct StateData {
	string id;
	int x, y;
};

double successorCost(StateData a, StateData b) {
	return sqrt(pow(a.x - b.x, 2.0) + pow(a.y - b.y, 2.0));
}

int solveProblem(int i, int j) {
	vector<string> stateIDs;
	unordered_map<string, StateData> stateDataMap;
	StateData originStateData;
	StateData neighbourStateData;
	int numStates = 0;
	double cheapestSuccessor = 0.0f;

	ifstream testFile;
	testFile.open("C:\\Users\\Elliot\\Documents\\4B Term\\CS 486\\A1\\randTSP\\" + to_string(i) + "\\instance_" + to_string(j) + ".txt");

	int lines;
	testFile >> lines;
	for (int i = 0; i < lines; i++) {
		string stateID;
		int x, y;
		testFile >> stateID >> x >> y;

		StateData stateData;
		stateData.id = stateID;
		stateData.x = x;
		stateData.y = y;

		if (i == 0) {
			originStateData = stateData;
		}
		else if (i == 1) {
			neighbourStateData = stateData;
		}

		stateIDs.push_back(stateID);
		stateDataMap[stateID] = stateData;
		numStates++;
	}
	if (numStates > 1) {
		cheapestSuccessor = successorCost(originStateData, neighbourStateData);

		for (unordered_map<string, StateData>::iterator it = stateDataMap.begin(); it != stateDataMap.end(); it++) {
			for (unordered_map<string, StateData>::iterator itt = stateDataMap.begin(); itt != stateDataMap.end(); itt++) {
				if (it->first == itt->first) {
					continue;
				}
				double distance = successorCost(it->second, itt->second);
				if (distance < cheapestSuccessor) {
					cheapestSuccessor = distance;
				}
			}
		}
	}

	int generatedNodes = 0;

	vector<string> empty;
	Node* firstNode = new Node(originStateData.id, 0.0f, numStates * cheapestSuccessor, empty);
	generatedNodes++;

	priority_queue<Node*, vector<Node*>, NodePriorityCompare> priorityQueue;
	priorityQueue.push(firstNode);

	Node *expansionCandidate;
	while (true) {
		expansionCandidate = priorityQueue.top();
		priorityQueue.pop();
		// If we are about to expand a goal node then we have our shortest path
		if (expansionCandidate->isGoalNode()) {
			break;
		}
		// Expand it
		vector<string> ancestors = expansionCandidate->getAncestors();
		ancestors.push_back(expansionCandidate->getID());
		vector<string> remainingNodeIDs;
		for (string id : stateIDs) {
			// Look for each ID in the list of ancestors
			if (std::find(ancestors.begin(), ancestors.end(), id) == ancestors.end()) { // If we haven't come across it already, we can add it
				remainingNodeIDs.push_back(id);
			}
		}
		// If we've completed a tour of all the states, we need to add the origin state back to return to it
		if (remainingNodeIDs.empty()) {
			remainingNodeIDs.push_back(originStateData.id);
		}
		int numRemainingPaths = numStates - ancestors.size();
		StateData expandedStateData = stateDataMap[expansionCandidate->getID()];
		for (string id : remainingNodeIDs) {
			StateData newLeafStateData = stateDataMap[id];
			double costToNewLeaf = successorCost(expandedStateData, newLeafStateData);
			Node* newLeafNode = new Node(id, expansionCandidate->getCost() + costToNewLeaf, numRemainingPaths * cheapestSuccessor, ancestors);
			generatedNodes++;
			priorityQueue.push(newLeafNode);
		}
	}

	cout << "Clock Time: " << clock() << endl;
	cout << "Generated Nodes: " << generatedNodes << endl;

	//cout << "Path: ";
	vector<string> path = expansionCandidate->getAncestors();
	for (vector<string>::iterator it = path.begin(); it != path.end(); it++) {
		//cout << *it << " ";
	}
	//cout << expansionCandidate->getID() << endl;

	//cout << "Cost: " << expansionCandidate->getCost() << endl;
	cin.get();
	return generatedNodes;
}

int main()
{
	for (int i = 9; i <= 9; i++) {
		float avg = 0;
		for (int j = 1; j <= 1; j++) {
			int result = solveProblem(i, j);
			avg += result / 10.0f;
			cout << result << endl;
		}
		cout << i << ", " << avg << endl;
	}
	cin.get();
    return 0;
}

