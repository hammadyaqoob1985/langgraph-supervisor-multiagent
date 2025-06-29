from langgraph.checkpoint.memory import MemorySaver
from langgraph.constants import START
from langgraph.graph import StateGraph

from agents.AgentState import GraphState
from nodes.nodes import supervisor_node, information_node, booking_node, doctor_profile_node

builder = StateGraph(GraphState)
memory = MemorySaver()
builder.add_edge(START, "supervisor")
builder.add_node("supervisor", supervisor_node)
builder.add_node("information_node", information_node)
builder.add_node("booking_node", booking_node)
builder.add_node("doctor_profile_node", doctor_profile_node)
graph = builder.compile(checkpointer=memory)