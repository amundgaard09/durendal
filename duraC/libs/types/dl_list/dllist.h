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

void init_list(DLList *l);
int is_empty(DLList *l);
int get_idx(DLList *l, int value);
int list_size(DLList *l);
void list_remove(DLList *l, int Idx);
void insert(DLList *l, int value, int Idx);
void insert_at_front(DLList *l, int value);
void insert_at_back(DLList *l, int value);
void print_list(DLList *l);
void free_list(DLList *l);

#endif