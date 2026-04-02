/*AWArray prototype file - AMUNDWORKS ARRAY LIBRARY - V.1*/

#ifndef AWARRAY_H
#define AWARRAY_H

typedef struct {
    float* data;      // Pointer to the actual array on the heap
    int size;         // How many elements are currently in the array
    int capacity;     // How many elements it can hold 
} Array;

void InitArray(Array *a);
int ArraySize(Array *a);
void Append(Array *a, float value);
void PrintArray(Array *a);

#endif