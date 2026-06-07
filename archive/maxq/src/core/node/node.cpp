
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
class Node {
    public:
        int ID;
};

// A node with inputs and outputs
class IONode : public Node {
    public:
        std::vector<float*> Inputs;
        std::vector<float*> Outputs;
        
        virtual void execute() {            // Base compute() function - is to be overridden by type-given node class (Constant, Compute, etc.)
            std::cout << "Placeholder for Node functionality" << std::endl;
        } 
        virtual ~IONode() {}
};

// Level 2
class ConstantNode : public IONode {
    public:
        float Value;
        virtual void execute() override {
            Outputs.push_back(&Value);

        }
};

// Level 2
class ComputeNode : public IONode {
    public:
        int NVInMin, NVInMax;            // Minimum and maximum number of valid inputs ()
        bool val_args(int argsGiven) {   // UNUSED - Validate given args to ComputeNode function. Returns true if valid - False otherwise.
            return (NVInMin <= argsGiven && argsGiven <= NVInMax);
        }
};

// Level 3 - Base of all algorithm nodes
class AlgoNode : public ComputeNode {
    public:
};