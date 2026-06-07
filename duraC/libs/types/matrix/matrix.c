/* MATRIX LIBRARY - DURENDAL ENGINEERING - V.1 */

#include <stdio.h>
#include <stdlib.h>
#include "matrix.h"

#define INITIAL_CAPACITY 4

void init_matrix(Matrix *M, int rows, int cols) {
    int capacity = (rows > 0 && cols > 0) ? rows * cols : INITIAL_CAPACITY;
    M->data = (float*)calloc(capacity, sizeof(float));
    if (M->data == NULL) { printf("Error: calloc failed\n"); return; }
    M->rows = rows;
    M->cols = cols;
    M->capacity = capacity;
}

void get_dims(Matrix *M) {
    printf("rows=%d, cols=%d\n", M->rows, M->cols);
}

float get_element(Matrix *M, int row, int col) {
    if (row < 0 || row >= M->rows || col < 0 || col >= M->cols) {
        printf("Error: index out of range\n");
        return 0.0f;
    }

    return M->data[row * M->cols + col];
}
void set_element(Matrix *M, int row, int col, float value) {
    if (row < 0 || row >= M->rows || col < 0 || col >= M->cols) {
        printf("Error: index out of range\n");
        return;
    }

    M->data[row * M->cols + col] = value;
    return;
}

void print_matrix(Matrix *M) {
    for (int i = 0; i < M->rows; i++) {
        for (int j = 0; j < M->cols; j++) {
            printf("%.2f ", get_element(M, i, j));
        }
        printf("\n");
    }
}

void add_row(Matrix *M) {
    M->rows++;
}
void add_col(Matrix *M) {
    M->cols++;
}

Vector matvec_multiply(Matrix *A, Vector *B) {
    (void)A;
    (void)B;
    Vector result = {0};
    return result;
}

Matrix matrix_multiply(Matrix *A, Matrix *B) {
    Matrix result = {0};

    if (A == NULL || B == NULL) {
        printf("Error: null matrix passed\n");
        return result;
    }

    if (A->cols != B->rows) {
        printf("Error: Matrices are incompatible for multiplication!\n");
        return result;
    }

    init_matrix(&result, A->rows, B->cols);

    for (int i = 0; i < A->rows; i++) {
        for (int j = 0; j < B->cols; j++) {
            float _sum = 0.0f;

            for (int k = 0; k < A->cols; k++) {
                _sum += get_element(A, i, k) * get_element(B, k, j);
            }

            set_element(&result, i, j, _sum);
        }
    }

    return result;
}

int main(void) {
    Matrix A, B;
    init_matrix(&A, 3, 3);
    init_matrix(&B, 3, 3);

    for (int i = 0; i < A.rows; i++) {
        for (int j = 0; j < A.cols; j++) {
            set_element(&A, i, j, (float)(i + j + 1));
            set_element(&B, i, j, (float)(i + j + 1));
        }
    }

    Matrix Result = matrix_multiply(&A, &B);
    print_matrix(&Result);
    return 0;
}

// set_element(&result, i, j, 0);

/*
def __matmul__(self, other) -> Matrix | SquareMatrix:
    for i in range(self._rows):
        for j in range(other._cols):
            for k in range(self._cols):
                result[i][j] += (self[i][k] * other[k][j])

    return SquareMatrix(array=result)
*/
