
#include <chrono>
#include <iostream>
#include <vector>
#include "../Libraries/AWUtils/AWUtils.h"

int main() {
    std::ios::sync_with_stdio(false);
    std::cin.tie(NULL);

    int CheckStop;

    std::cout << "Welcome to the Prime Checker!" << std::endl;
    std::cout << "Enter the CheckStop:" << std::endl;
    std::cin >> CheckStop;

    std::vector<int> PrimeArray;

    auto start = std::chrono::high_resolution_clock::now();

    for (int idx = 2; idx < CheckStop; ++idx) {
        if (IsPrime(idx)) {
            PrimeArray.push_back(idx);
        }
    }

    auto end = std::chrono::high_resolution_clock::now();
    auto duration = std::chrono::duration_cast<std::chrono::milliseconds>(end - start);

    for (int n : PrimeArray) {
        std::cout << n << "\n";
    }

    std::cout << "Time taken" << duration.count() << "ms\n";
    return 0;
}