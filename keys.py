import streamlit as st
import mysql.connector
import hashlib

# MySQL connection
def create_connection():
    connection = None
    try:
        connection = mysql.connector.connect(
            host="192.168.1.100",
            user="root",
            password="Illiana",
            database="food_recipes_db"
        )
    except mysql.connector.Error as e:
        st.error(f"Error: '{e}'")
    return connection

# Hash passwords for security
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# Signup functionality
def sign_up(username, password):
    connection = create_connection()
    if connection:
        try:
            cursor = connection.cursor()
            hashed_password = hash_password(password)
            query = "INSERT INTO users (username, password) VALUES (%s, %s)"
            cursor.execute(query, (username, hashed_password))
            connection.commit()
            st.success("User signed up successfully!")
        except mysql.connector.Error as e:
            st.error(f"Error: '{e}'")
        finally:
            cursor.close()
            connection.close()

# Login functionality
def login(username, password):
    connection = create_connection()
    if connection:
        try:
            cursor = connection.cursor()
            hashed_password = hash_password(password)
            query = "SELECT * FROM users WHERE username = %s AND password = %s"
            cursor.execute(query, (username, hashed_password))
            user = cursor.fetchone()
            if user:
                return True
            else:
                return False
        except mysql.connector.Error as e:
            st.error(f"Error: '{e}'")
        finally:
            cursor.close()
            connection.close()
    return False

# Save favorite recipe
def save_favorite_recipe(username, favorite_recipe):
    connection = create_connection()
    if connection:
        try:
            cursor = connection.cursor()
            query = "UPDATE users SET favorite_recipes = %s WHERE username = %s"
            cursor.execute(query, (favorite_recipe, username))
            connection.commit()
            st.success("Favorite recipe saved!")
        except mysql.connector.Error as e:
            st.error(f"Error: '{e}'")
        finally:
            cursor.close()
            connection.close()

# Streamlit app
st.title('Easy Eats - User Authentication')

menu = ["Login", "Sign Up"]
choice = st.sidebar.selectbox("Menu", menu)

if choice == "Sign Up":
    st.subheader("Create a New Account")
    new_user = st.text_input("Username")
    new_password = st.text_input("Password", type="password")
    if st.button("Sign Up"):
        if new_user and new_password:
            sign_up(new_user, new_password)
        else:
            st.error("Please enter both username and password")

elif choice == "Login":
    st.subheader("Login")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    if st.button("Login"):
        if login(username, password):
            st.success(f"Welcome, {username}!")

            favorite_recipe = st.text_input("Enter your favorite recipe URL to save:")
            if st.button("Save Favorite Recipe"):
                if favorite_recipe:
                    save_favorite_recipe(username, favorite_recipe)
                else:
                    st.error("Please enter a recipe URL")
        else:
            st.error("Incorrect username or password")
