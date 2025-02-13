from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
import streamlit as st
import os
from dotenv import load_dotenv

load_dotenv()
os.environ['OPENAI_API_KEY']=os.getenv("OPENAI_API_KEY")
# LangSmith Tracking
os.environ['LANGCHAIN_TRACKING_V2']="true"
os.environ['LANGCHAIN_API_KEY']=os.getenv('LANGCHAIN_API_KEY')


# Prompt Template

prompt=ChatPromptTemplate.from_messages(
    [
        ("system","You are a helpful assistant.Please respond according to the user query"),
        ("user","Question:{question}")
    ]
)

# Streamlit Framework

st.title("LangChain demo with openai api")
input_text=st.text_input("Search the topic u want")


# openAI

llm=ChatOpenAI(model="gpt-3.5-turbo")
output_parse=StrOutputParser()
chain=prompt|llm|output_parse

if input_text:
    st.write(chain.invoke({"question":input_text}))