
#include <vector>
#include "primality.hpp"

// Check if `Number` is prime
// Uses trial division to check for factors of `Number` up to the square root of `Number`.
bool isprime(int Number) {
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

std::vector<int> primefactorize(int Number) {
    std::vector<int> Factors;
    int divisor = 2;

    if (Number <= 1) return Factors;
    
    while (divisor * divisor <= Number) {
        while (Number % divisor == 0) {
            Factors.push_back(divisor);
            Number /= divisor;
        }
        divisor++;
    }

    if (Number > 1) { Factors.push_back(Number); }
    return Factors;
}