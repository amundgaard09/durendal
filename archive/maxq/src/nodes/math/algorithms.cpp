
#include "algorithms.hpp"
#include "../../core/node/node.hpp"
#include "../../commons/utilities/toolchain.hpp"
#include "../../../../awcpplib/libs/math/algorithms/primality.hpp"

std::vector<float> lovelace(float a, float b, float c, float d, float e, float f) {
    std::vector<float> vec;
    if (a*e == b*d) {;
        return vec;
    }
    
    float Dx = c*e - b*f;
    float Dy = a*f - c*d;
    vec.push_back(Dx / (a*e - b*d));
    vec.push_back(Dy / (a*e - b*d));
    return vec;
}

class PrimeFactorizeNode : public ComputeNode {
    public:
        virtual void execute() override {
            if (Inputs.size() == 1) {
                float* ptr = Inputs.at(0);
                float toFactorize = *ptr;
                int toFactorizeInt = static_cast<int>(toFactorize);
                std::vector<int> Factors = primefactorize(toFactorizeInt);

            } else {
                Outputs.push_back(NULL);
            }
        }
};

class LovelaceNode : public ComputeNode {
    public:
        virtual void execute() override {
            if (Inputs.size() == 6) {
                std::vector<float> coeffs = lovelace(*Inputs.at(0), *Inputs.at(1), *Inputs.at(2), *Inputs.at(3), *Inputs.at(4), *Inputs.at(5));
                Outputs = get_indvdl_ptrs(coeffs);
            } else {
                Outputs.push_back(NULL);
            }
        }

};
