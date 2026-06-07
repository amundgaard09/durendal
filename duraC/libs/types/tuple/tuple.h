/* Tuple prototype file - DURENDAL ENGINEERING MATRIX LIBRARY - V.1 */

#ifndef TUPLE.H
#define TUPLE.H

#include <stdlib.h>

#define INITIAL_CAPACITY 4

// A tuple with a capacity of 10 - simple first iteration
typedef struct {
    float i[10];
} decatuple;

// a dynamic tuple data type that automatically expands and shrinks as needed
typedef struct {
    void **elements;
    size_t size;
} dynatuple;

dynatuple* create_dynatuple();
void FreeDynatuple(dynatuple *tpl);

#endif