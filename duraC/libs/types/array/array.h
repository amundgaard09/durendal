/*Array prototype file - DURENDAL ENGINEERING ARRAY LIBRARY - V.1*/

#ifndef ARRAY_H
#define ARRAY_H

typedef struct {
    float* data;      // Pointer to the actual array on the heap
    int size;         // How many elements are currently in the array
    int capacity;     // How many elements it can hold 
} Array;

void init_array(Array *a);
void print_array(Array *a);
void append(Array *a, float data);
void set_value(Array *a, int Index, float Value);
void array_remove(Array *a, int Index);
void free_array(Array *a);

float get_value(Array *a, int Index);
int array_size(Array *a);

#endif