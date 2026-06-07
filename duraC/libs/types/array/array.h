/*Array prototype file - DURENDAL ENGINEERING ARRAY LIBRARY - V.1*/

#ifndef ARRAY_H
#define ARRAY_H

typedef struct {
    float* data;      // Pointer to the actual array on the heap
    int size;         // How many elements are currently in the array
    int capacity;     // How many elements it can hold 
} Array;

void InitArray(Array *a);
void PrintArray(Array *a);
void Append(Array *a, float data);
void SetValue(Array *a, int Index, float Value);
void Remove(Array *a, int Index);
void FreeArray(Array *a);

float GetValue(Array *a, int Index);
int ArraySize(Array *a);

#endif