
#include "arithmetic.hpp"
#include "../../commons/utils/mathtools.hpp"
#include "../../core/node/node.hpp"

// Level 2 - Takes two floats and returns a pointer to the sum.
class AddNode : public ComputeNode {
    public:
        virtual void compute() override {
            float temp;
            
            if (Inputs.size() == 2) {
                float* a = Inputs.at(0);
                float* b = Inputs.at(1);
                temp = *a * *b;
            } else {
                Output = NULL;
            }

            Output = &temp;
        }
};

// Level 2 - Takes a `float` pointer vector and returns the sum of the values.
class SumNode : public ComputeNode {
    public:
        virtual void compute() override {
            float temp = ptrvecsum(Inputs);
            Output = &temp;
        }
};

class SubtractNode : public ComputeNode {
    public:

};

class DivideNode : public ComputeNode {
    public:

};

class MultiplyNode : public ComputeNode {
    public:

};

