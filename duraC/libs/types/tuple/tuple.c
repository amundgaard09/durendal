/* TUPLE LIBRARY - DURENDAL ENGINEERING - V.1*/

#include <stdlib.h>
#include "tuple.h"

#define INITIAL_CAPACITY 4

// Free the given dynatuple
void FreeDynatuple(dynatuple *t) {
    return;
}

// Create a new dynatuple
dynatuple* create_dynatuple() {
    dynatuple *t = malloc(sizeof(dynatuple));
    t->elements = NULL;
    t->size = 0;
    return t;
}

// Append an element to the tuple
void append_tuple(dynatuple *t, void *element) {
    t->size++;
    t->elements = realloc(t->elements, t->size * sizeof(void *));
    t->elements[t->size - 1] = element;
}