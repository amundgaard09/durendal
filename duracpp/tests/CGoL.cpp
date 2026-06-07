
#include <iostream>
#include <string>
#include <vector>
#include <chrono>
#include <thread>

// 9x9 grid
std::vector<std::vector<char>> grid(9, std::vector<char>(9, '.'));

int CheckNeighborCount(std::vector<int> CharCoordinate, std::vector<std::vector<char>>& grid, bool IsSelfAlive) {
    int CellRow = CharCoordinate[0];
    int CellCol = CharCoordinate[1];
    int AliveNeighbors = 0;

    for (int i = CellRow - 1; i < CellRow + 2; i++) {
        for (int j = CellCol - 1; j < CellCol + 2; j++) {
            if (i >= 0 && i < grid.size() && j >= 0 && j < grid[0].size() && grid[i][j] == '#') {
                AliveNeighbors += 1;
            }
        }
    }

    if (IsSelfAlive) {
        AliveNeighbors -= 1;
    }

    return AliveNeighbors;
}

//per tick update (1 Hz tick)
void Update(std::vector<std::vector<char>>& grid) {
    std::vector<std::vector<char>> newGrid = grid;

    for (int row = 0; row < grid.size(); row++) {
        for (int col = 0; col < grid[row].size(); col++) {
            std::vector<int> Coordinate = {row, col};
            bool IsSelfAlive = grid[row][col] == '#';
            int Neighbors = CheckNeighborCount(Coordinate, grid, IsSelfAlive);

            if (IsSelfAlive && (Neighbors < 2 || Neighbors > 3))
                newGrid[row][col] = '.';
            else if (IsSelfAlive && (Neighbors == 2 || Neighbors == 3))
                newGrid[row][col] = '#';
            else if (!IsSelfAlive && Neighbors == 3)
                newGrid[row][col] = '#';
            else
                newGrid[row][col] = '.';
        }
    }

    grid = newGrid; 
}

void PrintGrid(std::vector<std::vector<char>>& grid){
    for (int row = 0; row < grid.size(); row++) {
        for (int col = 0; col < grid[row].size(); col++) {
            std::cout << grid[row][col];
        }
        std::cout << "\n";
    }
}

int main() {
    grid[4][3] = '#';
    grid[4][4] = '#';
    grid[4][5] = '#'; 

    while (true) {
        system("cls");
        PrintGrid(grid);
        Update(grid);
        std::this_thread::sleep_for(std::chrono::milliseconds(250));
    }

    return 0;
}