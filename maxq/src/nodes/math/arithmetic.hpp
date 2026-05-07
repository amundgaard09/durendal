
#include "../../core/node/node.hpp"

#ifndef ARITHMETIC.HPP
#define ARTIHMETIC.HPP

class AddNode : public ComputeNode {
    public:
        virtual void execute() override {};
};

class SubtractNode : public ComputeNode {
    public:
        virtual void execute() override {};

};

class DivideNode : public ComputeNode {
    public:
        virtual void execute() override {};

};

class MultiplyNode : public ComputeNode {
    public:
        virtual void execute() override {};

};

class SumNode : public ComputeNode {
    public:
        virtual void execute() override {};
};

#endif