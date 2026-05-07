
#ifndef NODE_HPP
#define NODE_HPP

#include <iostream>
#include <string>
#include <vector>
#include <stdbool.h>

class Node {
    public:
        int ID;
};

class IONode : public Node {
    public:
        std::vector<float*> Inputs;
        std::vector<float*> Outputs;
        
        virtual void execute() {};         // Base compute() function - is to be overridden by type-given node class (Constant, Compute, etc.) 
        virtual ~IONode() = default;
};

class ConstantNode : public IONode {
    public:
        float Value;
        virtual void execute(void) override {};
};

class ComputeNode : public IONode {
    public:
        int NVInMin;        // Minimum number of valid inputs 
        int NVInMax;        // Maximum number of valid inputs
        bool val_args(int argsGiven) {};   // Validate given args to ComputeNode function. Returns true if valid - False otherwise.
};

class AlgoNode : public ComputeNode {
    public:
};



#endif