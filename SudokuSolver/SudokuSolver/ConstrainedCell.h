#pragma once
#include <vector>

class ConstrainedCell {
public:
	static int totalCellAssignments;
private:
	static std::vector<int> domain;

	int row, col;
	int currentValue;
	bool readOnly;
	std::vector<ConstrainedCell*> neighbours;
	std::vector<int> restrictedAssignments;
	std::vector<int> previouslyTriedAssignments;
	std::vector<int> remainingValidAssignments;

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
