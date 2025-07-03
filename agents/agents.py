from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from langgraph.prebuilt import create_react_agent


from config.config import llm
from tools.tools import check_availability_by_doctor, check_availability_by_specialization, set_appointment, \
    cancel_appointment, reschedule_appointment, retrieve_doctor_information, check_availability_by_doctor_by_date, \
    check_availability_by_specialization_by_date, get_appointments


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
    tools=[check_availability_by_doctor,check_availability_by_specialization,check_availability_by_doctor_by_date,check_availability_by_specialization_by_date],
    system_prompt = """You are specialized agent to provide availability of doctors. 
    This will include returning the available slots for a particular doctor or specialization.
    This user can provide a date, a doctor's name or a specialisation.
    Once you have done the information go back to the supervisor agent.
    For any other requests outside this scope go back to the supervisor agent
    """
)

booking_agent = create_agent(
    llm=llm,
    tools=[set_appointment,cancel_appointment,reschedule_appointment, get_appointments],
    system_prompt = """You are specialized agent who has access to appointments for all customers
    You are able to get, set, cancel and reschedule appointments based on the query.
    Once you have done the information go back to the supervisor agent.
    For any other requests outside this scope go back to the supervisor agent""")

doctor_profile_agent = create_agent(
    llm=llm,
    tools=[retrieve_doctor_information],
    system_prompt = """You are specialized agent to provide information 
    related to background information regarding the doctors. This includes credentials, board certifications, 
    universities they went to, their years of experience and their specialisation
    Once you have provided the information go back to supervisor agent. 
    For any other requests outside this scope go back to the supervisor agent.
    For any actions regarding finding avaialability or making bookings go back to the supervisor agent.""")
