#include "stdafx.h"
#include "ConstrainedCell.h"

#include <algorithm>
#include <iostream>

using namespace std;

// PRIVATE

bool ConstrainedCell::isValidValue(int value) {
	bool result = noNeighbourHas(value);
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
		//cout << row << ":" << col << " doesn't want you to pick a " << value << endl;
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
	notifyNeighboursOfGivingUp(currentValue);
	for (int value : remainingValidAssignments) {
		if (isValidValue(value)) {
			currentValue = value;
			takeFromNeighbours(value);
			if (!readOnly) {
				totalCellAssignments++;
			}
			foundValidAssignment = true;
			break;
		}
	}
	if (foundValidAssignment) {
		remainingValidAssignments.remove(currentValue);
		previouslyTriedAssignments.push_back(currentValue);
	}
	return foundValidAssignment;
}

void ConstrainedCell::resetCellAssignment() {
	// Reset previously tried values since a higher up change may require that we try old values again
	if (!readOnly) {
		notifyNeighboursOfGivingUp(currentValue);
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
	return 0;
}
