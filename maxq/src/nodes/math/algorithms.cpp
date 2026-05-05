
#include "algorithms.hpp"
#include "../../core/node/node.hpp"
#include "../../../../awcpplib/Math/Algorithms/primality.hpp"

class PrimeFactorizeNode : public ComputeNode {
    public:
        virtual void compute() override {
            if (Inputs.size() == 1) {
                float* ptr = Inputs.at(0);
                float toFactorize = *ptr;
                int toFactorizeInt = static_cast<int>(toFactorize);
                std::vector<int> Factors = primefactorize(toFactorizeInt);

            } else {
                Output = NULL;
            }
        }
};

