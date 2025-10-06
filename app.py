import streamlit as st
import pandas as pd
from ydata_profiling import ProfileReport
import seaborn as sns
import io

st.set_page_config(page_title="YData Profiling App by Muhammad Umar", layout="wide")
st.title("YData Profiling App by Muhammad Umar")

st.markdown("""
Upload your CSV or Excel file to generate a profiling report, or select a sample dataset below.
""")

# Sample datasets
sample_datasets = {
    "Diamonds": sns.load_dataset("diamonds"),
    "Titanic": sns.load_dataset("titanic"),
    "Iris": sns.load_dataset("iris"),
}

sample_choice = st.selectbox("Or choose a sample dataset:", ["None"] + list(sample_datasets.keys()))

uploaded_file = st.file_uploader("Drag and drop your data file here (CSV or Excel)", type=["csv", "xlsx"])

df = None

if uploaded_file is not None:
    try:
        if uploaded_file.name.endswith('.csv'):
            df = pd.read_csv(uploaded_file)
        else:
            df = pd.read_excel(uploaded_file)
        st.success("File uploaded successfully!")
    except Exception as e:
        st.error(f"Error loading file: {e}")
elif sample_choice != "None":
    df = sample_datasets[sample_choice]
    st.info(f"Loaded sample dataset: {sample_choice}")

if df is not None:
    st.subheader("Data Preview")
    st.dataframe(df.head())

    st.subheader("YData Profiling Report")
    profile = ProfileReport(df, title="YData Profiling Report", explorative=True)
    # Render the report in Streamlit
    profile_html = profile.to_html()
    st.components.v1.html(profile_html, height=1200, scrolling=True)
else:
    st.info("Please upload a file or select a sample dataset to see the profiling report.")