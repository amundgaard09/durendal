
#include <vector>
#include "mathtools.hpp"

bool iswithinrange(int lower, int upper, int value) {
    return (lower <= value && value <= upper);
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

