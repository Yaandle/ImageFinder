import streamlit as st
import requests

# Set a title
st.title("Bike Number Detector")

# Add a header
st.header("Enter Bike Number")

# Create an input field for bike number
bike_number = st.text_input("Enter Bike Number")

# You can use the 'bike_number' variable to access the user's input
if st.button("Submit"):
    if bike_number:
        st.write(f"You entered bike number: {bike_number}")

        # Send the bike number to the Flask webhook
        webhook_url = "http://127.0.0.1:5000/webhook"
        data = {'bike_number': bike_number}

        response = requests.post(webhook_url, json=data)

        if response.status_code == 200:
            st.success("Bike number sent to Flask webhook successfully.")
        else:
            st.error("Failed to send bike number to Flask webhook.")
    else:
        st.write("Please enter a bike number.")
