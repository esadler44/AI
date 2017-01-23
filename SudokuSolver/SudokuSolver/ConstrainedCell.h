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
	std::list<int> previouslyTriedAssignments;
	std::list<int> remainingValidAssignments;

	bool isValidValue(int value);
	bool noNeighbourHas(int value);
	bool isCoolWithNeighbours(int value);
	bool neighbourWillTake(int value);
	void takeFromNeighbours(int value);
	void neighbourTook(int value);
	void notifyNeighboursOfGivingUp(int value);
	void neighbourGaveUp(int value);

public:
	ConstrainedCell(int row, int col, int value);

	int getRow() const;
	int getCol() const;
	bool isReadOnly() const;

	void addNeighbour(ConstrainedCell* neighbour);

	bool assignCell();
	void resetCellAssignment();
	int getValue() const;
	int getPriority() const;
};
