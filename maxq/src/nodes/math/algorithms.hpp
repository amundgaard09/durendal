

#include "../../core/node/node.hpp"

#ifndef ALGORITHMS.HPP
#define ALGORITHMS.HPP

std::vector<float> lovelace(float a, float b, float c, float d, float e, float f);

class PrimeFactorizeNode : public AlgoNode {
    public:
        virtual void compute() override {};
};

#endif