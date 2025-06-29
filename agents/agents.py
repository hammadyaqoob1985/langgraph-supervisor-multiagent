
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from langgraph.prebuilt import create_react_agent


from config.config import llm
from tools.tools import check_availability_by_doctor, check_availability_by_specialization, set_appointment, \
    cancel_appointment, reschedule_appointment

def create_agent(llm:ChatOpenAI,tools:list,system_prompt:str):
    system_prompt = ChatPromptTemplate.from_messages(
        [
            (
                "system",
                system_prompt
            ),
            ("placeholder", "{messages}"),
        ]
    )
    agent = create_react_agent(model=llm,tools=tools,prompt=system_prompt)
    return agent

information_agent = create_agent(
    llm=llm,
    tools=[check_availability_by_doctor,check_availability_by_specialization],
    system_prompt = "You are specialized agent to provide information related to availbility of doctors or any FAQs related to hospital based on the query. You have access to the tool.\n Make sure to ask user politely if you need any further information to execute the tool.\n For your information, Always consider current year is 2024."
)

booking_agent = create_agent(
    llm=llm,
    tools=[set_appointment,cancel_appointment,reschedule_appointment],
    system_prompt = "You are specialized agent to set, cancel or reschedule appointment based on the query. You have access to the tool.\n Make sure to ask user politely if you need any further information to execute the tool.\n For your information, Always consider current year is 2024."
)