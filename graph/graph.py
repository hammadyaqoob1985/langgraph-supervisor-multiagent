from langgraph.constants import START
from langgraph.graph import StateGraph

from agents.AgentState import GraphState
from nodes.nodes import supervisor_node, information_node, booking_node

builder = StateGraph(GraphState)
builder.add_edge(START, "supervisor")
builder.add_node("supervisor", supervisor_node)
builder.add_node("information_node", information_node)
builder.add_node("booking_node", booking_node)
graph = builder.compile()