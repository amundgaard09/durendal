
#include <iostream>
#include <vector>
#include <chrono>

// Check if `Number` is prime
// Uses trial division to check for factors of `Number` up to the square root of `Number`.
bool IsPrime(int Number) {
    if (Number <= 1) {
        return false;
    }

    for (int i = 2; i * i < Number; ++i) {
        if (Number % i == 0) {
            return false;
        } 
    }
    return true;
}

// Main function to check for prime numbers up to `CheckStop`, and measure the time taken for the operation.
// Uses a simple loop to check each number for primality and stores the prime numbers in a vector.
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

    std::cout << "Time taken: " << duration.count() << " ms\n";
    return 0;
}