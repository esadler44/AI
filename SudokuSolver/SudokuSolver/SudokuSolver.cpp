// SudokuSolver.cpp : Defines the entry point for the console application.
//

#include "stdafx.h"
#include "ConstrainedCell.h"

#include <fstream>
#include <iostream>
#include <string>

using namespace std;

list<int> ConstrainedCell::domain = { 1, 2, 3, 4, 5, 6, 7, 8, 9 };
int ConstrainedCell::totalCellAssignments = 0;

int solveProblem(string filePath);

int main() {
	ofstream outputFile;
	outputFile.open("backtrackWFwdResults.txt");
	outputFile << "Empty Cells, BacktrackFW Assignments" << endl;
	for (int i = 71; i >= 1; i--) {
		cout << "Problem: " << i << endl;
		outputFile << i;
		float average = 0;
		for (int j = 1; j <= 10; j++) {
			string file = "C:\\Users\\Elliot\\Documents\\4B Term\\CS 486\\A1\\problems\\" + to_string(i) + "\\" + to_string(j) + ".sd";
			int result = solveProblem(file);
			if (result < 0) {
				cout << "FOLDER " << i << ", RUN " << j << " IMPOSSIBLE!!!" << endl;
			} else {
				average += result / 10.0f;
			}
			//cout << result << endl;
			//cin.get();
		}
		cout << "Avg: " << average << endl;
		outputFile << ", " << average << endl;
		//cin.get();
	}
	outputFile.close();
}

int solveProblem(string filePath)
{
	ConstrainedCell* cells[9][9];

	ifstream testFile;
	testFile.open(filePath);

	list<ConstrainedCell*> givenCells;
	list<ConstrainedCell*> needAssigning;

	// Create grid
	int num;
	ConstrainedCell::totalCellAssignments = 0;
	for (int i = 0; i < 9; i++) {
		for (int j = 0; j < 9; j++) {
			testFile >> num;
			ConstrainedCell* cell = new ConstrainedCell(i, j, num);
			cells[i][j] = cell;
			if (num == 0) {
				needAssigning.push_back(cell);
			}
			else {
				givenCells.push_back(cell);
			}
		}
	}

	// Assign neighbours
	for (int i = 0; i < 9; i++) {
		for (int j = 0; j < 9; j++) {
			ConstrainedCell* cell = cells[i][j];
			// Add other cells in same row
			for (int col = 0; col < 9; col++) {
				if (col == j) {
					continue;
				}
				cell->addNeighbour(cells[i][col]);
			}
			// Add other cells in same col
			for (int row = 0; row < 9; row++) {
				if (row == i) {
					continue;
				}
				cell->addNeighbour(cells[row][j]);
			}
			// Add other cells in same block
			int topCornerBlockRow = i / 3;
			int topCornerBlockCol = j / 3;
			for (int blockRow = 0; blockRow < 3; blockRow++) {
				for (int blockCol = 0; blockCol < 3; blockCol++) {
					int cellLocRow = (topCornerBlockRow * 3) + blockRow;
					int cellLocCol = (topCornerBlockCol * 3) + blockCol;
					if (cellLocRow == i && cellLocCol == j) {
						continue;
					}
					cell->addNeighbour(cells[cellLocRow][cellLocCol]);
				}
			}
		}
	}

	// State
	bool impossible = false;

	// Assign given cells
	for (ConstrainedCell* cell : givenCells) {
		if (!cell->assignCell()) {
			impossible = true;
		}
	}

	// Assign remaining cells
	if (!impossible) {
		list<ConstrainedCell*> attemptedAssignments;
		list<ConstrainedCell*> resetCells;
		while (!needAssigning.empty()) {
			if (ConstrainedCell::totalCellAssignments > 10000) {
				break;
			}
			//cout << "Total Assignments: " << ConstrainedCell::totalCellAssignments << endl;
			//cout << "Remaining cells to assign: " << needAssigning.size() << endl;
			//cout << "Grid:" << endl;
			for (int i = 0; i < 9; i++) {
				for (int j = 0; j < 9; j++) {
					//cout << cells[i][j]->getValue() << " ";
				}
				//cout << endl;
			}
			// Get cell with highest priority
			ConstrainedCell* cell = needAssigning.back();
			for (ConstrainedCell* possibleCell : needAssigning) {
				if (possibleCell->getPriority() >= cell->getPriority()) {
					cell = possibleCell;
				}
			}
			needAssigning.remove(cell);
			//cout << "Top Cell: (row:" << cell->getRow() << ", col:" << cell->getCol() << ")" << endl;
			bool assigned = cell->assignCell();
			if (assigned) {
				attemptedAssignments.push_back(cell);
			}
			// Reverse back up through previous assignments until we can re-assign one or we get to the root of the assignment tree
			while (!assigned) {
				//cout << "Unassigned" << endl;
				if (attemptedAssignments.empty()) {
					impossible = true;
					break;
				}
				else {
					cell->resetCellAssignment();
					needAssigning.push_back(cell);
					cell = attemptedAssignments.back();
					//cout << "Reassigning Cell: (row:" << cell->getRow() << ", col:" << cell->getCol() << ")" << endl;
					attemptedAssignments.pop_back();
					assigned = cell->assignCell();
					if (assigned) {
						//cout << "REASSIGNED" << endl;
						attemptedAssignments.push_back(cell);
					} else {
						//cout << "NO VALID REASSIGNMENT" << endl;
					}
				}
			}
			//cin.get();
		}
	}

	// Results
	//cout << "Total Assignments: " << ConstrainedCell::totalCellAssignments << endl;
	//cout << "Result: " << (impossible ? "FAIL" : "PASS") << endl;
	if (!impossible) {
		for (int i = 0; i < 9; i++) {
			for (int j = 0; j < 9; j++) {
				//cout << cells[i][j]->getValue() << " ";
			}
			//cout << endl;
		}
	}

	// Clean up
	for (int i = 0; i < 9; i++) {
		for (int j = 0; j < 9; j++) {
			delete(cells[i][j]);
		}
	}

	// Results
	if (impossible) {
		return -1;
	} else {
		return ConstrainedCell::totalCellAssignments;
	}
}

