
#ifndef NODE_HPP
#define NODE_HPP

#include <iostream>
#include <string>
#include <vector>
#include <stdbool.h>

class BaseNode {
    public:
        std::vector<float*> Inputs;         // Vector of float pointers to inputs
        float Output;                       // The output from this node
        int ID;                             // This nodes ID
        
        virtual void compute();         // Base compute() function - is to be overridden by type-given node class (Constant, Compute, etc.) 
        virtual ~BaseNode() = default;
};

class ConstantNode : public BaseNode {
    public:
        float Value;                            // The value of this constant
        virtual void compute(void) override;    // The compute() function overridden as a setter method

};

class ComputeNode : public BaseNode {
    public:
        int NWInMin, NWInMax;            // Minimum and maximum number of valid inputs ()
        bool val_args(int argsGiven);   // Validate given args to ComputeNode function. Returns true if valid - False otherwise.
};

#endif