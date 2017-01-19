#include "stdafx.h"
#include "ConstrainedCell.h"

#include <algorithm>

using namespace std;

// PRIVATE

bool ConstrainedCell::isValidValue(int value) {
	bool result = true;
	for (ConstrainedCell* neighbour : neighbours) {
		if (neighbour->getValue() == value) {
			result = false;
			break;
		}
	}
	return result;
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

int ConstrainedCell::getRow() const
{
	return row;
}

int ConstrainedCell::getCol() const
{
	return col;
}

bool ConstrainedCell::isReadOnly()
{
	return readOnly;
}

void ConstrainedCell::addNeighbour(ConstrainedCell* neighbour) {
	neighbours.push_back(neighbour);
}

bool ConstrainedCell::assignCell() {
	bool foundValidAssignment = false;
	for (int value : remainingValidAssignments) {
		if (isValidValue(value)) {
			currentValue = value;
			if (!readOnly) {
				totalCellAssignments++;
			}
			foundValidAssignment = true;
			break;
		}
	}
	if (foundValidAssignment) {
		remainingValidAssignments.erase(remove(remainingValidAssignments.begin(), remainingValidAssignments.end(), currentValue), remainingValidAssignments.end());
		previouslyTriedAssignments.push_back(currentValue);
	}
	return foundValidAssignment;
}

void ConstrainedCell::resetCellAssignment() {
	// Reset previously tried values since a higher up change may require that we try old values again
	if (!readOnly) {
		currentValue = 0;
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
