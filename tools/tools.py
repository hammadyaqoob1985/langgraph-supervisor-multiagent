## Tools For Booking agent
from typing import Literal

import pandas as pd
from langchain_core.tools import tool, create_retriever_tool

from config.config import faiss_db
from model.schema import DateModel, DateTimeModel, IdentificationNumberModel

@tool
def check_availability_by_doctor(doctor_name:Literal['kevin anderson','robert martinez','susan davis','daniel miller','sarah wilson','michael green','lisa brown','jane smith','emily johnson','john doe']):
    """
    Checking the database if we have availability for the specific doctor.
    The parameters should be mentioned by the user in the query
    """
    df = pd.read_csv(f"availability.csv")
    rows = list(df[(df['doctor_name'] == doctor_name)&(df['is_available'] == True)]['date_slot'])

    if len(rows) == 0:
        output = "No availability in the entire day"
    else:
        output = "Available slots: " + ', '.join(rows)

    return output

@tool
def check_availability_by_specialization(specialization:Literal["general_dentist", "cosmetic_dentist", "prosthodontist", "pediatric_dentist","emergency_dentist","oral_surgeon","orthodontist"]):
    """
    Checking the database if we have availability for the specific specialization.
    The parameters should be mentioned by the user in the query
    """
    #Dummy data
    df = pd.read_csv(f"availability.csv")
    rows = df[(df['specialization'] == specialization) & (df['is_available'] == True)].groupby(['specialization', 'doctor_name'])['date_slot'].apply(list).reset_index(name='available_slots')

    if len(rows) == 0:
        output = "No availability in the entire day"
    else:
        def convert_to_am_pm(time_str):
            # Split the time string into hours and minutes
            time_str = str(time_str)
            hours, minutes = map(int, time_str.split("."))

            # Determine AM or PM
            period = "AM" if hours < 12 else "PM"

            # Convert hours to 12-hour format
            hours = hours % 12 or 12

            # Format the output
            return f"{hours}:{minutes:02d} {period}"
        for row in rows.values:
            output = row[1] + ". Available slots: \n" + ', \n'.join([value for value in row[2]])+'\n'

    return output

@tool
def check_availability_by_doctor_by_date(desired_date:DateModel, doctor_name:Literal['kevin anderson','robert martinez','susan davis','daniel miller','sarah wilson','michael green','lisa brown','jane smith','emily johnson','john doe']):
    """
    Checking the database if we have availability for the specific doctor  date.
    The parameters should be mentioned by the user in the query
    """
    df = pd.read_csv(f"availability.csv")
    df['date_slot_time'] = df['date_slot'].apply(lambda input: input.split(' ')[-1])
    rows = list(df[(df['date_slot'].apply(lambda input: input.split(' ')[0]) == desired_date.date)&(df['doctor_name'] == doctor_name)&(df['is_available'] == True)]['date_slot_time'])

    if len(rows) == 0:
        output = "No availability in the entire day"
    else:
        output = f'This availability for {desired_date.date}\n'
        output += "Available slots: " + ', '.join(rows)

    return output

@tool
def check_availability_by_specialization_by_date(desired_date:DateModel, specialization:Literal["general_dentist", "cosmetic_dentist", "prosthodontist", "pediatric_dentist","emergency_dentist","oral_surgeon","orthodontist"]):
    """
    Checking the database if we have availability for the specific specialization given a date.
    The parameters should be mentioned by the user in the query
    """
    #Dummy data
    df = pd.read_csv(f"availability.csv")
    df['date_slot_time'] = df['date_slot'].apply(lambda input: input.split(' ')[-1])
    rows = df[(df['date_slot'].apply(lambda input: input.split(' ')[0]) == desired_date.date) & (df['specialization'] == specialization) & (df['is_available'] == True)].groupby(['specialization', 'doctor_name'])['date_slot_time'].apply(list).reset_index(name='available_slots')

    if len(rows) == 0:
        output = "No availability in the entire day"
    else:
        def convert_to_am_pm(time_str):
            # Split the time string into hours and minutes
            time_str = str(time_str)
            hours, minutes = map(int, time_str.split("."))

            # Determine AM or PM
            period = "AM" if hours < 12 else "PM"

            # Convert hours to 12-hour format
            hours = hours % 12 or 12

            # Format the output
            return f"{hours}:{minutes:02d} {period}"
        output = f'This availability for {desired_date.date}\n'
        for row in rows.values:
            output += row[1] + ". Available slots: \n" + ', \n'.join([convert_to_am_pm(value)for value in row[2]])+'\n'

    return output

## Tools For Booking agent
@tool
def reschedule_appointment(old_date:DateTimeModel, new_date:DateTimeModel, id_number:IdentificationNumberModel, doctor_name:Literal['kevin anderson','robert martinez','susan davis','daniel miller','sarah wilson','michael green','lisa brown','jane smith','emily johnson','john doe']):
    """
    Rescheduling an appointment.
    The parameters MUST be mentioned by the user in the query.
    """
    #Dummy data
    df = pd.read_csv(f'availability.csv')
    available_for_desired_date = df[(df['date_slot'] == new_date.date)&(df['is_available'] == True)&(df['doctor_name'] == doctor_name)]
    if len(available_for_desired_date) == 0:
        return "Not available slots in the desired period"
    else:
        cancel_appointment.invoke({'date':old_date, 'id_number':id_number, 'doctor_name':doctor_name})
        set_appointment.invoke({'desired_date':new_date, 'id_number': id_number, 'doctor_name': doctor_name})
        return "Succesfully rescheduled for the desired time"

@tool
def cancel_appointment(date:DateTimeModel, id_number:IdentificationNumberModel, doctor_name:Literal['kevin anderson','robert martinez','susan davis','daniel miller','sarah wilson','michael green','lisa brown','jane smith','emily johnson','john doe']):
    """
    Canceling an appointment.
    The parameters MUST be mentioned by the user in the query.
    """
    df = pd.read_csv(f'availability.csv')
    case_to_remove = df[(df['date_slot'] == date.date)&(df['patient_to_attend'] == id_number.id)&(df['doctor_name'] == doctor_name)]
    if len(case_to_remove) == 0:
        return "You don´t have any appointment with that specifications"
    else:
        df.loc[(df['date_slot'] == date.date) & (df['patient_to_attend'] == id_number.id) & (df['doctor_name'] == doctor_name), ['is_available', 'patient_to_attend']] = [True, None]
        df.to_csv(f'availability.csv', index = False)

        return "Succesfully cancelled"

@tool
def set_appointment(desired_date:DateTimeModel, id_number:IdentificationNumberModel, doctor_name:Literal['kevin anderson','robert martinez','susan davis','daniel miller','sarah wilson','michael green','lisa brown','jane smith','emily johnson','john doe']):
    """
    Set appointment or slot with the doctor.
    The parameters MUST be mentioned by the user in the query.
    """
    df = pd.read_csv(f'availability.csv')
    from datetime import datetime


    def convert_datetime_format(dt_str):
        # Parse the input datetime string
        dt = datetime.strptime(dt_str, "%Y-%m-%d %H:%M")

        # Format the output as 'DD-MM-YYYY H.M' (removing leading zero from hour only)
        return dt.strftime("%d-%m-%Y %#H.%M")

    case = df[(df['date_slot'] == convert_datetime_format(desired_date.date))&(df['doctor_name'] == doctor_name)&(df['is_available'] == True)]
    if len(case) == 0:
        return "No available appointments for that particular case"
    else:
        df.loc[(df['date_slot'] == convert_datetime_format(desired_date.date))&(df['doctor_name'] == doctor_name) & (df['is_available'] == True), ['is_available','patient_to_attend']] = [False, id_number.id]
        df.to_csv(f'availability.csv', index = False)

        return "Succesfully done"

# Remove embedding/index creation from here. Instead, expect a setter to inject the FAISS db at runtime.
# _faiss_db = None

# def set_faiss_db(faiss_db):
#     global _faiss_db
#     _faiss_db = faiss_db

retrieve_doctor_information = create_retriever_tool(
    faiss_db.as_retriever(),
    "doctor_information_retriever",
    "Fetches background and credentials about doctors.",
)
# @tool
# def retrieve_doctor_information(query: str):
#     """
#     Retrieve relevant information from the local knowledge base using OpenAI embeddings and FAISS vector search.
#     """
#     if _faiss_db is None:
#         return "Knowledge base is not initialized."
#     results = _faiss_db.similarity_search(query, k=3)
#     if not results:
#         return "No relevant information found in the knowledge base."
#     return '\n'.join([r.page_content for r in results])

