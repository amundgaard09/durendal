/* MATRIX LIBRARY - DURENDAL ENGINEERING - V.1 */

#include <stdio.h>
#include <stdlib.h>
#include "matrix.h"
#include "../tuple/tuple.h"

#define INITIAL_CAPACITY 4

void MatrixInit(Matrix *M, int rows, int cols) {
    M->data = (float*)malloc(sizeof(float) * INITIAL_CAPACITY);
    if (M->data == NULL) { printf("Error: malloc failed\n"); return; }
    M->rows = rows;
    M->cols = cols;
    M->capacity = INITIAL_CAPACITY;
}

void getDimensions(Matrix *M) {
    int Dimensions = {M->rows, M->cols};
    return Dimensions;
}

void getElement(Matrix *M, int row, int col) {
    if (row < 0 || row >= M->rows || col < 0 || col >= M->cols) {
        printf("Error: index out of range\n");
        return;
    }

    return M->data[row * M->cols + col];
}
void setElement(Matrix *M, int row, int col, float value) {
    if (row < 0 || row >= M->rows || col < 0 || col >= M->cols) {
        printf("Error: index out of range\n");
        return;
    }

    M->data[row * M->cols + col] = value;
    return;
}

void addRow(Matrix *M) {
    M->rows++;
}
void addCol(Matrix *M) {
    M->cols++;
}

