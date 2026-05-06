
#ifndef NODE_HPP
#define NODE_HPP

#include <iostream>
#include <string>
#include <vector>
#include <stdbool.h>

class BaseNode {
    public:
        std::vector<float*> Inputs;         // Vector of float pointers to inputs
        std::vector<float*> OptOutputs;     // A optional vector output for multi-output nodes
        float* Output;                      // A pointer to the output from this node
        int ID;                             // This nodes ID
        
        virtual void compute() {};         // Base compute() function - is to be overridden by type-given node class (Constant, Compute, etc.) 
        virtual ~BaseNode() = default;
};

class ConstantNode : public BaseNode {
    public:
        float Value;
        virtual void compute(void) override {};
};

class ComputeNode : public BaseNode {
    public:
        int NVInMin;        // Minimum number of valid inputs 
        int NVInMax;        // Maximum number of valid inputs
        bool val_args(int argsGiven) {};   // Validate given args to ComputeNode function. Returns true if valid - False otherwise.
};

class AlgoNode : public ComputeNode {
    public:
};



#endif