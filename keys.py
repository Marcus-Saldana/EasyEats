import mysql.connector
from mysql.connector import Error
import streamlit as st

# Database connection function
def create_connection():
    connection = None
    try:
        connection = mysql.connector.connect(
            host='localhost',  # or your MySQL server IP
            user='your_username',
            password='your_password',
            database='your_database'
        )
        print("Connection to MySQL DB successful")
    except Error as e:
        print(f"The error '{e}' occurred")
    return connection

# User Signup function
def signup(username, password):
    conn = create_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO users (username, password) VALUES (%s, %s)", (username, password))
        conn.commit()
        st.success("User registered successfully!")
    except Error as e:
        st.error(f"The error '{e}' occurred")
    finally:
        cursor.close()
        conn.close()

# User Login function
def login(username, password):
    conn = create_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT * FROM users WHERE username = %s AND password = %s", (username, password))
        result = cursor.fetchone()
        if result:
            st.success("Login successful!")
            return True
        else:
            st.error("Invalid username or password.")
            return False
    except Error as e:
        st.error(f"The error '{e}' occurred")
    finally:
        cursor.close()
        conn.close()

# Streamlit UI
st.title("Food Recipe App")

menu = st.sidebar.selectbox("Menu", ["Signup", "Login"])

if menu == "Signup":
    username = st.text_input("Username")
    password = st.text_input("Password", type='password')
    if st.button("Sign Up"):
        signup(username, password)

elif menu == "Login":
    username = st.text_input("Username")
    password = st.text_input("Password", type='password')
    if st.button("Login"):
        login(username, password)
