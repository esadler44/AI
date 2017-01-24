#include "stdafx.h"
#include "ConstrainedCell.h"

#include <algorithm>
#include <iostream>

using namespace std;

// PRIVATE

bool ConstrainedCell::isValidValue(int value) {
	bool result = noNeighbourHas(value);
	// Comment out for pure backtracking
	result &= isCoolWithNeighbours(value);
	return result;
}

bool ConstrainedCell::noNeighbourHas(int value) {
	bool result = true;
	for (ConstrainedCell* neighbour : neighbours) {
		if (neighbour->getValue() == value) {
			result = false;
			break;
		}
	}
	return result;
}

bool ConstrainedCell::isCoolWithNeighbours(int value) {
	bool result = true;
	for (ConstrainedCell* neighbour : neighbours) {
		if (!neighbour->neighbourWillTake(value)) {
			result = false;
			break;
		}
	}
	return result;
}

bool ConstrainedCell::neighbourWillTake(int value) {
	if (currentValue != 0) {
		return true;
	}
	// If we would remove the last possible value from somebody don't do it
	if (remainingValidAssignments.size() == 1 && remainingValidAssignments.back() == value) {
		return false;
	} else { // We still have at least one choice
		return true;
	}
}

void ConstrainedCell::takeFromNeighbours(int value) {
	for (ConstrainedCell* neighbour : neighbours) {
		neighbour->neighbourTook(value);
	}
}

void ConstrainedCell::neighbourTook(int value) {
	// If this value was previously available to us, remove it
	list<int>::iterator found = find(remainingValidAssignments.begin(), remainingValidAssignments.end(), value);
	if (found != remainingValidAssignments.end()) {
		remainingValidAssignments.erase(found);
	}
}

void ConstrainedCell::notifyNeighboursOfGivingUp(int value) {
	if (value == 0) {
		return;
	}
	currentValue = 0;
	for (ConstrainedCell* neighbour : neighbours) {
		neighbour->neighbourGaveUp(value);
	}
}

void ConstrainedCell::neighbourGaveUp(int value) {
	// If nobody is further restricting it we can use it again
	if (noNeighbourHas(value)) {
		// Must check that we haven't already tried to use it
		if (find(previouslyTriedAssignments.begin(), previouslyTriedAssignments.end(), value) == previouslyTriedAssignments.end()) {
			remainingValidAssignments.push_back(value);
		}
	}
}

int ConstrainedCell::totalConstrainedNeighboursWhenTaken(int value) {
	int totalConstrainments = 0;
	for (ConstrainedCell* neighbour : neighbours) {
		if (neighbour->willNeighbourConstrainWith(value)) {
			totalConstrainments++;
		}
	}
	return totalConstrainments;
}

bool ConstrainedCell::willNeighbourConstrainWith(int value) {
	if (currentValue != 0) { // Don't count towards assigned variables, as per slides
		return false;
	} else if (find(remainingValidAssignments.begin(), remainingValidAssignments.end(), value) != remainingValidAssignments.end()) { // We will get constrained by this choice
		return true;
	} else {
		return false;
	}
}

// PUBLIC

ConstrainedCell::ConstrainedCell(int row, int col, int value) : row(row), col(col) {
	readOnly = (value != 0);
	currentValue = 0;
	if (!readOnly) {
		remainingValidAssignments = domain;
	} else {
		remainingValidAssignments.push_back(value);
	}
}

int ConstrainedCell::getRow() const {
	return row;
}

int ConstrainedCell::getCol() const {
	return col;
}

bool ConstrainedCell::isReadOnly() const {
	return readOnly;
}

void ConstrainedCell::addNeighbour(ConstrainedCell* neighbour) {
	if (find(neighbours.begin(), neighbours.end(), neighbour) == neighbours.end()) {
		neighbours.push_back(neighbour);
	}
}

bool ConstrainedCell::assignCell() {
	bool foundValidAssignment = false;
	// Comment out for pure backtracking
	notifyNeighboursOfGivingUp(currentValue);
	int minNeighboursRestrained;
	int leastRestrainingValue = 0;
	for (int value : remainingValidAssignments) {
		if (isValidValue(value)) {
			// Comment out for no heuristics
			/**/
			int numNeighboursRestrained = totalConstrainedNeighboursWhenTaken(value);
			if (leastRestrainingValue == 0) {
				minNeighboursRestrained = numNeighboursRestrained;
				leastRestrainingValue = value;
			} else if (numNeighboursRestrained < minNeighboursRestrained) {
				minNeighboursRestrained = numNeighboursRestrained;
				leastRestrainingValue = value;
			}
			/**/
			// End comment
			foundValidAssignment = true;
			// Comment in for no heuristics
			/*
			leastRestrainingValue = value;
			break;
			*/
		}
	}
	if (foundValidAssignment) {
		currentValue = leastRestrainingValue;
		// Comment out for pure backtracking
		takeFromNeighbours(currentValue);
		if (!readOnly) {
			totalCellAssignments++;
		}
		remainingValidAssignments.remove(currentValue);
		previouslyTriedAssignments.push_back(currentValue);
	}
	return foundValidAssignment;
}

void ConstrainedCell::resetCellAssignment() {
	// Reset previously tried values since a higher up change may require that we try old values again
	if (!readOnly) {
		// Comment out for pure backtracking
		notifyNeighboursOfGivingUp(currentValue);
		// Comment in for pure backtracking
		//currentValue = 0;
		while (!previouslyTriedAssignments.empty()) {
			remainingValidAssignments.push_back(previouslyTriedAssignments.back());
			previouslyTriedAssignments.pop_back();
		}
	}
}

int ConstrainedCell::getValue() const {
	return currentValue;
}

int ConstrainedCell::getPriority() const {
	// Comment out for no heuristics
	//return 0;
	// Comment in for heuristics
	/**/
	int remainingValuesInverted = (domain.size() - remainingValidAssignments.size()) * 21;
	int neighboursToConstrain = 0;
	// Everybody should have 20 neighbours
	for (ConstrainedCell* neighbour : neighbours) {
		if (neighbour->getValue() == 0) {
			neighboursToConstrain++;
		}
	}
	return (remainingValuesInverted + neighboursToConstrain);
	/**/
	// End comment
}
