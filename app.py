from langchain.document_loaders import PyPDFLoader
from langchain.indexes import VectorstoreIndexCreator
from langchain.chains import RetrievalQA
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings import HuggingFaceEmbeddings
from langchain_community.chat_models import ChatOllama
from langchain_chroma import Chroma
import json

from glob import glob
import streamlit as st
import ollama
from typing import Dict, Generator

from create_db import get_or_create_collection, vectorize_text, query_collection, add_paragraphs_to_collection, delete_collection, preprocess_text
import logging
import chromadb
from chromadb import Client
from chromadb.config import Settings
from fpdf import FPDF

logging.getLogger("chromadb.segment.impl.metadata.sqlite").setLevel(logging.ERROR)
logging.getLogger("chromadb.segment.impl.vector.local_hnsw").setLevel(logging.ERROR)


### LLM 🤓
def ollama_generator(messages: Dict) -> Generator:
    stream = ollama.chat(
            model="llava:7b",
            messages=messages,
            stream=True
        )
    for chunk in stream:
        yield chunk['message']['content']



folder_path= '/Users/rayaneghilene/Documents/Ollama/Mirakl_chatbot/PDF_files'
@st.cache_resource
def load_pdf():
    # pdf_name ='Issues with Entailment-based Zero-shot Text Classification.pdf'
    #loaders = [PyPDFLoader(pdf_name)]
    pdf_files = glob(f"{folder_path}/*.pdf")
    loaders = [PyPDFLoader(file_path) for file_path in pdf_files]

    index= VectorstoreIndexCreator(
        embedding = HuggingFaceEmbeddings(model_name= 'all-MiniLM-L12-V2'),
        text_splitter=RecursiveCharacterTextSplitter(chunk_size=100, chunk_overlap=0)
    ).from_loaders(loaders)
    return index

index = load_pdf()


### Chain

chain= RetrievalQA.from_chain_type(
    llm= ChatOllama(model="llava:7b"),
    chain_type ='stuff',
    retriever= index.vectorstore.as_retriever(),
    # retriever= Chroma(client=client, collection_name=collection_name),

    input_key='question'
)



### INTERFACE

with st.sidebar:
    # st.title('Side Bar')
    st.image('/Users/rayaneghilene/Documents/Ollama/Mirakl_chatbot/Images/Mirakl_logo.png',  use_column_width='auto')
    # st.file_uploader('Upload your own file')
st.title('Mirakl Chatbot')

if 'messages' not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    st.chat_message(message['role']).markdown(message['content'])

prompt = st.chat_input('Insert your text here :)')




if prompt: 
    st.chat_message('user').markdown(prompt)
    st.session_state.messages.append({'role': 'user', 'content': prompt})
    
    st.spinner(text='In progress')
    
    response = chain.run(prompt)
    st.chat_message("assistant").markdown(response)

    st.session_state.messages.append( {"role": "assistant", "content": response})   