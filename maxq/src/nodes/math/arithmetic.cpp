
#include "arithmetic.hpp"
#include "../../commons/utilities/toolchain.hpp"
#include "../../core/node/node.hpp"

// Level 2 - Takes two floats and returns a pointer to the sum.
class AddNode : public ComputeNode {
    public:
        virtual void execute() override {
            float temp;
            
            if (Inputs.size() == 2) {
                float* a = Inputs.at(0);
                float* b = Inputs.at(1);
                temp = *a + *b;
            } else {
                Outputs.push_back(NULL);
            }

            Outputs.push_back(&temp);
        }
};

class SubtractNode : public ComputeNode {
    public:
        virtual void execute() override {
            float temp;
            
            if (Inputs.size() == 2) {
                float* a = Inputs.at(0);
                float* b = Inputs.at(1);
                temp = *a - *b;
            } else {
                Outputs.push_back(NULL);
            }

            Outputs.push_back(&temp);
        }
};

class DivideNode : public ComputeNode {
    public:
        virtual void execute() override {
            float temp;
            
            if (Inputs.size() == 2) {
                float* a = Inputs.at(0);
                float* b = Inputs.at(1);
                temp = *a / *b;
            } else {
                Outputs.push_back(NULL);
            }

            Outputs.push_back(&temp);
        }
};

class MultiplyNode : public ComputeNode {
    public:
        virtual void execute() override {
            float temp;
            
            if (Inputs.size() == 2) {
                float* a = Inputs.at(0);
                float* b = Inputs.at(1);
                temp = *a * *b;
            } else {
                Outputs.push_back(NULL);
            }

            Outputs.push_back(&temp);
        }
};

class SumNode : public ComputeNode {
    public:
        virtual void execute() override {
            if (Inputs.size() > 1) {
                float temp = ptrvecsum(Inputs);
                Outputs.push_back(&temp);
            } else {
                Outputs.push_back(NULL);
            }
        }
};

