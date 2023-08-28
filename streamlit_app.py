import streamlit as st
import requests
import os
import zipfile
import base64

def main():
    st.title("Object Detection Image Filter")

    col1, col2 = st.columns(2)
    with col1:
        st.image('./header.png', caption="Image Validation", width=250)
        with col2:
            st.image('./labels.png', caption="Class Labels", width=250)



    num_list = [
        '1', '10', '100', '104', '105', '106', '11', '112', '113', '115',
        '118', '12', '123', '128', '13', '132', '137', '14', '147', '15',
        '150', '151', '159', '16', '160', '162', '166', '17', '171', '172',
        '174', '178', '18', '180', '182', '189', '199', '2', '20', '202',
        '21', '210', '211', '215', '217', '22', '222', '226', '23', '235',
        '24', '25', '26', '266', '27', '273', '275', '277', '28', '286',
        '29', '291', '299', '3', '30', '31', '310', '313', '32', '323',
        '33', '340', '346', '348', '355', '36', '37', '376', '38', '39',
        '392', '4', '40', '404', '411', '414', '42', '421', '427', '428',
        '43', '44', '46', '47', '48', '5', '50', '51', '518', '521', '53',
        '549', '55', '57', '585', '59', '6', '609', '61', '616', '62', '65',
        '666', '7', '710', '72', '724', '74', '77', '79', '8', '80', '81',
        '818', '826', '85', '852', '88', '89', '893', '9', '915', '916',
        '952', '96', '97', '972', '99', '999'
    ]
    
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
            b64_zip_data = base64.b64encode(open(zip_filename, 'rb').read()).decode()
            download_link = f'<a href="data:application/zip;base64,{b64_zip_data}" download="{zip_filename}">Download Filtered Images</a>'
            st.markdown(download_link, unsafe_allow_html=True)

        else:
            st.write("Error processing images")

if __name__ == "__main__":
    main()


st.subheader('This is :green[_working_]. :blue[24/08/2023].     :violet[yandle] :hearts:')