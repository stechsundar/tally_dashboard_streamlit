import streamlit as st
import pandas as pd

# --- PAGE SETUP  ----
st.set_page_config(page_title="Sales Dashboard", page_icon="🎢")
st.title("Sales Dashboard")

url = "https://raw.githubusercontent.com/stechsundar/tally_dashboard/refs/heads/main/sales.csv"


# --- LOAD DATA ---
@st.cache_data
def load_data(url):
    # Load the data with the correct encoding
    data = pd.read_csv(url, delimiter=',', encoding='utf-16', on_bad_lines='skip')

    # Strip leading/trailing spaces and standardize column names
    data.columns = data.columns.str.strip()
    # Convert 'Date' from string to datetime
    data['Date'] = pd.to_datetime(data['Date'].astype(str), format='%Y%m%d')

    # Extract month and year from 'Date'
    data["month"] = data["Date"].dt.month  # Extracts the month as a number
    data["year"] = data["Date"].dt.year  # Extracts the year

    # Convert 'Date' column to 'dd-mm-yyyy' format
    data['Date'] = data['Date'].dt.strftime('%d-%m-%Y')

    return data


# Load the raw data
data = load_data(url)

# Display the data in Streamlit
st.dataframe(data)
