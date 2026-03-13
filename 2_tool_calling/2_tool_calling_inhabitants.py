# import basics
import os
from dotenv import load_dotenv
import sqlite3

# import streamlit
import streamlit as st

# import langchain
from langchain_classic.agents import AgentExecutor
from langchain_chroma import Chroma
from langchain_openai import OpenAIEmbeddings
from langchain.chat_models import init_chat_model
from langchain_core.messages import AIMessage, HumanMessage
from langchain_classic.agents import create_tool_calling_agent
from langchain_core.prompts import PromptTemplate
from langchain_core.tools import tool

# load environment variables
load_dotenv()  


###############################   INITIALIZE CHAT MODEL   #######################################################################################################

llm = init_chat_model(
    os.getenv("CHAT_MODEL"),
    temperature=0.5
)


# pulling prompt from hub
prompt = PromptTemplate.from_template("""                                
You are a helpful assistant. You will be provided with a query and a chat history.
If necessary, you can use the tool 'get_country_inhabitants' to retrieve relevant information about how many people live in a country.
                                                       
The query is as follows:                    
{input}

The chat history is as follows:
{chat_history}
           
You can use the scratchpad to store any intermediate results or notes.
The scratchpad is as follows:
{agent_scratchpad}

""")


# fetching inhabitants from database
@tool
def get_country_inhabitants(country_iso_code: str):
    """Retrieve information related to a query. Be aware that the input is the 3 digit ISO code of a country, not the country name."""

    conn = sqlite3.connect("world_data.db")
    cursor = conn.cursor()

    # TODO: voeg hier je eigen SQL query toe
    query = """
    SELECT *
    FROM population_data
    WHERE country_iso_code = ?
    """

    cursor.execute(query, (country_iso_code,))
    result = cursor.fetchall()

    conn.close()

    return result

# combining all tools
tools = [get_country_inhabitants]

# initiating the agent
agent = create_tool_calling_agent(llm, tools, prompt)

# create the agent executor
agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)

# initiating application

messages = []


while True:

    human_message = input("User (type quit to exit):")

    if(human_message == "quit"):
        break

    print(f"You say: {human_message}")

    messages.append(HumanMessage(human_message))

    result = agent_executor.invoke({"input": human_message, "chat_history": messages})


    print(f"AI says: {result['output']}")

    messages.append(AIMessage(result["output"]))



