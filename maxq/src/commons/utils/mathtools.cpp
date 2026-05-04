
#include <vector>
#include "mathtools.hpp"

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

