import streamlit as st
import requests
import os
import zipfile
import base64

def main():
    destination_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'static', 'filtered_images')

    st.title("Object Detection Image Filter")

    col1, col2 = st.columns(2)
    with col1:
        st.image('static/header.png', caption="Image Validation", width=250)
        with col2:
            st.image('static/labels.png', caption="Class Labels", width=250)

    num_list = [ '1', '10', '100', '104', '105', '106', '11', '112', '113', '115', ]
    
    rider_number = st.text_input("Enter a rider number, 0-999.")
    class_name = None
    
    if rider_number:
        try:
            class_name = int(rider_number)
        except ValueError:
            st.write("Please enter a valid number.")
    
    if class_name in num_list:
        try:
            # Find the position of the class_name in the list
            position = num_list.index(str(class_name)) + 1
            st.success(f"The number {class_name} is at position {position} in the list.")
        except ValueError:
            st.error(f"The number {class_name} is not in the list.")
            return
    
    # Input for source folder path
    folder_path = st.text_input("Enter the path to the source folder:")

    if st.button("Filter and Copy Images"):
        if class_name is None:
            st.write("Please enter a valid rider number.")
            return

        data = {'class_name': class_name, 'folder_path': folder_path}
        response = requests.post('http://127.0.0.1:5000/detect_and_filter', json=data)

        if response.ok:
            filtered_images = response.json()['filtered_images']

            st.write("Filtered images copied to 'filtered_images' folder:")
            for image in filtered_images:
                st.image(image, caption=image, use_column_width=True)

            # Create and display download link for the zip file
            zip_filename = response.json()['zip_filename']
            b64_zip_data = base64.b64encode(open(os.path.join(destination_dir, zip_filename), 'rb').read()).decode()
            download_link = f'<a href="data:application/zip;base64,{b64_zip_data}" download="{zip_filename}">Download Filtered Images</a>'
            st.markdown(download_link, unsafe_allow_html=True)

        else:
            st.write("Error processing images")

if __name__ == "__main__":
    main()
st.subheader('This is :green[_working_]. :blue[24/08/2023].     :violet[yandle] :hearts:')
st.subheader('Happy Father\'s Day, :blue[3/09/2023].')
