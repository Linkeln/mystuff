#include <cstdint>
#include <iostream>
#include <sc-memory/sc_memory.hpp>
#include <sys/types.h>
#include <unordered_map>

#include <sc-agents-common/utils/AgentUtils.hpp>
#include <sc-agents-common/utils/IteratorUtils.hpp>

#include "MyAgent.hpp"

using namespace utils;
using namespace std;

namespace exampleModule {

ScAddr getReverseEdge(unique_ptr<ScMemoryContext>& ms_context, ScAddr actionNode, ScAddr edge) {
	ScAddr sourceV = ms_context->GetEdgeSource(edge);
	ScAddr targetV = ms_context->GetEdgeTarget(edge);

	ScIterator3Ptr nodes_it = ms_context->Iterator3(actionNode, ScType::EdgeAccessConstPosPerm, ScType::NodeConst);
	while (nodes_it->Next()) {
		ScAddr node = nodes_it->Get(2);
		ScIterator5Ptr edges_it = ms_context->Iterator5(node, ScType::EdgeDCommonConst, ScType::NodeConst, ScType::EdgeAccessConstPosPerm, actionNode);
		while (edges_it->Next()) {
			ScAddr otherTargetNode = edges_it->Get(2);
			if (otherTargetNode.Hash() == sourceV.Hash() && targetV.Hash() == node.Hash())
				return edges_it->Get(1);
		}
	}
	return ScAddr::Empty;
}

bool isCyclicUtil(unique_ptr<ScMemoryContext>& ms_context, ScAddr actionNode, ScAddr curNode, unordered_map<uint64_t, bool>& visited, unordered_map<uint64_t, bool>& recStack, ScAddr edgeToNotVisit) {
	if (!visited[curNode.Hash()]) {
		visited[curNode.Hash()] = true;
		recStack[curNode.Hash()] = true;
		
		ScIterator5Ptr edges_it = ms_context->Iterator5(curNode, ScType::EdgeDCommonConst, ScType::NodeConst, ScType::EdgeAccessConstPosPerm, actionNode);
		while (edges_it->Next()) {
			ScAddr curEdge = edges_it->Get(1);
			if (curEdge.Hash() == edgeToNotVisit.Hash()) {
				continue;
			}
			ScAddr otherV = edges_it->Get(2);
			ScAddr reverseEdge = getReverseEdge(ms_context, actionNode, curEdge);
			if (!visited[otherV.Hash()] && isCyclicUtil(ms_context, actionNode, otherV, visited, recStack, reverseEdge)) {
				return true;
			}
			else if (recStack[otherV.Hash()])
				return true;
		}

	}

	recStack[curNode.Hash()] = false;
	return false;
}

bool isCyclic(unique_ptr<ScMemoryContext>& ms_context, ScAddr actionNode, unordered_map<uint64_t, bool>& visited, unordered_map<uint64_t, bool>& recStack) {
	ScIterator3Ptr nodes_it = ms_context->Iterator3(actionNode, ScType::EdgeAccessConstPosPerm, ScType::NodeConst);
	while (nodes_it->Next()) {
		ScAddr node = nodes_it->Get(2);
		if (!visited[node.Hash()] && isCyclicUtil(ms_context, actionNode, node, visited, recStack, ScAddr::Empty))
			return true;
	}
	return false;
}

SC_AGENT_IMPLEMENTATION(MyAgent) {
	SC_LOG_INFO("MyAgent started");
	ScAddr actionNode = otherAddr;
	unordered_map<uint64_t, bool> visited;
	unordered_map<uint64_t, bool> recStack;

	ScIterator3Ptr nodes_it = ms_context->Iterator3(actionNode, ScType::EdgeAccessConstPosPerm, ScType::NodeConst);
	while (nodes_it->Next()) {
		ScAddr node = nodes_it->Get(2);
		visited[node.Hash()] = false;
		recStack[node.Hash()] = false;
	}

	if (isCyclic(ms_context, actionNode, visited, recStack)) {
		ScAddr cyclicClass = ms_context->HelperResolveSystemIdtf("Cyclic graphs", ScType::NodeConstClass);
		ms_context->CreateEdge(ScType::EdgeAccessConstPosPerm, cyclicClass, actionNode);
		utils::AgentUtils::finishAgentWork(ms_context.get(), actionNode, true);
		SC_LOG_INFO("MyAgent: finished");
		return SC_RESULT_OK;

	}
	ScAddr notCyclicClass = ms_context->HelperResolveSystemIdtf("Acyclic graphs", ScType::NodeConstClass);
	ms_context->CreateEdge(ScType::EdgeAccessConstPosPerm, notCyclicClass, actionNode);

	utils::AgentUtils::finishAgentWork(ms_context.get(), actionNode, true);
	SC_LOG_INFO("MyAgent: finished");
	return SC_RESULT_OK;
}

}
