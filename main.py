import streamlit as st
import pandas as pd

# --- PAGE SETUP  ----
st.set_page_config(page_title="Sales Dashboard", page_icon="🎢")
st.title("Sales Dashboard")

# --- HIDE STREAMLIT BRANDING ---
hide_st_style = """
    <style>
    #MainMenu { visibility: hidden;}
    header: { visibility: hidden;}
    </style>
"""
st.markdown(hide_st_style, unsafe_allow_html=True)


url = "https://raw.githubusercontent.com/stechsundar/tally_dashboard/refs/heads/main/sales.csv"


# --- LOAD DATA ---
@st.cache_data
def load_data(url):
    data = pd.read_csv(url, delimiter=',', encoding='utf-16', on_bad_lines='skip')

    # Strip leading/trailing spaces from column names to ensure proper names
    data.columns = data.columns.str.strip()

    # Convert Date from 'yyyymmdd' to 'dd-mm-yyyy'
    if 'Date' in data.columns:
        data['Date'] = pd.to_datetime(data['Date'], format='%Y%m%d')

        # Extract Month (as number) and Year from the 'Date' column
        data['Month'] = data['Date'].dt.month  # Extracts the month as a number
        data['Year'] = data['Date'].dt.year  # Extracts the year

        # Convert the 'Date' column back to 'dd-mm-yyyy' format
        data['Date'] = data['Date'].dt.strftime('%d-%m-%Y')

    else:
        st.error("The 'Date' column was not found. Please check the dataset.")

    # Remove commas from 'InvoiceNo' and 'Amount' columns (if they exist)
    data['InvoiceNo'] = data['InvoiceNo'].astype(str).str.replace(',', '')
    data['Rate'] = data['Rate'].astype(str).str.replace(',', '')
    data['Rate'] = data['Rate'].astype(float)  # Convert to float for proper formatting
    data['Rate'] = data['Rate'].round(2)  # Format to 2 decimal places

    # Convert and format the 'Amount' column
    data['Amount'] = data['Amount'].astype(float)  # Convert to float for proper formatting
    data['Amount'] = data['Amount'].round(2)  # Format to 2 decimal places

    return data


# Load the raw data (cached)
data = load_data(url)
st.dataframe(data)

"""
item_revenues = (
    data.groupby(["Item", "Year"])["Amount"]
    .sum()
    .unstack()
    .assign(changes=lambda x: x.pct_changes(axis=1)[2024] * 100)
)
st.dataframe(item_revenues)

# Apply styling separately
styled_data = data.style.format({'Amount': '{:,.2f}', 'Rate': '{:,.2f}'})  # This formats the Amount with commas and 2 decimal places
styled_data = styled_data.hide(axis="index")  # Hide the index column to keep the table neat

# Display the styled dataframe in Streamlit
st.dataframe(styled_data)
"""