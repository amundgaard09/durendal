
#include "../../core/node/node.hpp"

#ifndef ARITHMETIC.HPP
#define ARTIHMETIC.HPP

class AddNode : public ComputeNode {
    public:
        virtual void compute() override {};
};

class SumNode : public ComputeNode {
    public:
        virtual void compute() override {};
};

class SubtractNode : public ComputeNode {

};

class DivideNode : public ComputeNode {

};

class MultiplyNode : public ComputeNode {

};

#endif