import streamlit as st
import os
from dotenv import load_dotenv
import google.generativeai as genai

st.set_page_config(layout="wide")

def custom_css():
    st.markdown(
        """
        <style>
            @import url('https://fonts.googleapis.com/css2?family=League+Spartan:wght@400;700&display=swap');

            .stApp {
                background-color: #071013;
                font-family: 'League Spartan', sans-serif;  /* Applying the League Spartan font */
            }
            
            h1, h2, h3, h4, h5, h6 {
                color: #DFE0E2 !important;
                font-family: 'League Spartan', sans-serif;  /* Applying the League Spartan font */
                font-size: 45px; /* Increasing font size for headers */
            }
            
            div, span, p, label {
                color: #DFE0E2 !important;
                font-family: 'League Spartan', sans-serif;  /* Applying the League Spartan font */
                font-size: 18px; /* Increasing font size for regular text */
            }
            
            .stTextInput input, .stTextArea textarea {
                color: #DFE0E2 !important; /* making input text white */
            }
        </style>
        """,
        unsafe_allow_html=True
    )

def main():
    custom_css()

# Load API key
load_dotenv('codespace.env')
api_key = os.getenv('GOOGLE_API_KEY')
if api_key is None:
    st.error("API key not found. Please check your .env file.")
else:
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel("gemini-1.5-flash")

# App header and horizontal line
st.title('EasyEats Recipe Generator')

# User inputs

user_input = st.text_input("Enter the ingredients you would like to use:")
calorie_limit = st.slider("Set your calorie limit:", 100, 3000, 800)
meal_type = st.radio("What type of meal are you making?", options=["Breakfast", "Lunch", "Dinner", "Snack"], horizontal = True)
dietary_preferences = st.multiselect("Do you have any dietary restrictions or preferences?", ("None", "Vegan", "Gluten-Free", "Keto", "Paleo", "Dairy-Free", "Vegetarian"))
avoid_ingredients = st.text_input("Are there any ingredients you're allergic to or would prefer to avoid?")
cuisine_preference = st.selectbox("Do you have a preference for a specific cuisine?", ("No preference", "Italian", "Mexican", "Asian", "American", "French", "Indian", "Middle Eastern"))
cooking_time = st.slider("How much time do you have for cooking?", 5, 120, 30)

# Generating and displaying recipe
if user_input:
    prompt = f"Give me a {meal_type.lower()} recipe I can make with the following ingredients: {user_input}"
    if cuisine_preference != "No preference":
        prompt += f" in {cuisine_preference} style"
    if dietary_preferences:
        prompt += f" that is {' and '.join(dietary_preferences).lower()}"
    if avoid_ingredients:
        prompt += f", avoiding {avoid_ingredients}"
    prompt += f" under {calorie_limit} calories, that can be prepared in {cooking_time} minutes or less."
    
    response = model.generate_content(prompt)
    st.write(response.text)
