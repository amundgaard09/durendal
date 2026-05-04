
#include <iostream>
#include <string>
#include <vector>
#include <stdbool.h>
#include "node.hpp"

// The level 0 node - All nodes are derived from here
class BaseNode {
    public:
        std::vector<float*> Inputs;         // Vector of float pointers to inputs
        float* Output;                      // A pointer to the output from this node
        int ID;                             // This nodes ID
        
        virtual void compute() {            // Base compute() function - is to be overridden by type-given node class (Constant, Compute, etc.)
            std::cout << "Placeholder for Node functionality" << std::endl;
        } 
        virtual ~BaseNode() {}
};

// Level 1
class ConstantNode : public BaseNode {
    public:
        float Value;                            // The value of this constant
        virtual void compute(void) override {   // The compute() function overridden as a setter method
            Output = &Value;
        }
};

// Level 1
class ComputeNode : public BaseNode {
    public:
        int NWInMin, NWInMax;            // Minimum and maximum number of valid inputs ()
        bool val_args(int argsGiven) {   // UNUSED - Validate given args to ComputeNode function. Returns true if valid - False otherwise.
            return (NWInMin <= argsGiven && argsGiven <= NWInMax);
        }
};



