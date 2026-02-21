import os
from dotenv import load_dotenv

load_dotenv()

from langchain.chat_models import init_chat_model

llm = init_chat_model("gpt-4.1")

output = llm.invoke("write a story about an astronaut")

print(output.content)