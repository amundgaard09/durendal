/* UTILITY LIBRARY - AMUNDWORKS - V.1 */

#include <stdio.h>
#include <stdbool.h>
#include <stdint.h>

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

uint64_t factorial(int i) {
    if (i == 0 || i == 1) {
        return 1;
    } else {
        return (i * factorial(i - 1));
    }
}
uint64_t fibonacci(int i) {
    if (i==0) {
        return 0;
    } else if (i==1) {
        return 1;
    } else {
    return fibonacci(i-1) + fibonacci(i-2);
    }
}

