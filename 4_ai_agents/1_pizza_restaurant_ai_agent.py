# import basics
import os
import sqlite3
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
You are a helpful assistant. You answer questions related to a pizza restaurant. You will be provided with a query and a chat history.

You have access to the following tool calls to serve the user:
- 'fetch_restaurant_info': Retrieve information about the pizza restaurant.
- 'fetch_menu': Retrieve information about the restaurants menu.
- 'create_order': Create a new order for the pizza restaurant
- 'add_item_to_order': Add an item to an existing order for the pizza restaurant. 

When you want to create a new order, first make sure you have all the order details, such as:

- customer first name + last name
- DATETIME object (in string) when the pizza should be delivered
- The pizzas that should be ordered (with quantity)             

When you have all these details, first create the order with the 'create_order' tool call, and then add the pizzas to the order with the 'add_item_to_order' tool call.                                                              
                                      
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
def fetch_restaurant_info():
    """Retrieve information about the pizza restaurant."""

    db_file = "restaurant.db"

    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()

    query = """
    SELECT *
    FROM restaurant_details"""

    cursor.execute(query)
    result = cursor.fetchall()

    conn.close()

    return result

@tool
def fetch_menu():
    """Retrieve information about the restaurants menu."""

    db_file = "restaurant.db"

    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()

    query = """
    SELECT *
    FROM pizza_menu"""

    cursor.execute(query)
    result = cursor.fetchall()

    conn.close()

    return result

@tool
def create_order(customer_name: str, order_time: str):
    """Create a new order for the pizza restaurant. Always provide customer first name + last name and DATETIME object (in string) when the pizza should be delivered."""

    db_file = "restaurant.db"

    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()


    cursor.execute("""
    INSERT INTO restaurant_orders (customer_name, order_time)
    VALUES (?, ?)
    """, (customer_name, order_time))

    conn.commit()
    conn.close()

    return True

@tool
def add_item_to_order(order_id: int, pizza_id: int, quantity: int):
    """Add an item to an existing order for the pizza restaurant"""

    db_file = "restaurant.db"

    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()


    cursor.execute("""
    INSERT INTO restaurant_orders_items (order_id, pizza_id, quantity)
    VALUES (?, ?, ?)
    """, (order_id, pizza_id, quantity))

    conn.commit()
    conn.close()

    return cursor.lastrowid


# combining all tools
tools = [fetch_restaurant_info, fetch_menu, create_order, add_item_to_order]

# initiating the agent
agent = create_tool_calling_agent(llm, tools, prompt)

# create the agent executor
agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)

# initiating streamlit app
st.set_page_config(page_title="AI Agent", page_icon="🍕")
st.title("🍕 AI Agent")

# initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# display chat messages from history on app rerun
for message in st.session_state.messages:
    if isinstance(message, HumanMessage):
        with st.chat_message("user"):
            st.markdown(message.content)
    elif isinstance(message, AIMessage):
        with st.chat_message("assistant"):
            st.markdown(message.content)


# create the bar where we can type messages
user_question = st.chat_input("How are you?")


# did the user submit a prompt?
if user_question:

    # add the message from the user (prompt) to the screen with streamlit
    with st.chat_message("user"):
        st.markdown(user_question)

        st.session_state.messages.append(HumanMessage(user_question))


    # invoking the agent
    result = agent_executor.invoke({"input": user_question, "chat_history":st.session_state.messages})

    ai_message = result["output"]

    # adding the response from the llm to the screen (and chat)
    with st.chat_message("assistant"):
        st.markdown(ai_message)

        st.session_state.messages.append(AIMessage(ai_message))