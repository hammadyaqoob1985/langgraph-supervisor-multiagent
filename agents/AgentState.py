from numbers import Number
from typing import TypedDict, Annotated

from langchain_core.messages import AnyMessage
from langgraph.graph import add_messages


class GraphState(TypedDict):
    messages: Annotated[list[AnyMessage], add_messages]
    id_number: Number