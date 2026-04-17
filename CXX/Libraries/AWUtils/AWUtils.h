/*AWUtils prototype file - AMUNDWORKS UTILITIES LIBRARY - V.1*/

#include <stdint.h>
#include "../AWList/AWList.h"

#ifndef AWUTILS.H
#define AWUTILS.H

bool IsPrime(int Number);
DLList PrimeFactorize(int Number);
uint64_t factorial(int I);
uint64_t fibonacci(int I);

#endif