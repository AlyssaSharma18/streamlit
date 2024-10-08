import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import math

st.title("Data App Assignment, on Oct 7th")

st.write("### Input Data and Examples")
df = pd.read_csv("Superstore_Sales_utf8.csv", parse_dates=True)
st.dataframe(df)

# Question 1

option = st.selectbox(
    "Category:",
    ("Furniture", "Office Supplies", "Technology"),
)

st.write("You selected:", option)

# Question 2

# Define subcategories for each category
subcategory_options = {
    "Furniture": ["Bookcases", "Chairs", "Tables", "Furnishings", "Art"],
    "Office Supplies": ["Labels", "Storage", "Binders", "Appliances", "Paper", "Envelopes", "Fasteners"],
    "Technology": ["Phones", "Accessories"],
}

# Multiselect for subcategories based on the selected category
options = st.multiselect(
    "Subcategory:",
    subcategory_options[option],  # Get subcategories for the selected category
)

st.write("You selected:", options)

#Question 3 

# Filter the DataFrame based on selected category and subcategories
filtered_df = df[df['Category'] == option]

if options:
    filtered_df = filtered_df[filtered_df['Sub_Category'].isin(options)]

# Check if the filtered DataFrame is not empty
if not filtered_df.empty:
    # Ensure Order_Date is in datetime format and set as an index
    filtered_df["Order_Date"] = pd.to_datetime(filtered_df["Order_Date"])
    filtered_df.set_index("Order_Date", inplace=True)

    # Group sales by month
    sales_by_month = filtered_df.resample('M')['Sales'].sum()

    # Do the calculations for question 4
    # Calculate total sales for the selected category and subcategories
    total_sales = filtered_df['Sales'].sum()

    # Add calculations for profit and profit margin if those columns exist in your dataset.
    total_profit = filtered_df['Profit'].sum() if 'Profit' in filtered_df.columns else 0
    overall_profit_margin = (total_profit / total_sales * 100) if total_sales > 0 else 0
    
    #End calculations for question 4

    #Question 5
    # Calculate the overall average profit margin across all categories
    total_sales_all = df['Sales'].sum()
    total_profit_all = df['Profit'].sum() if 'Profit' in df.columns else 0
    overall_average_profit_margin = (total_profit_all / total_sales_all * 100) if total_sales_all > 0 else 0

    # Calculate the delta (difference) between the overall profit margin and the overall average profit margin
    profit_margin_delta = overall_profit_margin - overall_average_profit_margin

    #End question 5
    
    # Display the line chart of sales for the selected items in the selected subcategory
    st.line_chart(sales_by_month)

    # Back to Question 4
    
    # Metrics for total sales, total profit, and overall profit margin
    col1, col2, col3 = st.columns(3)
    col1.metric("Total Sales", f"${total_sales:,.2f}")
    col2.metric("Total Profit", f"${total_profit:,.2f}")
    col3.metric(
        "Overall Profit Margin", 
        f"{overall_profit_margin:.2f}%", 
        delta=f"{profit_margin_delta:.2f}%"  # Format delta correctly
    )   

    # End Question 4


else:
    st.write("No sales data available for the selected subcategory.")


#Return to original code

# This bar chart will not have solid bars--but lines--because the detail data is being graphed independently
st.bar_chart(df, x="Category", y="Sales")

# Now let's do the same graph where we do the aggregation first in Pandas... (this results in a chart with solid bars)
st.dataframe(df.groupby("Category").sum())
# Using as_index=False here preserves the Category as a column.  If we exclude that, Category would become the datafram index and we would need to use x=None to tell bar_chart to use the index
st.bar_chart(df.groupby("Category", as_index=False).sum(), x="Category", y="Sales", color="#04f")

# Aggregating by time
# Here we ensure Order_Date is in datetime format, then set is as an index to our dataframe
df["Order_Date"] = pd.to_datetime(df["Order_Date"])
df.set_index('Order_Date', inplace=True)
# Here the Grouper is using our newly set index to group by Month ('M')
sales_by_month = df.filter(items=['Sales']).groupby(pd.Grouper(freq='M')).sum()

st.dataframe(sales_by_month)

# Here the grouped months are the index and automatically used for the x axis
st.line_chart(sales_by_month, y="Sales")

st.write("## Your additions")
st.write("### (1) add a drop down for Category (https://docs.streamlit.io/library/api-reference/widgets/st.selectbox)")
st.write("### (2) add a multi-select for Sub_Category *in the selected Category (1)* (https://docs.streamlit.io/library/api-reference/widgets/st.multiselect)")
st.write("### (3) show a line chart of sales for the selected items in (2)")
st.write("### (4) show three metrics (https://docs.streamlit.io/library/api-reference/data/st.metric) for the selected items in (2): total sales, total profit, and overall profit margin (%)")
st.write("### (5) use the delta option in the overall profit margin metric to show the difference between the overall average profit margin (all products across all categories)")
