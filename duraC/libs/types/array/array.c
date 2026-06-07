/* ARRAY LIBRARY - DURENDAL ENGINEERING - V.1 */

#define INITIAL_CAPACITY 4  // starting capacity, doubles when full

#include <stdio.h>
#include <stdlib.h>
#include "array.h"

void init_array(Array *a) {
    a->data = (float*)malloc(sizeof(float) * INITIAL_CAPACITY);
    if (a->data == NULL) { printf("Error: malloc failed\n"); return; }
    a->size = 0;
    a->capacity = INITIAL_CAPACITY;
}

void print_array(Array *a) {
    printf("[");
    for (int i = 0; i < a->size; i++) {
        printf("%.2f", a->data[i]);
        if (i < a->size - 1) {
            printf(", ");
        }
    }
    printf("]\n");
}

void append(Array *a, float data) {
    if (a->size == a->capacity) {
        a->capacity = a->capacity * 2;
        a->data = (float*)realloc(a->data, sizeof(float) * a->capacity);
        if (a->data == NULL) { printf("Error: realloc failed\n"); return; }
    }

    a->data[a->size] = data;
    a->size++;   
}

float get_value(Array *a, int idx) {
    if (idx < 0 || idx >= a->size) {
        printf("Error: index out of range\n");
        return -1;
    }
    return a->data[idx];
}

void set_value(Array *a, int idx, float value) {
    if (idx < 0 || idx >= a->size) {
        printf("Error: index out of range\n");
        return;
    }

    a->data[idx] = value;
}
void array_remove(Array *a, int idx) {
    if (idx < 0 || idx >= a->size) {
        printf("Error: index out of range\n");
        return;
    }

    for (int idx = idx; idx < a->size - 1; idx++) {
        a->data[idx] = a->data[idx + 1];
    }

    a->size--;
}
void free_array(Array *a) {
    free(a->data);
    a->data = NULL;
    a->size = 0;
    a->capacity = 0;
}

int array_size(Array *a) {
    return a->size;
} 

int main(void) {
    Array a;
    init_array(&a);

    append(&a, 1.5f);
    append(&a, 2.5f);
    append(&a, 3.5f);

    print_array(&a);
}
