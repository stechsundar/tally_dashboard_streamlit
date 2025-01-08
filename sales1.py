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


# --- CONFIG ---
YEAR = 2024  # Current year for comparison
url = "https://raw.githubusercontent.com/stechsundar/tally_dashboard/refs/heads/main/sales.csv"

# --- LOAD DATA ---
@st.cache_data
def load_data(url):
    # Load the data with the correct encoding
    data = pd.read_csv(url, delimiter=',', encoding='utf-16', on_bad_lines='skip')

    # Standardize column names
    data.columns = data.columns.str.strip()

    # Convert 'Date' from string to datetime
    data['Date'] = pd.to_datetime(data['Date'].astype(str), format='%Y%m%d')

    # Extract month and year from 'Date'
    data["month"] = data["Date"].dt.month
    data["year"] = data["Date"].dt.year

    # Convert 'Date' column to 'dd-mm-yyyy' format
    data['Date'] = data['Date'].dt.strftime('%d-%m-%Y')

    return data

# Load the raw data
data = load_data(url)

# Group by 'Group' and 'year' to calculate revenues
item_revenues = (
    data.groupby(["Group", "year"])['Amount']
    .sum()
    .unstack()
    .assign(change=lambda x: x.pct_change(axis=1)[YEAR] * 100)
)

# --- KEY METRICS ---
# Define groups dynamically based on available data
GROUPS = item_revenues.index.tolist()
columns = st.columns(len(GROUPS))

for idx, group in enumerate(GROUPS):
    with columns[idx]:
        st.metric(
            label=group,
            value=f"Rs {item_revenues.loc[group, YEAR]:,.2f}",
            delta=f"{item_revenues.loc[group, 'change']:.2f}% vs. Last Year"
        )

# --- SELECTION FIELDS ---
selected_group =  st.selectbox("Select a Group:", GROUPS)
show_previous_year = st.toggle("Show Previous Year")
if show_previous_year:
    visualization_year = YEAR - 1
else:
    visualization_year = YEAR

st.write(f"** Sales for {visualization_year}**")

# tabs for analysis
tab_month, tab_group =  st.tabs(['Monthly Analysis', 'Group Analysis'])

# --- FILTER & VISUALIZE DATA ---
with tab_month:
    filtered_data = (
        data.query("Group == @selected_group & year == @visualization_year").groupby("month", dropna=False, as_index=False)["Amount"].sum()
    )
    st.bar_chart(
        data=filtered_data.set_index("month")["Amount"]
    )

with tab_group:
    # Filter data for the selected year without filtering by group
    filtered_data = (
        data.query("year == @visualization_year")
        .groupby("Group", dropna=False, as_index=False)["Amount"]
        .sum()
    )

    # Create the bar chart for group analysis
    st.bar_chart(
        data=filtered_data.set_index("Group")["Amount"]
    )

