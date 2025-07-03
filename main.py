from fastapi import FastAPI, Request
from pydantic import BaseModel
from langchain_core.messages import HumanMessage
from graph.graph import graph
import uvicorn

app = FastAPI()

class InvokeRequest(BaseModel):
    message: str
    id_number: int

@app.post("/invoke")
async def invoke_graph(request: InvokeRequest):
    inputs = [HumanMessage(content=request.message)]
    config = {"configurable": {"thread_id": "1", "recursion_limit": 10}}
    state = {'messages': inputs, 'id_number': request.id_number}
    result = graph.invoke(input=state, config=config)
    latest_message = result['messages'][-1] if result['messages'] else None
    return {"result": latest_message.content}

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
