import requests 
import streamlit as st



def get_openai_response(input_text):
    response=requests.post("http://localhost:8000/essay/invoke",
                           json={"input":{"topic":input_text}})
    

    return response.json()['output']['content']

## streamlit

st.header("LangChain Demo")
input_text=st.text_input("Write an topic which will generate essay")

if input_text:
    st.write(get_openai_response(input_text=input_text))



