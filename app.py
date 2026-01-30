import streamlit as st
import pandas as pd
from sanitizer import sanitize_data

st.set_page_config(
    page_title="Excel Data Sanitisation Tool",
    layout="wide"
)

st.title("🧹 Excel Data Sanitisation Tool")

st.markdown("""
Upload:
- **Excel data file**
- **Excel range definition file**

Rows with values outside the allowed range will be marked as **bad data**.
""")

data_file = st.file_uploader(
    "Upload Data Excel File",
    type=["xlsx"]
)

range_file = st.file_uploader(
    "Upload Range Excel File",
    type=["xlsx"]
)

if data_file and range_file:
    data = pd.read_excel(data_file)
    ranges = pd.read_excel(range_file)

    st.subheader("📊 Uploaded Data")
    st.dataframe(data)

    st.subheader("📏 Parameter Ranges")
    st.dataframe(ranges)

    if st.button("Run Data Sanitisation"):
        clean_data, bad_data = sanitize_data(data, ranges)

        st.subheader("✅ Clean Data (Safe for Deployment)")
        st.dataframe(clean_data)

        st.subheader("❌ Bad Data (Out of Range / Invalid)")
        st.dataframe(bad_data)

        st.download_button(
            "Download Clean Data (Excel)",
            clean_data.to_excel(index=False),
            file_name="clean_data.xlsx"
        )

        st.download_button(
            "Download Bad Data Report (Excel)",
            bad_data.to_excel(index=False),
            file_name="bad_data.xlsx"
        )
