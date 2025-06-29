from typing import Literal, Annotated, TypedDict

from langchain_core.messages import AIMessage, HumanMessage
from langgraph.constants import END
from langgraph.types import Command

from agents.AgentState import GraphState
from agents.agents import information_agent, booking_agent, doctor_profile_agent
from config.config import llm

members_dict = {'information_node':'specialized agent to provide information related to availability of doctors.\n Make sure to ask user politely if you need any further information to execute the tool.'
    ,'booking_node':'specialized agent to only to book, cancel, reschedule or get appointments'
                ,'doctor_profile_node':'specialized agent to provide information related to credentials and background information regarding the doctors and their specialisation. Use this agent when user has general faqs about the doctors in the hospital'}
options = list(members_dict.keys()) + ["FINISH"]
worker_info = '\n\n'.join([f'WORKER: {member} \nDESCRIPTION: {description}' for member, description in members_dict.items()]) + '\n\nWORKER: FINISH \nDESCRIPTION: If User Query is answered and route to Finished'

system_prompt = (
    "You are a supervisor tasked with managing a conversation between following workers. "
    "### SPECIALIZED ASSISTANT:\n"
    f"{worker_info}\n\n"
    "Your primary role is to help the user make an appointment with the doctor and doctor's availability and answer general queries about the doctors"
    "If a customer requests to know the availability of a doctor or to book, reschedule, or cancel an appointment, or to know about the doctor's profile"
    "delegate the task to the appropriate specialized workers. Given the following user request,"
    " respond with the worker to act next. Each worker will perform a"
    " task and respond with their results and status. When finished,"
    " respond with FINISH."
    "UTILIZE last conversation to assess if the conversation should end you answered the query, then route to FINISH "
)

class Router(TypedDict):
    """Worker to route to next. If no workers needed, route to FINISH. and provide reasoning for the routing"""

    next: Annotated[Literal[*options], ..., "worker to route to next, route to FINISH"]
    reasoning: Annotated[str, ..., "Support proper reasoning for routing to the worker"]

def information_node(state: GraphState):
    result = information_agent.invoke(state)
    return Command(
        update={
            "messages": state["messages"] + [
                AIMessage(content=result["messages"][-1].content, name="information_node")
            ]
        },
        goto="supervisor",
    )

def booking_node(state: GraphState):
    result = booking_agent.invoke(state)
    return Command(
        update={
            "messages": state["messages"] + [
                AIMessage(content=result["messages"][-1].content, name="booking_node")
            ]
        },
        goto="supervisor",
    )

def doctor_profile_node(state: GraphState):
    result = doctor_profile_agent.invoke(state)
    return Command(
        update={
            "messages": state["messages"] + [
                AIMessage(content=result["messages"][-1].content, name="doctor_profile_node")
            ]
        },
        goto="supervisor",
    )

def supervisor_node(state: GraphState) -> Command[Literal[*list(members_dict.keys()), "__end__"]]:
    print(state)
    messages = [
                   {"role": "system", "content": system_prompt},
                   #{"role": "user", "content": f"user's identification number is {state['id_number']}"},
               ] + [state["messages"][-1]]
    query = ''
    if len(state['messages'])==1:
        query = state['messages'][0].content
    response = llm.with_structured_output(Router).invoke(messages)
    goto = response["next"]
    if goto == "FINISH":
        goto = END
    if query:
        return Command(goto=goto, update={"next": goto,'query':query,'cur_reasoning':response["reasoning"],
                                          "messages":[HumanMessage(content=f"user's identification number is {state['id_number']}")]
                                          })
    return Command(goto=goto, update={"next": goto,'cur_reasoning':response["reasoning"]})