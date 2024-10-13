import streamlit as st
import os
from dotenv import load_dotenv
import google.generativeai as genai

#load environment variables
load_dotenv('codespace.env')

# Retrieve the API key

api_keyy = os.getenv('GOOGLE_API_KEY')
if api_keyy is None:
    st.error("API key not found. Please check your .env file.")
else:
    genai.configure(api_key=api_keyy)

model = genai.GenerativeModel("gemini-1.5-flash")

user_input = st.text_input("Enter the ingredients you would like to use: ")

healthy = st.checkbox("Limit calories?")

if healthy:
    calorie_limit = st.text_input("Enter calories limit: ")



if st.button("Generate recipie"):
    if healthy:
        response = model.generate_content("Give me a recipie I can make with only the following ingredients and is under" + calorie_limit + " calories if possible: " + user_input)
    else:
        response = model.generate_content("Give me a recipie I can make with the following ingredients: " + user_input)
    # Display the response in the Streamlit app
    st.write(response.text)

