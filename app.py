from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_groq import ChatGroq
import langchain
from langchain.agents import create_agent
from tavily import TavilyClient
import pytesseract as pyt
import streamlit as st
import os
import time
from PIL import Image
import pandas as pd
import numpy as np

# To Show web-app: complete page layout
st.set_page_config(layout="wide")
# To Give Title
st.title("AI RESUME GENERATOR")
st.write("""This app helps user to build customized Professional
Resume with Latest Job apply links""")
st.image("bg.jpg")
#=======api key========
TAVILY_API_KEY="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"
GOOGLE_API_KEY="AQ.Ab8RN6IZJpjfyC0XgDAdvQg6idHs_z7yFnTHOxTFwOs0_HvE5g"
Groq_API_KEY="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"

#======google api key===========
model=ChatGoogleGenerativeAI(
    model= "gemini-3.5-flash-lite",
    google_api_key=GOOGLE_API_KEY
)

'''response= model.invoke("Hey bro ,how are you?")
response.content[-1]['text']'''

#=============tavily api key================
def search_latest_news_jobs(query):
  '''this  function helps to fetch latest
    news or jobs related article using tavily'''

  client=TavilyClient(
      api_key=TAVILY_API_KEY)
  response=client.search(query)
  return response

#==================agent==============
agent = create_agent(
    model=model,
    tools=[search_latest_news_jobs]
)


#=======================main code to create resume using agent=====================

def main_agent(agent,query):
  """this is main agent or  agent
  orchestrate sub agent"""
  #giving prompt to create deatiled prompt for code generation
  prompt=""" you are AI assistant and below given is aprompt , your task is to give detailed prompt for this,
  you are professional Resume generator where user will give there personal details ,
  you have to create a detailed Resume for student that can be shortlist in companies like google
  and microsoft .it must be with dynamic UI and UX and with advanced CSS professional designing
  make sure to give output in html format only to markdown allowed"""

  response = agent.invoke({'messages':[{'role':'user','content':prompt}]})
  detailed_prompt=response['messages'][-1].content[-1]['text']

  with open('prompt.txt','w')as f:
    f.write(detailed_prompt)


  user_details = """Below Given is a user details
  generate Resume based on that, if not
  given keep: Default Resume: Python Developer
  user details:{query}"""
def main_agent(agent,query):
  """this is main agent or  agent
  orchestrate sub agent"""
  #giving prompt to create deatiled prompt for code generation
  prompt=''' you are AI assistant and below given is aprompt , your task is to give detailed prompt for this,
  you are professional Resume generator where user will give there personal details ,
  you have to create a detailed Resume for student that can be shortlist in companies like google
  and microsoft .it must be with dynamic UI and UX and with advanced CSS professional designing
  make sure to give output in html format only to markdown allowed  '''

  response = agent.invoke({'messages':[{'role':'user','content':prompt}]})
  detailed_prompt=response['messages'][-1].content[-1]['text']

  with open('prompt.txt','w')as f:
    f.write(detailed_prompt)


  user_details ="""Below Given is a user details
  generate Resume based on that, if not
  given keep: Default Resume: Python Developer
  user details:{query}"""

  final_prompt = prompt + detailed_prompt + user_details

# CODE GENERATION
  response = agent.invoke({'messages': [{'role':'user','content':final_prompt}]})
  code = response['messages' ] [-1].content[-1] ['text' ]
  return code

#==============display code (resume)=========
'''code = main_agent(agent, "ALAN TURING, GEN AI EXPERT")
from IPython import display as DISPLAY
DISPLAY.HTML(code)'''

#==================job_searching code================ 
def get_jobs(agent,
             Location="Noida,Delhi,Gurugram",
             Profile="Data Analyst, SDE"):
    Location="Noida,Delhi,Gurugram"
    Profile="Data Analyst, SDE"
    prompt="""based on user given job profile ,
    using naukri ,linkedin,indeed and other popular platform which are trusted and used to apply job ,
    show results with job profile name ,location,salary ,company name ,requirements
    show only jobs related to given {Location}and {Profile},output must be in proffessional html naukri theme  cards with dynamic design,
    show only top 15 results means jobs"""
    response=agent.invoke({'messages':[{'role':'user','content':prompt}]})
    code=response['messages'][-1].content[-1]['text']

    return code

#==================display code for jobs searching==============
'''code=get_jobs(agent)
DISPLAY.HTML(code)'''
