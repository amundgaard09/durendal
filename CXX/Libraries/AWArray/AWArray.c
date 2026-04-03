/* AWARRAY LIBRARY - AMUNDWORKS - V.1 */

#define INITIAL_CAPACITY 4  // starting capacity, doubles when full

#include <stdio.h>
#include <stdlib.h>
#include "AWArray.h"

void InitArray(Array *a) {
    a->data = (float*)malloc(sizeof(float) * INITIAL_CAPACITY);
    if (a->data == NULL) { printf("Error: malloc failed\n"); return; }
    a->size = 0;
    a->capacity = INITIAL_CAPACITY;
}
void PrintArray(Array *a) {
    printf("[");
    for (int i = 0; i < a->size; i++) {
        printf("%.2f", a->data[i]);
        if (i < a->size - 1) {
            printf(", ");
        }
    }
    printf("]\n");
}

void Append(Array *a, float data) {
    if (a->size == a->capacity) {
        a->capacity = a->capacity * 2;
        a->data = (float*)realloc(a->data, sizeof(float) * a->capacity);
        if (a->data == NULL) { printf("Error: realloc failed\n"); return; }
    }

    a->data[a->size] = data;
    a->size++;   
}
void SetValue(Array *a, int Index, float Value) {
    if (Index < 0 || Index >= a->size) {
        printf("Error: index out of range\n");
        return;
    }

    a->data[Index] = Value;
}
void Remove(Array *a, int Index) {
    if (Index < 0 || Index >= a->size) {
        printf("Error: index out of range\n");
        return;
    }

    for (int idx = Index; idx < a->size - 1; idx++) {
        a->data[idx] = a->data[idx + 1];
    }

    a->size--;
}
void FreeArray(Array *a) {
    free(a->data);
    a->data = NULL;
    a->size = 0;
    a->capacity = 0;
}

float GetValue(Array *a, int Index) {
    if (Index < 0 || Index >= a->size) {
        printf("Error: index out of range\n");
        return -1;
    }
    return a->data[Index];
}

int ArraySize(Array *a) {
    return a->size;
} 

int main(void) {
    Array a;
    InitArray(&a);

    Append(&a, 1.5f);
    Append(&a, 2.5f);
    Append(&a, 3.5f);

    PrintArray(&a);
}
