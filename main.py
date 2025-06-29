from langchain_core.messages import HumanMessage
from graph.graph import graph


def main():
    inputs = [
        HumanMessage(content='Can you tell me about the qualification of the doctor Michael Green?')
    ]



    config = {"configurable": {"thread_id": "1", "recursion_limit": 10}}

    state = {'messages': inputs,'id_number':10232303}
    print(state)
    result = graph.invoke(input=state,config=config)
    print(result)

if __name__ == "__main__":
    main()