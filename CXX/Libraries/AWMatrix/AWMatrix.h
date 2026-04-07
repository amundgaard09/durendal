/*AWMatrix prototype file - AMUNDWORKS MATRIX LIBRARY - V.1*/

#ifndef AWMATRIX.H
#define AWMATRIX.H

typedef struct {
    float* data;      // Pointer to the actual matrix on the heap
    int rows;         // The rows of the matrix
    int cols;         // The columns of the matrix
    int capacity;     // How many elements it can hold 
} Matrix; 

void InitMatrix(Matrix *M, int rows, int cols);

#endif