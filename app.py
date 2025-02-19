# Imports
import streamlit as st
import pandas as pd
import os 
from io import BytesIO


st.set_page_config(page_title="Data sweeper", layout='wide')
st.markdown(
    """
   <style>
  @import url('https://fonts.googleapis.com/css2?family=Aclonica&display=swap');

    html, body {
        font-family: "Aclonica", serif;
        height: 100%;
        margin: 0;
        padding: 0;
    }
    .main {
        background-color: #2c2c2c; 
        min-height: 100vh;
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
    }
    .block-container {
        padding: 3rem 2rem;
        border-radius: 12px;
        background-color: #3b3b3b; 
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.3);
        margin: 2rem;
        width: 90%;
        max-width: 1200px;
    }
    /* Headings  */
    h1, h2, h3, h4, h5, h6 {
        color: #b39ddb; 
    }
   
    p, span, li, a, div {
        color: #ffffff;
    }
    /* Button styles  */
    .stButton>button {
        border: none;
        border-radius: 8px;
        background-color: #FF5F1F;
        color: white;
        padding: 0.75rem 1.5rem;
        font-size: 1rem;
        box-shadow: 0 4px 10px rgba(0, 0, 0, 0.4);
        transition: background-color 0.3s ease;
    }
    .stButton>button:hover {
        background-color: #FF5733;
        cursor: pointer;
    }
    /* Data tables and frames  */
    .stDataFrame, .stTable {
        border-radius: 10px;
        overflow: hidden;
        background-color: #424242;
        color: white;
    }
    
    .css-1aumxhk, .css-18e3th9 {
        text-align: left;
        color: white;
    }
    /* Radio and checkbox labels */
    .stRadio>label,
    .stCheckbox>label {
        font-weight: bold;
        color: white;
    }

     div[data-baseweb="radio"] input[type="radio"] {
        accent-color: #7e57c2; 
    }
    div[data-baseweb="checkbox"] input[type="checkbox"] {
        accent-color: #7e57c2; 
    }
    /* Download button styling */
    .stDownloadButton>button {
        background-color: #7e57c2;
        color: white;
        border: none;
        border-radius: 8px;
        padding: 0.75rem 1.5rem;
        transition: background-color 0.3s ease;
    }
    .stDownloadButton>button:hover {
        background-color: #6a45a1;
    }
</style>

    """,
    unsafe_allow_html=True  
)
st.title("Data sweeper")
st.write("Transform your files between CSV and Excel formats with built-in data cleaning and visualization!")

uploaded_files = st.file_uploader("Upload your files (CSV or Excel):", type=["csv","xlsx"],
accept_multiple_files=True)

if uploaded_files:
    for file in uploaded_files:
        file_ext = os.path.splitext(file.name) [-1].lower()

        if file_ext == ".csv":
            df = pd.read_csv(file)
        elif file_ext == ".xlsx":
            df = pd.read_excel(file)
        else:
            st.error(f"Unsupported file type: {file_ext}")
            continue

        #Display info about the file
        st.write(f"**File Name:** {file.name}")
        st.write(f"**File Size:** {file.size/1024}")

        #Show 5 rows of our df
        st.write("Preview the Head of the Dataframe")
        st.dataframe(df.head())

        #Options for data cleaning
        st.subheader("Data Cleaning Options")
        if st.checkbox(f"Clean Data for {file.name}"):
            col1,col2 = st.columns(2)


            with col1:
                if st.button(f"Remove Duplicates from {file.name}"):
                    df.drop_duplicates(inplace=True)
                    st.write("Duplicates Removed!")

            with col2:
                if st.button(f"Fill Missing values for {file.name}"):
                    numeric_cols = df.select_dtypes(include=['number']).columns
                    df[numeric_cols] = df[numeric_cols].fillna(df[numeric_cols].mean())
                    st.write("Missing Values have been Filled!")

        st.subheader("Select Columns to Convert")
        columns = st.multiselect(f"Choose Columns for {file.name}",df.columns,default=df.columns)
        df = df[columns]

        st.subheader("Data Visualization")
        if st.checkbox(f"Show Visualization for {file.name}"):
            st.bar_chart(df.select_dtypes(include='number').iloc[:,:2])

        st.subheader("Conversion Options")
        conversion_type= st.radio(f"Convert {file.name} to:" , ["CSV","Excel"] , key=file.name)
        if st.button(f"Convert {file.name}"):
            buffer = BytesIO()
            if conversion_type == "CSV":
                df.to_csv(buffer,index=False)
                file_name=file.name.replace(file_ext,".csv")
                mime_type="text/csv"

            elif conversion_type == "Excel":
                df.to_excel(buffer,index=False,engine='openpyxl')
                file_name = file.name.replace(file_ext,".xlsx")
                mime_type = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            buffer.seek(0)


            st.download_button(
                label=f"Download {file.name} as {conversion_type}",
                data=buffer,
                file_name=file_name,
                mime=mime_type
            )
    
st.success("All files processed!")