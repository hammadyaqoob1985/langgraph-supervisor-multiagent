import os

from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from pydantic import BaseModel
from langchain_core.messages import HumanMessage
from app.graph.graph import graph
import uvicorn
from dotenv import load_dotenv

load_dotenv()
app = FastAPI()

class InvokeRequest(BaseModel):
    message: str
    id_number: int
    conversation_id: int

@app.get("/")
async def redirect_root_to_docs():
    return RedirectResponse("/docs")
@app.post("/invoke")
async def invoke_graph(request: InvokeRequest):
    inputs = [HumanMessage(content=request.message)]
    config = {"recursion_limit": 25, "configurable": {"thread_id": request.conversation_id}}
    state = {'messages': inputs, 'id_number': request.id_number}
    result = graph.invoke(input=state, config=config)
    latest_message = result['messages'][-1] if result['messages'] else None
    return {"result": latest_message.content}

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
