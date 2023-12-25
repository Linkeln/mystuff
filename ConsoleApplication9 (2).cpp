#include <iostream>
#include <fstream>
#include <vector>
#include <sstream>
#include <unordered_set>
#include <unordered_map>
#include <queue>
#include <tuple>

class Node {
public:
    std::string name;
    std::string color;
};

class Edge {
public:
    Node* startNode;
    Node* endNode;
    std::string color;
};
class BinaryTreeNode {
public:
    std::string name;
    std::string color;
    BinaryTreeNode* left;
    BinaryTreeNode* right;

    BinaryTreeNode(const std::string& nodeName, const std::string& nodeColor)
        : name(nodeName), color(nodeColor), left(nullptr), right(nullptr) {}
};
class Graph {
public:
    std::string name;
    std::vector<Node> nodes;
    std::vector<Edge> edges;
    std::vector<std::vector<int>> incidentMatrix;
};
class BinaryTree {
public:
    BinaryTreeNode* root;

    BinaryTree() : root(nullptr) {}

    void printBinaryTree() const {
        if (root) {
            std::cout << "Binary Tree Structure:\n";
            printBinaryTree(root, 0);
        }
        else {
            std::cerr << "Binary Tree is empty.\n";
        }
        std::cout << "------------------------\n";
    }

private:
    void printBinaryTree(BinaryTreeNode* node, int level) const {
        if (node) {
            printBinaryTree(node->right, level + 1);
            for (int i = 0; i < level; ++i) {
                std::cout << "   ";
            }
            std::cout << node->name << " (" << node->color << ")\n";
            printBinaryTree(node->left, level + 1);
        }
    }
};

class GraphEditor {
public:
    std::vector<Graph> graphs;
    size_t activeGraphIndex;  // Добавляем переменную для отслеживания активного графа
    BinaryTree binaryTree;

    GraphEditor() : activeGraphIndex(0) {}

    void createGraph() {
        Graph graph;
        std::cout << "Enter the name for the graph: ";
        std::cin >> graph.name;
        graphs.push_back(graph);
    }
    void printColoredEdgeName(const Edge& edge) const {
        std::cout << "\033[38;2;" << getColorRGB(edge.color) << "m" << edge.startNode->name << "->" << edge.endNode->name << "\033[0m";
    }
    bool isEulerian(const Graph& graph) const {
        for (const auto& node : graph.nodes) {
            int degree = 0;
            for (const auto& edge : graph.edges) {
                if (edge.startNode->name == node.name || edge.endNode->name == node.name) {
                    degree++;
                }
            }
            if (degree % 2 != 0) {
                return false; // Найдена вершина с нечетной степенью
            }
        }
        return true; // Все вершины имеют четную степень
    }
    void printGraphInfo(const Graph& graph) const {
        if (!graphs.empty() && activeGraphIndex < graphs.size()) {
            const Graph& graph = graphs[activeGraphIndex];
            std::cout << "Graph Name: " << graph.name << std::endl;
            std::cout << "Number of Nodes: " << graph.nodes.size() << std::endl;
            std::cout << "Number of Edges: " << graph.edges.size() << std::endl;

            // Output information for each node
            std::cout << "Nodes:\n";
            for (const auto& node : graph.nodes) {
                std::cout << "  Name: ";
                std::cout << "\033[38;2;" << getColorRGB(node.color) << "m" << node.name << "\033[0m"; // Set color for text
                std::cout << ", Color: " << node.color << std::endl;
            }

            // Output information for each edge
            std::cout << "Edges:\n";
            for (const auto& edge : graph.edges) {
                std::cout << "  Start Node: ";
                printColoredEdgeName(edge);
                std::cout << ", Color: " << edge.color << std::endl;
            }
            // Check if the graph is Eulerian
            std::cout << "Graph Eulerian: " << (isEulerian(graph) ? "Yes" : "No") << std::endl;

            std::cout << "------------------------" << std::endl;
        }
        else {
            std::cerr << "No graphs available to print information." << std::endl;
        }
    }

    std::string getColorRGB(const std::string& color) const {
        if (color == "Red") {
            return "255;0;0";
        }
        else if (color == "Green") {
            return "0;255;0";
        }
        else if (color == "Blue") {
            return "0;0;255";
        }
        else {
            // Default to white color
            return "255;255;255";
        }
    }

    void addNode(Graph& graph) {
        Node node;
        std::cout << "Enter the name for the node: ";
        std::cin >> node.name;
        graph.nodes.push_back(node);

        // Update incident matrix
        graph.incidentMatrix.push_back(std::vector<int>(graph.edges.size(), 0));

        for (auto& row : graph.incidentMatrix) {
            row.push_back(0);
        }
    }

    void addNodeToActiveGraph() {
        if (!graphs.empty()) {
            addNode(graphs[activeGraphIndex]);
        }
        else {
            std::cerr << "No graphs available to add nodes." << std::endl;
        }
    }

    void removeNodeFromActiveGraph() {
        if (!graphs.empty()) {
            std::cout << "Enter the name of the node to remove: ";
            std::string nodeNameToRemove;
            std::cin >> nodeNameToRemove;
            removeNode(graphs[activeGraphIndex], nodeNameToRemove);
        }
        else {
            std::cerr << "No graphs available to remove nodes." << std::endl;
        }
    }

    void setActiveGraph() {
        if (graphs.empty()) {
            std::cerr << "No graphs available to set as active." << std::endl;
            return;
        }

        std::cout << "Available graphs:" << std::endl;
        for (size_t i = 0; i < graphs.size(); ++i) {
            std::cout << i << ". " << graphs[i].name << std::endl;
        }

        std::cout << "Enter the index of the graph to set as active: ";
        int selectedGraphIndex;
        std::cin >> selectedGraphIndex;

        if (selectedGraphIndex >= 0 && selectedGraphIndex < static_cast<int>(graphs.size())) {
            activeGraphIndex = static_cast<size_t>(selectedGraphIndex);
            std::cout << "Active graph set to: " << graphs[activeGraphIndex].name << std::endl;
        }
        else {
            std::cerr << "Invalid graph index. Setting active graph to the first graph." << std::endl;
            activeGraphIndex = 0;
        }
    }

    void removeNode(Graph& graph, const std::string& nodeName) {
        auto it = std::remove_if(graph.nodes.begin(), graph.nodes.end(),
            [nodeName](const Node& node) { return node.name == nodeName; });

        graph.nodes.erase(it, graph.nodes.end());

        // Remove edges connected to the deleted node
        graph.edges.erase(std::remove_if(graph.edges.begin(), graph.edges.end(),
            [nodeName](const Edge& edge) {
                return edge.startNode->name == nodeName || edge.endNode->name == nodeName;
            }),
            graph.edges.end());

        // Update incident matrix
        for (auto& row : graph.incidentMatrix) {
            row.pop_back();
        }
    }

    void renameNode(Graph& graph, const std::string& oldName, const std::string& newName) {
        for (auto& node : graph.nodes) {
            if (node.name == oldName) {
                node.name = newName;
                break;
            }
        }
    }

    void addEdge(Graph& graph, const std::string& startNodeName, const std::string& endNodeName) {
        // Find pointers to start and end nodes
        Node* startNode = nullptr;
        Node* endNode = nullptr;

        for (auto& node : graph.nodes) {
            if (node.name == startNodeName) {
                startNode = &node;
            }
            if (node.name == endNodeName) {
                endNode = &node;
            }
        }

        if (!startNode) {
            std::cerr << "Error: Node '" << startNodeName << "' not found.\n";
            return;
        }

        if (!endNode) {
            std::cerr << "Error: Node '" << endNodeName << "' not found.\n";
            return;
        }

        Edge edge;
        edge.startNode = startNode;
        edge.endNode = endNode;

        graph.edges.push_back(edge);

        // Update incident matrix
        size_t startNodeIndex = 0;
        size_t endNodeIndex = 0;

        for (size_t i = 0; i < graph.nodes.size(); ++i) {
            if (graph.nodes[i].name == startNodeName) {
                startNodeIndex = i;
                graph.incidentMatrix[i].push_back(1);
            }
            else if (graph.nodes[i].name == endNodeName) {
                endNodeIndex = i;
                graph.incidentMatrix[i].push_back(-1);
            }
            else {
                graph.incidentMatrix[i].push_back(0);
            }
        }

        // Check if indices are valid
        if (startNodeIndex >= graph.incidentMatrix.size() || endNodeIndex >= graph.incidentMatrix.size()) {
            std::cerr << "Error: Invalid indices while updating incident matrix.\n";
            return;
        }

        // Resize other rows if needed
        for (size_t i = 0; i < graph.incidentMatrix.size(); ++i) {
            if (i != startNodeIndex && i != endNodeIndex) {
                if (startNodeIndex >= graph.incidentMatrix[i].size() || endNodeIndex >= graph.incidentMatrix[i].size()) {
                    std::cerr << "Error: Invalid indices while updating incident matrix.\n";
                    return;
                }

                graph.incidentMatrix[i].push_back(0);
            }
        }
    }



    void removeEdge(Graph& graph, const std::string& startNodeName, const std::string& endNodeName) {
        graph.edges.erase(std::remove_if(graph.edges.begin(), graph.edges.end(),
            [startNodeName, endNodeName](const Edge& edge) {
                return edge.startNode->name == startNodeName && edge.endNode->name == endNodeName;
            }),
            graph.edges.end());

        // Update incident matrix
        for (size_t i = 0; i < graph.nodes.size(); ++i) {
            if (graph.nodes[i].name == startNodeName || graph.nodes[i].name == endNodeName) {
                graph.incidentMatrix[i].pop_back();
            }
        }
    }

    void printNodeDegrees() const {
        if (!graphs.empty()) {
            printNodeDegrees(graphs[activeGraphIndex]);
        }
        else {
            std::cerr << "No graphs available to print node degrees." << std::endl;
        }
    }

    void printNodeDegrees(const Graph& graph) const {
        for (const auto& node : graph.nodes) {
            int inDegree = 0, outDegree = 0;
            for (const auto& edge : graph.edges) {
                if (edge.startNode->name == node.name) {
                    outDegree++;
                }
                if (edge.endNode->name == node.name) {
                    inDegree++;
                }
            }
            std::cout << "Node " << node.name << ": In-Degree = " << inDegree << ", Out-Degree = " << outDegree;
            std::cout << ", Color: \033[38;2;" << getColorRGB(node.color) << "m" << node.color << "\033[0m" << std::endl;
        }
    }

    void setColor(Graph& graph, const std::string& nodeName, const std::string& color) {
        for (auto& node : graph.nodes) {
            if (node.name == nodeName) {
                node.color = color;
                break;
            }
        }
    }

    void setColor(Graph& graph, const std::string& startNodeName, const std::string& endNodeName, const std::string& color) {
        for (auto& edge : graph.edges) {
            if (edge.startNode->name == startNodeName && edge.endNode->name == endNodeName) {
                edge.color = color;
                break;
            }
        }
    }

    void saveGraph(const Graph& graph) {
        std::string filePath = graph.name + "_graph.txt";
        std::ofstream file(filePath);

        if (file.is_open()) {
            // Save nodes
            file << "Nodes:\n";
            for (const auto& node : graph.nodes) {
                file << node.name << " " << node.color << "\n";
            }

            // Save edges
            file << "\nEdges:\n";
            for (const auto& edge : graph.edges) {
                file << edge.startNode->name << " " << edge.endNode->name << " " << edge.color << "\n";
            }

            file.close();
            std::cout << "Graph saved successfully.\n";
        }
        else {
            std::cerr << "Unable to open the file.\n";
        }
    }

    void loadGraph(Graph& graph) {
        std::string filePath = graph.name + "_graph.txt";
        std::ifstream file(filePath);

        if (file.is_open()) {
            // Clear existing data
            graph.nodes.clear();
            graph.edges.clear();
            graph.incidentMatrix.clear();

            std::string line;
            while (std::getline(file, line)) {
                std::istringstream iss(line);
                std::string type;
                iss >> type;

                if (type == "Nodes:") {
                    while (std::getline(file, line) && !line.empty()) {
                        Node node;
                        std::istringstream issNode(line);
                        issNode >> node.name >> node.color;
                        graph.nodes.push_back(node);

                        // Update incident matrix
                        graph.incidentMatrix.emplace_back(graph.edges.size(), 0);
                    }
                }
                else if (type == "Edges:") {
                    while (std::getline(file, line)) {
                        Edge edge;

                        // Find pointers to start and end nodes
                        std::string startNodeName, endNodeName;
                        iss >> startNodeName >> endNodeName;

                        for (auto& node : graph.nodes) {
                            if (node.name == startNodeName) {
                                edge.startNode = &node;
                            }
                            if (node.name == endNodeName) {
                                edge.endNode = &node;
                            }
                        }

                        // Update incident matrix
                        for (size_t i = 0; i < graph.nodes.size(); ++i) {
                            if (graph.nodes[i].name == edge.startNode->name) {
                                graph.incidentMatrix[i].push_back(1);
                            }
                            else if (graph.nodes[i].name == edge.endNode->name) {
                                graph.incidentMatrix[i].push_back(-1);
                            }
                            else {
                                graph.incidentMatrix[i].push_back(0);
                            }
                        }

                        graph.edges.push_back(edge);
                    }
                }
            }

            file.close();
            std::cout << "Graph loaded successfully.\n";
        }
        else {
            std::cerr << "Unable to open the file.\n";
        }
    }

    void findHamiltonianCycles(Graph& graph) {
        std::vector<int> path;
        path.reserve(graph.nodes.size());

        // Инициализация массива посещенных вершин
        std::vector<bool> visited(graph.nodes.size(), false);

        // Начать с любой вершины (в данном примере, начнем с первой вершины)
        path.push_back(0);
        visited[0] = true;

        std::cout << "Hamiltonian Cycles:\n";
        hamiltonianCyclesUtil(graph, path, visited, 1);

        std::cout << "------------------------\n";
    }

    void hamiltonianCyclesUtil(Graph& graph, std::vector<int>& path, std::vector<bool>& visited, size_t pos) {
        if (pos == graph.nodes.size()) {
            // Проверяем, существует ли ребро из последней вершины в первую
            size_t lastNode = path.back();
            size_t firstNode = path.front();

            for (const auto& edge : graph.edges) {
                if ((edge.startNode->name == graph.nodes[lastNode].name && edge.endNode->name == graph.nodes[firstNode].name) ||
                    (edge.startNode->name == graph.nodes[firstNode].name && edge.endNode->name == graph.nodes[lastNode].name)) {
                    // Найден гамильтонов цикл
                    printHamiltonianCycle(path);
                    break;
                }
            }
            return;
        }

        for (size_t v = 0; v < graph.nodes.size(); ++v) {
            if (!visited[v] && isEdgeValidForHamiltonianCycle(graph, path.back(), v)) {
                path.push_back(v);
                visited[v] = true;

                hamiltonianCyclesUtil(graph, path, visited, pos + 1);

                path.pop_back();
                visited[v] = false;
            }
        }
    }

    bool isEdgeValidForHamiltonianCycle(const Graph& graph, size_t v1, size_t v2) const {
        // Проверяем, существует ли ребро между вершинами v1 и v2
        for (const auto& edge : graph.edges) {
            if ((edge.startNode->name == graph.nodes[v1].name && edge.endNode->name == graph.nodes[v2].name) ||
                (edge.startNode->name == graph.nodes[v2].name && edge.endNode->name == graph.nodes[v1].name)) {
                return true;
            }
        }
        return false;
    }

    void printHamiltonianCycle(const std::vector<int>& path) const {
        if (!graphs.empty() && activeGraphIndex < graphs.size()) {
            std::cout << "Cycle: ";
            for (size_t i = 0; i < path.size(); ++i) {
                std::cout << graphs[activeGraphIndex].nodes[path[i]].name;
                if (i < path.size() - 1) {
                    std::cout << " -> ";
                }
            }
            std::cout << std::endl;
        }
        else {
            std::cerr << "No graphs available or invalid active graph index." << std::endl;
        }
    }

    void convertToBinaryTree(const Graph& graph) {
        if (graph.nodes.empty() || graph.edges.empty()) {
            std::cerr << "Graph is empty. Cannot convert to binary tree.\n";
            return;
        }

        std::unordered_set<std::string> visitedNodes;
        BinaryTreeNode* rootNode = nullptr;

        // Создаем узлы для каждой вершины графа
        std::unordered_map<std::string, BinaryTreeNode*> nodeMap;
        for (const auto& node : graph.nodes) {
            nodeMap[node.name] = new BinaryTreeNode(node.name, node.color);
        }

        // Строим бинарное дерево по ребрам графа
        for (const auto& edge : graph.edges) {
            const std::string& startNodeName = edge.startNode->name;
            const std::string& endNodeName = edge.endNode->name;

            if (!rootNode) {
                rootNode = nodeMap[startNodeName];
            }

            BinaryTreeNode* parentNode = nodeMap[startNodeName];
            BinaryTreeNode* childNode = nodeMap[endNodeName];

            if (!parentNode->left) {
                parentNode->left = childNode;
            }
            else if (!parentNode->right) {
                parentNode->right = childNode;
            }

            visitedNodes.insert(startNodeName);
            visitedNodes.insert(endNodeName);
        }

        // Находим корень, если он не был найден по ребрам
        if (!rootNode && !visitedNodes.empty()) {
            const std::string& firstNodeName = *visitedNodes.begin();
            rootNode = nodeMap[firstNodeName];
        }

        binaryTree.root = rootNode;
    }
    std::pair<int, int> findNodeByNameInGraphs(const std::string& nodeName) const {
        for (size_t i = 0; i < graphs.size(); ++i) {
            for (size_t j = 0; j < graphs[i].nodes.size(); ++j) {
                if (graphs[i].nodes[j].name == nodeName) {
                    return std::make_pair(static_cast<int>(i), static_cast<int>(j));
                }
            }
        }
        return std::make_pair(-1, -1); // Узел не найден
    }


};

int main() {
    GraphEditor graphEditor;
    int choice;
    std::string startNode, endNode;

    do {
        std::cout << "1. Create Graph\n"
            << "2. Print Graph Information\n"
            << "3. Add Node\n"
            << "4. Remove Node\n"
            << "5. Rename Node\n"
            << "6. Add Edge\n"
            << "7. Remove Edge\n"
            << "8. Print Node Degrees\n"
            << "9. Set Node Color\n"
            << "10. Set Edge Color\n"
            << "11. Save Graph\n"
            << "12. Load Graph\n"
            << "13. Set Active Graph\n"
            << "14. Find Hamiltonian cycle\n"
            << "15. Convert Graph To Tree And Print\n"
            << "16. Find Node By Its Content\n"
            << "17. Exit\n"
            << "Enter your choice: ";
        std::cin >> choice;

        switch (choice) {
        case 1:
            graphEditor.createGraph();
            break;
        case 2:
            if (!graphEditor.graphs.empty()) {
                graphEditor.printGraphInfo(graphEditor.graphs[graphEditor.activeGraphIndex]);
            }
            else {
                std::cerr << "No graphs available to print information." << std::endl;
            }
            break;
        case 3:
            // Assume working with the first graph in the vector
            graphEditor.addNodeToActiveGraph();
            break;
        case 4: {
            graphEditor.removeNodeFromActiveGraph();
            break;
        }
        case 5: {
            std::cout << "Enter the name of the node to rename: ";
            std::string oldName, newName;
            std::cin >> oldName;
            std::cout << "Enter the new name for the node: ";
            std::cin >> newName;
            graphEditor.renameNode(graphEditor.graphs.front(), oldName, newName);
            break;
        }
        case 6: {
            std::cout << "Enter the names of the start and end nodes for the edge: ";
            std::cin >> startNode >> endNode;
            graphEditor.addEdge(graphEditor.graphs.front(), startNode, endNode);
            break;
        }
        case 7: {
            std::cout << "Enter the names of the start and end nodes for the edge to remove: ";
            std::cin >> startNode >> endNode;
            graphEditor.removeEdge(graphEditor.graphs.front(), startNode, endNode);
            break;
        }
        case 8:
            graphEditor.printNodeDegrees(graphEditor.graphs[graphEditor.activeGraphIndex]);
            break;
        case 9: {
            std::cout << "Enter the name of the node: ";
            std::string nodeName;
            std::cin >> nodeName;
            std::cout << "Enter the color for the node: ";
            std::string nodeColor;
            std::cin >> nodeColor;
            graphEditor.setColor(graphEditor.graphs.front(), nodeName, nodeColor);
            break;
        }
        case 10: {
            std::cout << "Enter the names of the start and end nodes for the edge: ";
            std::cin >> startNode >> endNode;
            std::cout << "Enter the color for the edge: ";
            std::string edgeColor;
            std::cin >> edgeColor;

            // Находим указатель на ребро
            Edge* selectedEdge = nullptr;
            for (auto& edge : graphEditor.graphs.front().edges) {
                if (edge.startNode->name == startNode && edge.endNode->name == endNode) {
                    selectedEdge = &edge;
                    break;
                }
            }

            if (selectedEdge) {
                // Изменяем цвет ребра
                selectedEdge->color = edgeColor;

                // Выводим информацию с окрашенным названием ребра
                std::cout << "Edge ";
                graphEditor.printColoredEdgeName(*selectedEdge);
                std::cout << " colored successfully.\n";
            }
            else {
                std::cerr << "Edge not found.\n";
            }
            break;
        }
        case 11:
            graphEditor.saveGraph(graphEditor.graphs.front());
            break;
        case 12:
            if (!graphEditor.graphs.empty()) {
                graphEditor.loadGraph(graphEditor.graphs.front());
            }
            else {
                std::cerr << "No graphs available to load." << std::endl;
            }
            break;
        case 13:
            graphEditor.setActiveGraph();
            break;
        case 14:
            if (!graphEditor.graphs.empty()) {
                graphEditor.findHamiltonianCycles(graphEditor.graphs[graphEditor.activeGraphIndex]);
            }
            else {
                std::cerr << "No graphs available to find Hamiltonian cycles." << std::endl;
            }
            break;
        case 15:
            if (!graphEditor.graphs.empty()) {
                graphEditor.convertToBinaryTree(graphEditor.graphs[graphEditor.activeGraphIndex]);
                graphEditor.binaryTree.printBinaryTree();
            }
            else {
                std::cerr << "No graphs available to convert to binary tree.\n";
            }
            break;
        case 16: {
            std::cout << "Enter node name: ";
            std::string searchNodeName;
            std::cin >> searchNodeName;

            auto result = graphEditor.findNodeByNameInGraphs(searchNodeName);
            int graphIndex = result.first;
            int nodeIndex = result.second;

            if (nodeIndex != -1) {
                const Graph& foundGraph = graphEditor.graphs[graphIndex];
                const Node& foundNode = foundGraph.nodes[nodeIndex];

                std::cout << "Node '" << foundNode.name << "' found in Graph '" << foundGraph.name << "'.";
                std::cout << " (Color: " << foundNode.color << ")\n";
            }
            else {
                std::cout << "Node was not found.\n";
            }
            break;
        }
        case 17:
            std::cout << "Exiting program.\n";
            break;
        default:
            std::cout << "Invalid choice. Try again.\n";
        }

    } while (choice != 17);

    return 0;
}
