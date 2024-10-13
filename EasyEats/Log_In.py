import streamlit as st

st.title('My Multi-Page Streamlit App')
st.write('Select a page above to navigate through the app.')

import streamlit as st
import pandas as pd
import os

# Define the CSV file
CSV_FILE = 'users.csv'

# Function to create the users CSV file if it doesn't exist
def create_user_file():
    if not os.path.exists(CSV_FILE):
        with open(CSV_FILE, 'w') as f:
            f.write('username,password\n')  # Create header

# Function to register a new user
# Function to register a new user
def register_user(username, password):
    # Read existing users
    df = pd.read_csv(CSV_FILE)
    
    # Check if the username already exists
    if username in df['username'].values:
        st.error("Username already exists. Please choose another.")
    else:
        # Create a new DataFrame for the new user
        new_user = pd.DataFrame({'username': [username], 'password': [password]})
        
        # Concatenate the new user DataFrame with the existing one
        df = pd.concat([df, new_user], ignore_index=True)
        df.to_csv(CSV_FILE, index=False)  # Save to CSV
        st.success("Account created successfully!")

# Function to verify user credentials
def verify_user(username, password):
    df = pd.read_csv(CSV_FILE)
    if username in df['username'].values:
        if df[df['username'] == username]['password'].values[0] == password:
            return True
    return False

# Main application
def main():
    create_user_file()  # Ensure the CSV file exists
    
    st.title("CSV Login System")

    # Login form
    st.subheader("Login")
    login_username = st.text_input("Username")
    login_password = st.text_input("Password", type="password")
    
    if st.button("Login"):
        if verify_user(login_username, login_password):
            st.success("Logged in successfully!")
            st.session_state.page = "other_page"
            return



        else:
            st.error("Invalid username or password.")

    # Registration form
    st.subheader("Create Account")
    register_username = st.text_input("Username (for registration)")
    register_password = st.text_input("Password (for registration)", type="password")
    
    if st.button("Sign Up"):
        register_user(register_username, register_password)

if __name__ == "__main__":
    main()
