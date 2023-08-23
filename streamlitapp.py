import streamlit as st
import requests
import os
import zipfile
import base64

def main():
    st.title("Image Filter, Copy, and Download")
    rider_number = st.text_input("Enter a rider number, 0-999")
    if rider_number:
        try:
            class_name = int(rider_number)
        except ValueError:
            st.write("Please enter a number.")
    folder_path = st.text_input("Enter the path to the source folder:")           

    if st.button("Filter and Copy Images"):
        data = {'class_name': class_name, 'folder_path': folder_path}
        response = requests.post('http://127.0.0.1:5000/detect_and_filter', json=data)

        if response.ok:
            filtered_images = response.json()['filtered_images']
            st.write("Filtered images copied to 'filtered_images' folder:")
            for image in filtered_images:
                st.image(image, caption=image, use_column_width=True)
                
            zip_filename = response.json()['zip_filename']
            b64_zip_data = base64.b64encode(open(zip_filename, 'rb').read()).decode()
            download_link = f'<a href="data:application/zip;base64,{b64_zip_data}" download="{zip_filename}">Download Filtered Images</a>'
            st.markdown(download_link, unsafe_allow_html=True)
        else:
            st.write("Error processing images")
if __name__ == "__main__":
    main()
    
def main():
    num_list = [ ]                     #Define the number list
    st.subheader("Number Position Finder")
    search_number = st.text_input("Enter the number you want to search for:")                # Get the number to search for
    if st.button("Find Position"):
        try:
            position = num_list.index(search_number) + 1
            st.success(f"The number {search_number} is at position {position} in the list.")
        except ValueError:
            st.error(f"The number {search_number} is not in the list.")
if __name__ == "__main__":
    main()
