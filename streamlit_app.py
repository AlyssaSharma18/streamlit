import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import math

st.title("Data App Assignment, on Oct 7th")

st.write("### Input Data and Examples")
# Ensure that Order_Date is parsed correctly as a datetime object
df = pd.read_csv("Superstore_Sales_utf8.csv", parse_dates=["Order_Date"])
st.dataframe(df)

# Check if 'Sub_Category' column exists
if 'Sub_Category' not in df.columns:
    st.error("The 'Sub_Category' column is missing from the dataset.")
else:
    # Question 1: Add a dropdown for category
    option = st.selectbox(
        "Category",
        ("Furniture", "Office Supplies", "Technology"),
    )

    st.write("You selected:", option)

    # Filter the dataframe based on the selected category
    filtered_df = df[df['Category'] == option]

    # Ensure that Order_Date is in datetime format
    filtered_df['Order_Date'] = pd.to_datetime(filtered_df['Order_Date'])

    # Aggregating sales by month for the selected category
    sales_by_month = filtered_df.resample('M', on='Order_Date')['Sales'].sum()

    # Display the filtered sales data
    st.write(f"### Monthly Sales for {option}")
    st.dataframe(sales_by_month)

    # Line chart of sales for the selected category
    st.line_chart(sales_by_month)

    # Bar chart of sales by subcategory for the selected category
    st.write(f"### Sales by Sub_Category for {option}")
    subcategory_sales = filtered_df.groupby('Sub_Category')['Sales'].sum().sort_values(ascending=False)
    st.bar_chart(subcategory_sales)

    # Exclude non-numeric columns like 'Order_Date' from the aggregation
    numeric_df = df.select_dtypes(include=['number'])

    # Aggregated sales by category for solid bars
    st.write(f"### Aggregated Sales by Category")
    st.dataframe(numeric_df.groupby(df['Category']).sum())

    # Bar chart with aggregated sales by category
    st.bar_chart(numeric_df.groupby(df['Category'], as_index=False).sum(), x="Category", y="Sales", color="#04f")

    # Display a line chart of overall sales aggregated by month
    st.write("### Aggregated Sales by Month (Overall)")
    overall_sales_by_month = numeric_df['Sales'].resample('M', on=df['Order_Date']).sum()
    st.line_chart(overall_sales_by_month)

    # Additional instructions or future additions can go here
    st.write("## Your additions")
    st.write("### (1) Add a multi-select for Sub_Category in the selected Category")
    st.write("### (2) Show a line chart of sales for the selected items in (2)")
    st.write("### (3) Show three metrics for the selected items: total sales, total profit, and overall profit margin")
    st.write("### (4) Use the delta option in the overall profit margin metric to show the difference with the average profit margin across categories")
