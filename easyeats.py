import streamlit as st
import os
from dotenv import load_dotenv
import google.generativeai as genai

# Load environment variables
load_dotenv('codespace.env')

# Retrieve the API key
api_key = os.getenv('GOOGLE_API_KEY')
if api_key is None:
    st.error("API key not found. Please check your .env file.")
else:
    genai.configure(api_key=api_key)

model = genai.GenerativeModel("gemini-1.5-flash")

# User inputs
user_input = st.text_input("Enter the ingredients you would like to use:")
calorie_limit = st.slider("Set your calorie limit:", 100, 1000, 500)  # Min, max, default values
meal_type = st.selectbox("What type of meal are you making?", ("Breakfast", "Lunch", "Dinner", "Snack"))
cuisine_preference = st.selectbox("Do you have a preference for a specific cuisine?", ("No preference", "Italian", "Mexican", "Asian", "American", "French", "Indian", "Middle Eastern"))
dietary_preferences = st.multiselect("Do you have any dietary restrictions or preferences?", ("None", "Vegan", "Gluten-Free", "Keto", "Paleo", "Dairy-Free", "Vegetarian"))
avoid_ingredients = st.text_input("Are there any ingredients you're allergic to or would prefer to avoid?")
cooking_time = st.slider("How much time do you have for cooking?", 5, 120, 30)  # Min 5 mins, Max 120 mins, default 30 mins

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
    # Display the response in the Streamlit app
    st.write(response.text)
