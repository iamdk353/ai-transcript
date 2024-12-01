import streamlit as st
from dotenv import load_dotenv
load_dotenv()
import google.generativeai as genai
import os
genai.configure(api_key=os.getenv("google_api_key"))
from youtube_transcript_api import YouTubeTranscriptApi

def getData(url:str):
  ai=genai.GenerativeModel("gemini-pro")
  prompt="""
    you are a yt summeriser summerise this youtube video in 250 words 
    here youtube transcript :

"""
  if (getTranscript(url=url)):
    resp=ai.generate_content(prompt+getTranscript(url=url))
    return(resp.text)

def getTranscript(url:str):
  
  try:
    with st.spinner("loading"):
      videoId=url.split("=")[1]
      text=YouTubeTranscriptApi.get_transcript(video_id=videoId)
      if(len(text)>2500):
        st.warning("video is too long")
        return 
      if(len(text)<20):
        st.warning("video may be a song or doesnt have a subtitle")
        return 
      transcript=""
      for i in text:
        transcript+=" "+i["text"]
      return transcript
  except Exception as e:
      raise "could not retrive transcript of the video"

st.title("AI YOUTUBE VIDEO EXPLANATION BOT")
ytLink=st.text_input("enter yt link")
if ytLink:
   videoId=ytLink.split("=")[1]
   st.image(f"http://img.youtube.com/vi/{videoId}/0.jpg",use_container_width=True)
   st.write(getData(ytLink))
# "AIzaSyCrf1ChQC24gck0Vbt_M-sVPbr_DdRej8Y"