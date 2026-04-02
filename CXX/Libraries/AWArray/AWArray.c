/* ARRAY LIBRARY - AMUNDWORKS - V.1 */

#define INITIAL_CAPACITY 4  // starting capacity, doubles when full

#include <stdio.h>
#include <stdlib.h>
#include "AWArray.h"

typedef struct {
    float* data;      // pointer to the actual array on the heap
    int size;         // how many elements are currently in the array
    int capacity;     // how many it can hold before needing to resize
} Array;

void InitArray(Array *a) {
    a->data = (float*)malloc(sizeof(float) * INITIAL_CAPACITY);
    if (a->data == NULL) { printf("Error: malloc failed\n"); return; }
    a->size = 0;
    a->capacity = INITIAL_CAPACITY;
}

int ArraySize(Array *l) {
    return l->size;
} 

void Append(Array *a, float data) {
    if (a->size == a->capacity) {
        a->capacity = a->capacity * 2;
    }

    a->data = (float*)realloc(a->data, sizeof(float) * a->capacity);
    if (a->data == NULL) { printf("Error: realloc failed\n"); return; }

    a->data[a->size] = data;
    a->size++;   
}

int main(void) {
    Array a;
    InitArray(&a);

    Append(&a, 1.5f);
    Append(&a, 2.5f);
    Append(&a, 3.5f);
}
