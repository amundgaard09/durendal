/* ALGORITHMS LIBRARY - AMUNDWORKS - V.1 */

#include <stdio.h>
#include <stdbool.h>
#include <stdint.h>
#include "../datatypes/dl_list/dllist.h"

// Check if `Number` is prime via trial division up to the square root of `Number` 
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

// Return a `DLList` constisting of the prime factors of `Number`
DLList PrimeFactorize(int Number) {
    DLList factors;
    InitList(&factors);

    if (Number <= 1) return factors;

    int divisor = 2;

    while (divisor * divisor <= Number) {
        while (Number % divisor == 0) {
            InsertAtBack(&factors, divisor);
            Number /= divisor;
        }
        divisor++;
    }

    if (Number > 1) {
        InsertAtBack(&factors, Number);
    }

    return factors;
}

// Return the factorial of `I`
uint64_t Factorial(int I) {
    if (I == 0 || I == 1) {
        return 1;
    } else {
        return (I * Factorial(I - 1));
    }
}

// Return the fibonacci number at index `I`
uint64_t Fibonacci(int I) {
    if (I==0) {
        return 0;
    } else if (I==1) {
        return 1;
    } else {
    return Fibonacci(I-1) + Fibonacci(I-2);
    }
}
