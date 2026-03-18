#################################################################################################################################################################
###############################   1.  IMPORTING MODULES AND INITIALIZING VARIABLES   ############################################################################
#################################################################################################################################################################

from dotenv import load_dotenv
import os
import json
import pandas as pd
from langchain_chroma import Chroma
from langchain_openai import OpenAIEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import PyPDFDirectoryLoader
from langchain_community.document_loaders import TextLoader
from uuid import uuid4
import shutil
import time


load_dotenv()

###############################   INITIALIZE EMBEDDINGS MODEL  #################################################################################################

embeddings = OpenAIEmbeddings(
    model=os.getenv("EMBEDDING_MODEL"),
)

###############################   DELETE CHROMA DB IF EXISTS AND INITIALIZE   ##################################################################################

if os.path.exists(os.getenv("DATABASE_LOCATION")):
    shutil.rmtree(os.getenv("DATABASE_LOCATION"))


###############################   INITIALIZE TEXT SPLITTER   ###################################################################################################


loader = PyPDFDirectoryLoader(os.getenv("DATASET_STORAGE_FOLDER"))

# split the documents in multiple chunks
documents = loader.load()

# Add source metadata before splitting
for doc in documents:
    # often already present, but this makes it explicit
    doc.metadata["source"] = doc.metadata.get("source", "unknown")

# Split into chunks
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000,
    chunk_overlap=100
)
docs = text_splitter.split_documents(documents)

# Store chunks in Chroma
vector_store = Chroma.from_documents(
    collection_name=os.getenv("COLLECTION_NAME"),
    persist_directory=os.getenv("DATABASE_LOCATION"), 
    documents=docs,
    embedding=embeddings
)