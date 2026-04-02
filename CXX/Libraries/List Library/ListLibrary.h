/*List Library prototype file - AMUNDWORKS DLLIST LIBRARY - V.1*/

#ifndef LISTLIBRARY_H
#define LISTLIBRARY_H

typedef struct Node {
    int data;
    struct Node* next;
    struct Node* prev;
} Node;

typedef struct DLList {
    int size;
    Node* head;
    Node* tail;
} DLList;

void InitList(DLList *l);
int IsEmpty(DLList *l);
int GetIndex(DLList *l, int value);
int ListSize(DLList *l);
void InsertAtFront(DLList *l, int value);
void InsertAtBack(DLList *l, int value);
void PrintList(DLList *l);
void Insert(DLList *l, int value, int Idx);
void Remove(DLList *l, int Idx);
void FreeList(DLList *l);

#endif