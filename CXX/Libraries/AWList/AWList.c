/* DOUBLY LINKED LIST LIBRARY - AMUNDWORKS - V.1 */

#include <stdio.h>
#include <stdlib.h>
#include "AWList.h"

void InitList(DLList *l) {
    l->head = NULL;
    l->tail = NULL;
    l->size = 0;
}

int IsEmpty(DLList *l) {
    return (l->head == NULL);
}

int GetIndex(DLList *l, int value) {
    Node* CurrentNode = l->head;
    int index = 0;

    while (CurrentNode != NULL) {
        if (CurrentNode->data == value) {
            return index;
        }

        CurrentNode = CurrentNode->next;
        index++;
    }

    return -1;
}

int ListSize(DLList *l) {
    return l->size;
} 

void InsertAtFront(DLList *l, int value) {
    Node* newNode = (Node*)malloc(sizeof(Node));
    if (newNode == NULL) {
        printf("Error: malloc failed\n");
        return;
    }

    newNode->data = value;
    newNode->prev = NULL;
    newNode->next = l->head;

    if (l->head != NULL) {
        l->head->prev = newNode;

    } else {
        l->tail = newNode;
    }

    l->head = newNode;
    l->size++;
}
void InsertAtBack(DLList *l, int value) {
    Node* newNode = (Node*)malloc(sizeof(Node));
    if (newNode == NULL) {
        printf("Error: malloc failed\n");
        return;
    }

    newNode->data = value;
    newNode->prev = l->tail;
    newNode->next = NULL;

    if (l->tail != NULL) {
        l->tail->next = newNode;
    } else {
        l->head = newNode; 
    }

    l->tail = newNode;
    l->size++;

}
void PrintList(DLList *l) {
    printf("[");
    Node* CurrentNode = l->head;
    while (CurrentNode != NULL) {
        printf("%d", CurrentNode->data);
        if (CurrentNode->next != NULL) {
            printf(", "); 
        }
        CurrentNode = CurrentNode->next;
    }

    printf("]\n");
}
void Insert(DLList *l, int value, int Idx) {
    if ((Idx + 1) > ListSize(l)) {
        printf("List Index out of range!");
        return;
    }

    Node* CurrentNode = l->head;
    Node* newNode = (Node*)malloc(sizeof(Node));

    if (newNode == NULL) { printf("Error: malloc failed\n"); return; }

    newNode->data = value;

    int CurrentIdx = 0;

    if (Idx == 0) {
        InsertAtFront(l, value);
        return;
    } else if (Idx == ListSize(l) - 1) {
        InsertAtBack(l, value);
        return;
    }

    while (CurrentNode->next != NULL) {
        if (CurrentIdx == Idx) {
            newNode->prev = CurrentNode->prev;
            newNode->next = CurrentNode;
            CurrentNode->prev->next = newNode;
            CurrentNode->prev = newNode;
            l->size++;
            return;
        }

        CurrentNode = CurrentNode->next;
        CurrentIdx++;   
    }
}
void Remove(DLList *l, int Idx) {
    if ((Idx + 1) > ListSize(l)) {
        printf("List Index out of range!");
        return;
    }

    Node* CurrentNode = l->head;
    int CurrentIdx = 0;

    if (Idx == 0) {
        Node* temp = l->head;
        l->head = l->head->next;
        if (l->head != NULL) {l->head->prev = NULL;} else {l->tail = NULL;}
        free(temp);
        l->size--;
        return;

    } else if (Idx == ListSize(l) - 1) {
        Node* temp = l->tail;
        l->tail = l->tail->prev;
        if (l->tail != NULL) {l->tail->next = NULL;} else {l->head = NULL;}
        free(temp);
        l->size--;
        return;
    }

    while (CurrentNode != NULL) {
        if (CurrentIdx == Idx) {
            CurrentNode->next->prev = CurrentNode->prev;
            CurrentNode->prev->next = CurrentNode->next;
            free(CurrentNode);
            l->size--;
            return;
        }

        CurrentNode = CurrentNode->next;
        CurrentIdx++;   
    }
}
void FreeList(DLList *l) {
    Node* CurrentNode = l->head;

    while (CurrentNode != NULL) {
        Node* NextToRemove = CurrentNode->next;
        free(CurrentNode);
        CurrentNode = NextToRemove;
    }

    l->head = NULL;
    l->tail = NULL;
    l->size = 0;
}

int main(void) {
    DLList l;

    InitList(&l);

    InsertAtBack(&l, 10);
    InsertAtBack(&l, 25);
    InsertAtBack(&l, 30);
    InsertAtFront(&l, 99);

    PrintList(&l);

    Insert(&l, 20, 2);

    PrintList(&l);
}