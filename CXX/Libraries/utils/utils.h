/* Utils prototype file - AMUNDWORKS UTILITIES LIBRARY - V.1*/

#include <stdint.h>
#include "../datatypes/dl_list/dllist.h"

#ifndef UTILS.H
#define UTILS.H

bool IsPrime(int Number);
DLList PrimeFactorize(int Number);
uint64_t Factorial(int I);
uint64_t Fibonacci(int I);

#endif