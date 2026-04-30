/*Matrix prototype file - AMUNDWORKS MATRIX LIBRARY - V.1*/

#ifndef MATRIX.H
#define MATRIX.H

typedef struct {
    float* data;      // Pointer to the actual matrix on the heap
    int rows;         // The rows of the matrix
    int cols;         // The columns of the matrix
    int capacity;     // How many elements it can hold 
} Matrix; 

void MatrixInit(Matrix *M, int rows, int cols);
void GetElement(Matrix *M, int row, int col);
void SetElement(Matrix *M, int row, int col);

#endif