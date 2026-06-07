
#include "graphengine.hpp"
#include "../node/node.hpp"
#include <memory>
#include <vector>

class GraphEngine {
    std::vector<std::unique_ptr<IONode>> nodes;
        public:
            void addNode(std::unique_ptr<IONode> node) {
                nodes.push_back(std::move(node));
            }

            void run(std::vector<float*> _Input) {
                for (auto& node : nodes) {
                    node->Inputs = _Input;
                    node->execute();
                    float* nextInput = node->Output; 
                }
            }
};