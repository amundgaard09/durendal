/* VECTOR LIBRARY - DURENDAL ENGINEERING - V.1 */

/* 
NOTE - This is not much more than a simple wrapper around the duraC::Array struct. 
The vector class' only difference is compatability with the duraC::Matrix struct.
*/

#include <stdint.h>
#include "../array/array.h"
#include "vector.h"

void init_vector(Vector *a) {
    init_array(&a->elements);
}