# import basics
import os
from dotenv import load_dotenv

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
If necessary, you can use the tool 'get_temperature' to retrieve relevant information related to a query.
                                                       
The query is as follows:                    
{input}

The chat history is as follows:
{chat_history}
           
You can use the scratchpad to store any intermediate results or notes.
The scratchpad is as follows:
{agent_scratchpad}

""")


# creating the retriever tool
@tool
def get_temperature(city_name: str):
    """Retrieve information related to a query."""

    return "18 degrees Celsius"

# combining all tools
tools = [get_temperature]

# initiating the agent
agent = create_tool_calling_agent(llm, tools, prompt)

# create the agent executor
agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=False)

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



