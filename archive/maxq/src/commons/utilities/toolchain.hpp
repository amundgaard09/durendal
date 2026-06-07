
#include <vector>

#ifndef TOOLCHAIN.HPP
#define TOOLCHAIN.HPP

std::vector<float*> get_indvdl_ptrs(const std::vector<float> valuevector);
float ptrvecsum(const std::vector<float*>& vec);
float vecsum(const std::vector<float>& vec);

bool iswithinrange(int lower, int upper, int value);

#endif