import streamlit as st
import mysql.connector
from mysql.connector import Error
import hashlib

# Database connection
def create_connection():
    connection = None
    try:
        connection = mysql.connector.connect(
            host="192.168.1.100",
            user="root",
            password="Illiana",
            database="food_recipes_db"
        )
    except Error as e:
        st.error(f"Error: '{e}'")
    return connection

# Hashing passwords for security
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# User sign-up function
def sign_up(username, password):
    connection = create_connection()
    if connection is not None:
        try:
            cursor = connection.cursor()
            hashed_password = hash_password(password)
            cursor.execute("INSERT INTO users (username, password) VALUES (%s, %s)", (username, hashed_password))
            connection.commit()
            st.success("User signed up successfully!")
        except Error as e:
            st.error(f"Error: '{e}'")
        finally:
            cursor.close()
            connection.close()

# User login function
def login(username, password):
    connection = create_connection()
    if connection is not None:
        try:
            cursor = connection.cursor()
            hashed_password = hash_password(password)
            cursor.execute("SELECT * FROM users WHERE username = %s AND password = %s", (username, hashed_password))
            user = cursor.fetchone()
            if user:
                return True
            else:
                return False
        except Error as e:
            st.error(f"Error: '{e}'")
        finally:
            cursor.close()
            connection.close()
    return False

# Save favorite recipe
def save_favorite_recipe(username, recipe):
    connection = create_connection()
    if connection is not None:
        try:
            cursor = connection.cursor()
            cursor.execute("UPDATE users SET favorite_recipes = %s WHERE username = %s", (recipe, username))
            connection.commit()
            st.success("Recipe saved to favorites!")
        except Error as e:
            st.error(f"Error: '{e}'")
        finally:
            cursor.close()
            connection.close()

# Streamlit app
st.title('Easy Eats')

menu = ["Login", "Sign Up"]
choice = st.sidebar.selectbox("Menu", menu)

if choice == "Sign Up":
    st.subheader("Create a New Account")
    new_user = st.text_input("Username")
    new_password = st.text_input("Password", type="password")
    if st.button("Sign Up"):
        sign_up(new_user, new_password)

elif choice == "Login":
    st.subheader("Login")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    if st.button("Login"):
        if login(username, password):
            st.success(f"Welcome {username}")

            # Show the recipe functionality only if logged in
            ingredients = st.text_input("Enter ingredients you have (comma separated):")
            def get_recipes(ingredients):
                app_id = "29d395d3"
                app_key = "81d1f11d53570c150a29393dd774cf4e"
                ingredients_query = ','.join([ing.strip() for ing in ingredients.split(',')])
                url = f"https://api.edamam.com/api/recipes/v2?type=public&q={ingredients_query}&app_id={app_id}&app_key={app_key}"
                response = requests.get(url)
                exact_matches = []
                partial_matches = []
                if response.status_code == 200:
                    recipes = response.json().get('hits', [])
                    for recipe in recipes:
                        recipe_ingredients = set([ingredient['food'] for ingredient in recipe['recipe']['ingredients']])
                        user_ingredients_set = set(ingredients_query.split(','))
                        if recipe_ingredients == user_ingredients_set:
                            exact_matches.append(recipe['recipe'])
                        elif user_ingredients_set.issubset(recipe_ingredients):
                            missing_ingredients = recipe_ingredients - user_ingredients_set
                            partial_matches.append((recipe['recipe'], missing_ingredients))
                    return exact_matches, partial_matches
                else:
                    return [], []

            if st.button('Find Recipes'):
                if ingredients:
                    exact_recipes, possible_recipes = get_recipes(ingredients)
                    if exact_recipes:
                        st.subheader("Recipes you can make with your ingredients:")
                        for recipe in exact_recipes:
                            st.write(f"**{recipe['label']}**")
                            st.markdown(f"[Recipe Link]({recipe['url']})")
                    else:
                        st.write("No exact recipes found that match your ingredients.")
                    
                    if possible_recipes:
                        st.subheader("Possible recipes if you get a few more ingredients:")
                        for recipe, missing in possible_recipes:
                            st.write(f"**{recipe['label']}** - Missing ingredients: {', '.join(missing)}")
                            st.markdown(f"[Recipe Link]({recipe['url']})")
                    else:
                        st.write("No possible recipes found with a few more ingredients.")

                else:
                    st.write("Please enter some ingredients to find recipes.")

            # Save favorite recipe
            favorite_recipe = st.text_input("Enter your favorite recipe URL to save:")
            if st.button("Save Favorite Recipe"):
                save_favorite_recipe(username, favorite_recipe)

        else:
            st.error("Incorrect username or password")
