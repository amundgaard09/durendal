/*Doubly Linked List prototype file - DURENDAL ENGINEERING DLLIST LIBRARY - V.1*/

#ifndef DLLIST_H
#define DLLIST_H

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
void Remove(DLList *l, int Idx);
void Insert(DLList *l, int value, int Idx);
void InsertAtFront(DLList *l, int value);
void InsertAtBack(DLList *l, int value);
void PrintList(DLList *l);
void FreeList(DLList *l);

#endif