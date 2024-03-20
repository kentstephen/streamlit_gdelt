import streamlit as st
import duckdb
import pandas as pd

# Connect to DuckDB
conn = duckdb.connect('duckdb\gdelt.duckdb')

# SQL Query to select everything from the table
sql_query = """
SELECT
    extract(year from date) as year,
    extract(month from date) as month,
    *
FROM
    upd_multiple_countriesS_sum_of_criticsim_russia_2020_2024
ORDER BY
    year, month;
"""

# Execute query and load data into DataFrame
df = conn.execute(sql_query).df()

# Close DuckDB connection
conn.close()

# Convert 'date' to datetime format and create a 'MonthYear' column
df['date'] = pd.to_datetime(df['date'])
df['MonthYear'] = df['date'].dt.strftime('%Y-%m')

# Streamlit app adjustments
st.title("Countries Denouncing Russia (2020-2024)")

# Create checkboxes for each country
selected_countries = []
countries = ['USA', 'Germany', 'Poland', 'Hungary', 'France', 'China', 'UK']
for country in countries:
    if st.checkbox(country, True, key=country):
        selected_countries.append(country)

# Proceed if any countries are selected
if selected_countries:
    # Aggregate scores by MonthYear
    df_aggregated = df.groupby('MonthYear')[selected_countries].sum().reset_index()
    df_aggregated['MonthYear'] = pd.to_datetime(df_aggregated['MonthYear'])

    # Plot the aggregated scores by MonthYear
    st.write("Aggregated Scores by MonthYear")
    st.line_chart(df_aggregated.set_index('MonthYear')[selected_countries])

    # Slider for selecting a specific MonthYear
    st.write("Zoom into a specific Month-Year")
    unique_month_years = df['MonthYear'].drop_duplicates().sort_values()
    month_year_to_view = st.select_slider('Drag the Slider to View Different Months', options=unique_month_years, value=unique_month_years.iloc[0])

    # Filter the dataframe based on the selected month and year
    df_filtered = df[df['MonthYear'] == month_year_to_view]
    df_filtered.set_index('date', inplace=True)

    # Plot the detailed scores by the selected MonthYear
    st.line_chart(df_filtered[selected_countries])
else:
    st.write("Select at least one country to display the data.")
