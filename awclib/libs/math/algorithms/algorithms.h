/* Algorithms prototype file - AMUNDWORKS ALGORITHMS LIBRARY - V.1*/

#include <stdint.h>
#include "../../types/dl_list/dllist.h"

#ifndef ALGORITHMS.H
#define ALGORITHMS.H

bool IsPrime(int Number);
DLList PrimeFactorize(int Number);
uint64_t Factorial(int I);
uint64_t Fibonacci(int I);

#endif