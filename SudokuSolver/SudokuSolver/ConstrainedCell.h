#pragma once
#include <list>

class ConstrainedCell {
public:
	static int totalCellAssignments;
private:
	static std::list<int> domain;

	int row, col;
	int currentValue;
	bool readOnly;
	std::list<ConstrainedCell*> neighbours;
	std::list<int> restrictedAssignments;
	std::list<int> previouslyTriedAssignments;
	std::list<int> remainingValidAssignments;

	bool isValidValue(int value);

public:
	ConstrainedCell(int row, int col, int value);

	int getRow() const;
	int getCol() const;
	bool isReadOnly();

	void addNeighbour(ConstrainedCell* neighbour);

	bool assignCell();
	void resetCellAssignment();
	int getValue() const;
	int getPriority() const;
};
