
#include <vector>
#include "toolchain.hpp"

// Replace the values in a vector with the values' pointers.
std::vector<float*> get_indvdl_ptrs(const std::vector<float> valvec) {
    std::vector<float*> ptrvec;
    for (float val : valvec) { if (val) { ptrvec.push_back(&val); } }

    return ptrvec;
}

float ptrvecsum(const std::vector<float*>& vec) {
    float total = 0.0f;
    
    for (float* ptr : vec) { if (ptr) { total += *ptr; } }
    return total;
}

float vecsum(const std::vector<float>& vec) {
    float total = 0.0f;
    
    for (float ptr : vec) { if (ptr) { total += ptr; } }
    return total;
}

bool iswithinrange(int lower, int upper, int value) { return (lower <= value && value <= upper); }

