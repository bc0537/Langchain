import streamlit as st
import os
from langchain_groq import ChatGroq
from langchain_community.document_loaders import WebBaseLoader
from langchain.embeddings import OpenAIEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import ChatPromptTemplate
from langchain.chains import create_retrieval_chain
from langchain_community.vectorstores import FAISS
from dotenv import load_dotenv
import time

load_dotenv()

# Loading the Groq API Key
# os.environ['GROQ_API_KEY']=os.getenv("GROQ_API_KEY")
groq_api_key=os.getenv("GROQ_API_KEY")

if "vector" not in  st.session_state:
    st.session_state.embeddings=OpenAIEmbeddings()
    # reading the content from langsmith using webpage loader
    st.session_state.loader=WebBaseLoader("https://docs.smith.langchain.com/") 
    st.session_state.docs=st.session_state.loader.load()

    st.session_state.text_splitter=RecursiveCharacterTextSplitter(chunk_size=1000,chunk_overlap=250)
    st.session_state.final_documents=st.session_state.text_splitter.split_documents(st.session_state.docs[:50])
    st.session_state.vectors=FAISS.from_documents(st.session_state.final_documents,st.session_state.embeddings)
    

st.title("Chat Groq Demo")

llm=ChatGroq(groq_api_key=groq_api_key,
             model_name="mixtral-8x7b-32768")


prompt=ChatPromptTemplate.from_template(
"""
Answer the question based on the provided context only.
Please provide the most accurate response based on question
<context>
{context}
</context>
Question:{input}

"""
)

document_chain=create_stuff_documents_chain(llm,prompt)
retriever=st.session_state.vectors.as_retriever()
retrieval_chain=create_retrieval_chain(retriever,document_chain)

prompt1=st.text_input("Enter your prompt here")

if prompt1:
    start=time.process_time()
    response=retrieval_chain.invoke({"input":prompt1}) 
    print("Response time:",time.process_time() - start)
    st.write(response['answer'])

    with st.expander("Document Similarity Search"):
        for i,doc in enumerate(response['context']):
            st.write(doc.page_content)
            st.write("----------------------------------")



