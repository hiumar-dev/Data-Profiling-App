import streamlit as st
import pandas as pd
from ydata_profiling import ProfileReport
import seaborn as sns
import io

st.set_page_config(page_title="YData Profiling App by Muhammad Umar", layout="wide")
st.title(" YData Profiling App by Muhammad Umar")

st.markdown("""
Upload your CSV or Excel file to generate a profiling report, or select a sample dataset below.
You can choose between **Quick Mode (sample)** for faster reports or **Full Mode** for complete analysis.
""")

# Sample datasets
sample_datasets = {
    "Diamonds": sns.load_dataset("diamonds"),
    "Titanic": sns.load_dataset("titanic"),
    "Iris": sns.load_dataset("iris"),
    "Tips": sns.load_dataset("tips"),
}

sample_choice = st.selectbox("Or choose a sample dataset:", ["None"] + list(sample_datasets.keys()))

uploaded_file = st.file_uploader(" Upload your data file (CSV or Excel)", type=["csv", "xlsx"])

df = None

if uploaded_file is not None:
    try:
        if uploaded_file.name.lower().endswith('.csv'):
            df = pd.read_csv(uploaded_file)
        elif uploaded_file.name.lower().endswith('.xlsx'):
            df = pd.read_excel(uploaded_file)
        else:
            st.error("Unsupported file format. Please upload a CSV or Excel file.")
        if df is not None:
            st.success(" File uploaded successfully!")
    except Exception as e:
        st.error(f"Error loading file: {e}")

elif sample_choice != "None":
    df = sample_datasets[sample_choice]
    st.info(f"Loaded sample dataset: **{sample_choice}**")

if df is not None:
    st.subheader(" Data Preview")
    st.dataframe(df.head())

    # Choose profiling mode
    st.markdown("### Profiling Options")
    mode = st.radio("Select profiling mode:", ["Quick (Sample 10K rows)", "Full (Entire dataset)"])

    # Handle large datasets safely
    if mode == "Quick (Sample 10K rows)" and len(df) > 10000:
        st.warning(f"Dataset too large ({len(df)} rows). Sampling 10,000 rows for quick profiling...")
        df = df.sample(10000, random_state=42)
        minimal_mode = True
    elif mode == "Full (Entire dataset)" and len(df) > 100000:
        st.warning(" Large dataset detected! This may cause memory issues. Switching to safe (minimal) mode.")
        minimal_mode = True
    else:
        minimal_mode = (mode == "Quick (Sample 10K rows)")

    st.subheader(" YData Profiling Report")

    try:
        profile = ProfileReport(df, title="YData Profiling Report", explorative=True, minimal=minimal_mode)
        profile_html = profile.to_html()
        st.components.v1.html(profile_html, height=1200, scrolling=True)

        # Add download button
        buffer = io.BytesIO()
        buffer.write(profile_html.encode('utf-8'))
        buffer.seek(0)
        st.download_button(
            label=" Download Profiling Report (HTML)",
            data=buffer,
            file_name="profiling_report.html",
            mime="text/html"
        )

    except Exception as e:
        st.error(f"Error generating profiling report: {e}")

else:
    st.info("Please upload a file or select a sample dataset to see the profiling report.")

st.markdown("""
---
**Note:**  
- *Quick Mode* analyzes up to 10,000 rows (recommended for speed).  
- *Full Mode* runs complete analysis but may take longer for large files.
""")
