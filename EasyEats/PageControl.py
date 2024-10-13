import streamlit as st

# Initialize session state
if 'page' not in st.session_state:
    st.session_state.page = "login_page"

# Routing logic
if st.session_state.page == "login_page":
    import Log_In  # Import the main page module
    Log_In.main()  # Call its main function
elif st.session_state.page == "other_page":
    import RecipeGenerator  # Import the other page module
    RecipeGenerator.main()  # Call its main function
