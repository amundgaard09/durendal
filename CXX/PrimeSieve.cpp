#include <iostream>
#include <vector>
#include <chrono>

// Sieve of Eratosthenes
int main() {
    std::ios::sync_with_stdio(false);
    std::cin.tie(NULL);

    int CheckStop;

    std::cout << "Welcome to the Prime Checker!" << std::endl;
    std::cout << "Enter the CheckStop:" << std::endl;
    std::cin >> CheckStop;

    auto start = std::chrono::high_resolution_clock::now();

    std::vector<bool> IsPrime(CheckStop, true);
    IsPrime[0] = false;
    IsPrime[1] = false;

    for (int i = 2; i * i < CheckStop; ++i) {
        if (IsPrime[i]) {
            for (int j = i * i; j < CheckStop; j += i) {
                IsPrime[j] = false;
            }
        }
    }

    auto end = std::chrono::high_resolution_clock::now();
    auto duration = std::chrono::duration_cast<std::chrono::milliseconds>(end - start);

    for (int i = 2; i < CheckStop; ++i) {
        if (IsPrime[i]) {
            std::cout << i << "\n";
        }
    }

    std::cout << "Time taken" << duration.count() << "ms\n";
    return 0;
}