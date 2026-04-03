/* MATRIX LIBRARY - AMUNDWORKS - V.1 */

#include <stdio.h>
#include <stdlib.h>
#include "AWMatrix.h"

#define INITIAL_CAPACITY 4

void InitMatrix(Matrix *M, int rows, int cols) {
    M->data = (float*)malloc(sizeof(float) * INITIAL_CAPACITY);
    if (M->data == NULL) { printf("Error: malloc failed\n"); return; }
    M->rows = rows;
    M->cols = cols;
    M->capacity = INITIAL_CAPACITY;
}