/*Matrix prototype file - DURENDAL ENGINEERING MATRIX LIBRARY - V.1*/

#ifndef MATRIX.H
#define MATRIX.H

typedef struct {
    float* data;      // Pointer to the actual matrix on the heap
    int rows;         // The rows of the matrix
    int cols;         // The columns of the matrix
    int capacity;     // How many elements it can hold 
} Matrix; 

void MatrixInit(Matrix *M, int rows, int cols);
void getElement(Matrix *M, int row, int col);
void setElement(Matrix *M, int row, int col, float value);

void addRow(Matrix *M);
void addCol(Matrix *M);

#endif