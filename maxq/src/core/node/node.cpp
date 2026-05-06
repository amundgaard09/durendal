
/*
 *
 * MAX-Q Composable Systems Engine - Version 0.0.0.1
 *
 * This file contains the base node classes (Levels 0, 1 and 2) which all nodes inherit from.
 *
 */

#include <iostream>
#include <string>
#include <vector>
#include <stdbool.h>
#include "node.hpp"

// The level 0 node - All nodes are derived from here
class BaseNode {
    public:
        std::vector<float*> Inputs;
        std::vector<float*> OptOutputs;
        float* Output;
        int ID;
        
        virtual void compute() {            // Base compute() function - is to be overridden by type-given node class (Constant, Compute, etc.)
            std::cout << "Placeholder for Node functionality" << std::endl;
        } 
        virtual ~BaseNode() {}
};

// Level 1
class ConstantNode : public BaseNode {
    public:
        float Value;
        virtual void compute(void) override {
            Output = &Value;

        }
};

// Level 1
class ComputeNode : public BaseNode {
    public:
        int NVInMin, NVInMax;            // Minimum and maximum number of valid inputs ()
        bool val_args(int argsGiven) {   // UNUSED - Validate given args to ComputeNode function. Returns true if valid - False otherwise.
            return (NVInMin <= argsGiven && argsGiven <= NVInMax);
        }
};

// Level 2 - Base of all algorithm nodes
class AlgoNode : public ComputeNode {
    public:
};

