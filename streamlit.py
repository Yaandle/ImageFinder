import streamlit as st
import requests
import os

gcp_url = ''    #Define URL

st.title("Bike Number Detector")
st.header("Enter Bike Number")
Bike_Number = st.text_input("Enter Bike Number")

if st.button("Submit"):
    if Bike_Number:
        st.write(f"You entered bike number: {Bike_Number}")
        webhook_url = gcp_url + '/webhook'                      
        data = {"Bike_Number": Bike_Number}
        response = requests.post(webhook_url, json=data)
        if response.status_code == 200:
            st.success("Bike number sent to Flask webhook successfully.")
        else:
            st.error("Failed to send bike number to Flask webhook.")
    else:
        st.write("Please enter a bike number.")
