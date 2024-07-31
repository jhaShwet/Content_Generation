import streamlit as st
import requests

st.title("Content Generator")

# Initialize session state variables
if 'content_data' not in st.session_state:
    st.session_state.content_data = {}

# Input for topic
topic = st.text_input("Enter a topic:")

# Button to generate content
if st.button("Generate Content"):
    if topic:
        response = requests.post("http://127.0.0.1:8000/generate/", json={"topic": topic})
        if response.status_code == 200:
            st.session_state.content_data = response.json()
            st.write("Content generated successfully.")
        else:
            st.write("Error:", response.json().get("detail", "Unknown error"))
    else:
        st.write("Please enter a topic.")

# Check if content_data has content before accessing
if 'content' in st.session_state.content_data:
    content = st.session_state.content_data['content']
    st.write("Content:", content)

    # Button to submit content
    if st.button("Submit Content"):
        content_id = st.session_state.content_data['id']
        submit_response = requests.post("http://127.0.0.1:8000/submit/", json={"content_id": content_id})
        if submit_response.status_code == 200:
            st.write("Content submitted successfully.")
            st.session_state.content_data = {}  # Clear the data after submission
        else:
            st.write("Error:", submit_response.json().get("detail", "Unknown error"))
else:
    st.write("No content available. Please generate content first.")
