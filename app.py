from PIL import Image
import os, pandas as pd, google.generativeai as gem, csv, ast, streamlit as st
from langchain_core.messages import HumanMessage
from langchain_google_genai import ChatGoogleGenerativeAI

os.environ["GOOGLE_API_KEY"] = 'AIzaSyBbepUh8x3CqpkxNFnJ1IX0dFc0UNTwwbU'
# Configuration
IMAGE_FOLDER = "uploaded_images"
os.makedirs(IMAGE_FOLDER, exist_ok=True)

# Initialize Google Generative AI
llm = ChatGoogleGenerativeAI(model="gemini-pro-vision")

# Streamlit UI
st.markdown(f"<h2 style='color:blue; text-align: center;'>{'Business Card Extractor'}</h2>",unsafe_allow_html = True)
st.markdown("""<style>.stButton > button {display: block;margin: 0 auto;}</style>""", unsafe_allow_html=True)

# # Check if the CSV file exists
# csv_filename = "business_cards.csv"
# csv_exists = os.path.exists(csv_filename)

# # 1. Option to upload images
# uploaded_files = st.file_uploader("Upload Images", accept_multiple_files=True, type=["jpg", "jpeg", "png"])
# if uploaded_files:
#     for uploaded_file in uploaded_files:
#         with open(os.path.join(IMAGE_FOLDER, uploaded_file.name), "wb") as f:
#             f.write(uploaded_file.getbuffer())
#     st.success("Images uploaded successfully!")

#     # Display uploaded images in a grid
#     image_paths = [os.path.join(IMAGE_FOLDER, uploaded_file.name) for uploaded_file in uploaded_files]
#     if image_paths:
#         num_cols = 5  # Number of columns for grid layout
#         cols = st.columns(num_cols)
#         for i, image_path in enumerate(image_paths):
#             with cols[i % num_cols]:
#                 image = Image.open(image_path)
#                 st.image(image, caption=os.path.basename(image_path))

# # 2. Option to choose images from an existing folder
# existing_images = [f for f in os.listdir(IMAGE_FOLDER) if os.path.isfile(os.path.join(IMAGE_FOLDER, f))]
# selected_images = st.multiselect("Select Images from Existing Folder", existing_images)

# # Display selected images in a grid
# if selected_images:
#     image_paths = [os.path.join(IMAGE_FOLDER, image_file) for image_file in selected_images]
#     if image_paths:
#         num_cols = 5  # Number of columns for grid layout
#         cols = st.columns(num_cols)
#         for i, image_path in enumerate(image_paths):
#             with cols[i % num_cols]:
#                 image = Image.open(image_path)
#                 st.image(image, caption=os.path.basename(image_path))
                
# # Create columns for placing checkboxes
# col1, col2 = st.columns([1, 4])

# # Place the first checkbox (CSV) in the first column
# with col1:
#     display_csv = st.checkbox("View CSV", value=csv_exists, help="Check to display CSV data")
# # Place the second checkbox (JSON) in the second column
# with col2:
#     display_json = st.checkbox("View JSON", key="display_json", help="Check to display JSON data extracted")

# # Apply custom CSS to move the checkboxes downwards
# st.markdown(
#     """
#     <style>
#     .stCheckbox {
#         display: flex;
#         justify-content: flex-end;
#         margin-top: 20px; /* Adjust the margin-top value as needed */
#     }
#     </style>
#     """,
#     unsafe_allow_html=True)

# # 3. Option to clean the existing images in the folder/clean selected images from the existing folder
# if st.button("Clean All Images"):
#     for f in existing_images:
#         os.remove(os.path.join(IMAGE_FOLDER, f))
#     st.info("All images cleaned successfully!")

# if st.button("Clean Selected Images"):
#     for f in selected_images:
#         os.remove(os.path.join(IMAGE_FOLDER, f))
#     st.info("Selected image(s) cleaned successfully!")

# # Process selected images
# if st.button("Process Selected Images") and selected_images:
#     all_rows = []

#     for image_file in selected_images:
#         image_path = os.path.join(IMAGE_FOLDER, image_file)

#         message = HumanMessage(
#             content=[
#                 {
#                     "type": "text",
#                     "text": """Carefully analyze the business card(s) and get the output in pure json format

#                     [{"Person name": "full name of the person if exists",
#                         "Company name": "get the full company name if exists",
#                         "Email": "get the complete mail if exists",
#                         "Contact number": "get every contact numbers if exists"}]
#                         your response shall not contain ' ```json ' and ' ``` ' """,
#                 },
#                 {"type": "image_url", "image_url": image_path}
#             ]
#         )

#         response = llm.invoke([message])
#         extracted_data = ast.literal_eval(response.content)

#         columns = ["Person name", "Company name", "Email", "Contact number"]

#         rows = []
#         for item in extracted_data:
#             row = {col: item.get(col, "") for col in columns}
#             rows.append(row)
#         all_rows.extend(rows)

#     df = pd.DataFrame(all_rows, columns=columns)

#     # Load existing CSV if it exists and append new data
#     if csv_exists:
#         existing_df = pd.read_csv(csv_filename)
#         df = pd.concat([existing_df, df], ignore_index=True)

#     # Save the DataFrame back to the CSV file
#     df.to_csv(csv_filename, index=False)
#     st.success(f"CSV file '{csv_filename}' updated successfully!")

#     # Show extracted data in JSON format if the switch is on
#     if display_json:
#       with st.expander(f"Show JSON - {image_file}"):
#         st.json(extracted_data)

# # Display the DataFrame if the checkbox is checked
# if display_csv and csv_exists:
#     df = pd.read_csv(csv_filename)
#     st.markdown('##### Verify Data')
#     edited_df = st.data_editor(df, num_rows="dynamic", key="editor_displayed")

#     # Save the edited DataFrame back to the CSV file
#     edited_df.to_csv(csv_filename, index=False)
#     st.markdown('##### Final Data')
#     st.write(edited_df)

# st.stop()


# Check if the CSV file exists
csv_filename = "business_cards.csv"
csv_exists = os.path.exists(csv_filename)

# 1. Option to upload images
uploaded_files = st.file_uploader("Upload Images", accept_multiple_files=True, type=["jpg", "jpeg", "png"])
if uploaded_files:
    for uploaded_file in uploaded_files:
        with open(os.path.join(IMAGE_FOLDER, uploaded_file.name), "wb") as f:
            f.write(uploaded_file.getbuffer())
    st.success("Images uploaded successfully!")

    # Display uploaded images in a grid
    image_paths = [os.path.join(IMAGE_FOLDER, uploaded_file.name) for uploaded_file in uploaded_files]
    if image_paths:
        num_cols = 5  # Number of columns for grid layout
        cols = st.columns(num_cols)
        for i, image_path in enumerate(image_paths):
            with cols[i % num_cols]:
                image = Image.open(image_path)
                st.image(image, caption=os.path.basename(image_path))

# 2. Option to choose images from an existing folder
existing_images = [f for f in os.listdir(IMAGE_FOLDER) if os.path.isfile(os.path.join(IMAGE_FOLDER, f))]
selected_images = st.multiselect("Select Images from Existing Folder", existing_images)

# Display selected images in a grid
if selected_images:
    image_paths = [os.path.join(IMAGE_FOLDER, image_file) for image_file in selected_images]
    if image_paths:
        num_cols = 5  # Number of columns for grid layout
        cols = st.columns(num_cols)
        for i, image_path in enumerate(image_paths):
            with cols[i % num_cols]:
                image = Image.open(image_path)
                st.image(image, caption=os.path.basename(image_path))
                
# Create columns for placing checkboxes
col1, col2 = st.columns([1, 4])

# Place the first checkbox (CSV) in the first column
with col1:
    display_csv = st.checkbox("View CSV", value=csv_exists, help="Check to display CSV data")
# Place the second checkbox (JSON) in the second column
with col2:
    display_json = st.checkbox("View JSON", key="display_json", help="Check to display JSON data extracted")

# Apply custom CSS to move the checkboxes downwards
st.markdown(
    """
    <style>
    .stCheckbox {
        display: flex;
        justify-content: flex-end;
        margin-top: 20px; /* Adjust the margin-top value as needed */
    }
    </style>
    """,
    unsafe_allow_html=True)

# 3. Option to clean the existing images in the folder/clean selected images from the existing folder
if st.button("Clean All Images"):
    for f in existing_images:
        os.remove(os.path.join(IMAGE_FOLDER, f))
    st.success("All images cleaned successfully!")

if st.button("Clean Selected Images"):
    for f in selected_images:
        os.remove(os.path.join(IMAGE_FOLDER, f))
    st.success("Selected images cleaned successfully!")

# Process selected images
if st.button("Process Selected Images") and selected_images:
    all_rows = []

    for image_file in selected_images:
        image_path = os.path.join(IMAGE_FOLDER, image_file)

        message = HumanMessage(
            content=[
                {
                    "type": "text",
                    "text": """Carefully analyze the business card(s) and get the output in pure json format

                    [{"Person name": "full name of the person if exists",
                        "Company name": "get the full company name if exists",
                        "Email": "get the complete mail if exists",
                        "Contact number": "get every contact numbers if exists"}]
                        your response shall not contain ' ```json ' and ' ``` ' """,
                },
                {"type": "image_url", "image_url": image_path}
            ]
        )

        response = llm.invoke([message])
        extracted_data = ast.literal_eval(response.content)

        columns = ["Person name", "Company name", "Email", "Contact number"]

        rows = []
        for item in extracted_data:
            row = {col: item.get(col, "") for col in columns}
            rows.append(row)
        all_rows.extend(rows)

        # Show extracted data in JSON format if the switch is on
        if display_json:
            with st.expander(f"Show JSON - {image_file}"):
                st.json(extracted_data)

    df = pd.DataFrame(all_rows, columns=columns)

    # Load existing CSV if it exists and append new data
    if csv_exists:
        existing_df = pd.read_csv(csv_filename)
        df = pd.concat([existing_df, df], ignore_index=True)

    # Save the DataFrame back to the CSV file
    df.to_csv(csv_filename, index=False)
    st.success(f"CSV file '{csv_filename}' updated successfully!")

# Display the DataFrame if the checkbox is checked
if display_csv and csv_exists:
    df = pd.read_csv(csv_filename)
    st.markdown('##### Verify Data📝')
    edited_df = st.data_editor(df, num_rows="dynamic", key="editor_displayed")

    # Save the edited DataFrame back to the CSV file
    edited_df.to_csv(csv_filename, index=False)
    st.markdown('##### Final Data')
    st.write(edited_df)

st.stop()
