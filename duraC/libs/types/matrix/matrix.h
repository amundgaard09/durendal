/*Matrix prototype file - DURENDAL ENGINEERING MATRIX LIBRARY - V.1*/

#include "../vector/vector.h"

#ifndef MATRIX_H
#define MATRIX_H

typedef struct {
    float* data;      // Pointer to the actual matrix on the heap
    int rows;         // The rows of the matrix
    int cols;         // The columns of the matrix
    int capacity;     // How many elements it can hold 
} Matrix; 

void init_matrix(Matrix *M, int rows, int cols);
void get_dims(Matrix *M);

float get_element(Matrix *M, int row, int col);
void set_element(Matrix *M, int row, int col, float value);
void print_matrix(Matrix *M);

void add_row(Matrix *M);
void add_col(Matrix *M);

Vector matvec_multiply(Matrix *A, Vector *B);
Matrix matrix_multiply(Matrix *A, Matrix *B);

#endif