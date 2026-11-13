
# ==========================================
# SHOPLYTICS - E-COMMERCE SALES DASHBOARD
# ==========================================

# Import required libraries
import streamlit as st
import pandas as pd
import plotly.express as px
from pathlib import Path

# ------------------------------------------
# 1. PAGE CONFIGURATION
# ------------------------------------------

st.set_page_config(
    page_title="Shoplytics",
    page_icon="🛍️",
    layout="wide"
)

# ------------------------------------------
# 2. LOAD DATASET
# ------------------------------------------

# Find the folder containing this app.py file
BASE_DIR = Path(__file__).resolve().parent

# Load the dashboard dataset from the same folder
DATA_PATH = BASE_DIR / "shoplytics_dashboard.csv"

df = pd.read_csv(DATA_PATH)

# Convert InvoiceDate into datetime format
df["InvoiceDate"] = pd.to_datetime(df["InvoiceDate"])

# Convert YearMonth into a readable string
df["YearMonth"] = df["InvoiceDate"].dt.to_period("M").astype(str)

# Map cluster numbers to business-friendly names
cluster_names = {
    0: "At-Risk Customers",
    1: "Regular Customers",
    2: "VIP Customers"
}

df["Customer Segment"] = df["Cluster"].map(cluster_names)

# ------------------------------------------
# 3. DASHBOARD HEADER
# ------------------------------------------

st.title("🛍️ Shoplytics")
st.subheader("E-Commerce Sales Intelligence Dashboard")

st.write(
    "An interactive dashboard to analyse sales performance "
    "and customer behaviour."
)

st.divider()

# ------------------------------------------
# 4. INTERACTIVE FILTERS
# ------------------------------------------

# ------------------------------------------
# SIDEBAR NAVIGATION
# ------------------------------------------

st.sidebar.title("🛍️ Shoplytics")
st.sidebar.header("Dashboard Navigation")

page = st.sidebar.radio(
    "Go to",
    [
        "Overview",
        "Sales Analysis",
        "Customer Insights",
        "Transaction Records"
    ]
)

st.sidebar.divider()

st.sidebar.header("Dashboard Filters")

# Country filter
countries = ["All Countries"] + sorted(
    df["Country"].dropna().unique().tolist()
)

selected_country = st.sidebar.selectbox(
    "Select Country",
    countries
)

# Date range filter
min_date = df["InvoiceDate"].min().date()
max_date = df["InvoiceDate"].max().date()

selected_dates = st.sidebar.date_input(
    "Select Date Range",
    value=(min_date, max_date),
    min_value=min_date,
    max_value=max_date
)

# Customer segment filter
segments = ["All Segments"] + [
    "At-Risk Customers",
    "Regular Customers",
    "VIP Customers"
]

selected_segment = st.sidebar.selectbox(
    "Select Customer Segment",
    segments
)

# ------------------------------------------
# 5. APPLY FILTERS
# ------------------------------------------

filtered_df = df.copy()

# Apply country filter
if selected_country != "All Countries":
    filtered_df = filtered_df[
        filtered_df["Country"] == selected_country
    ]

# Apply date filter
if len(selected_dates) == 2:
    start_date, end_date = selected_dates

    filtered_df = filtered_df[
        (filtered_df["InvoiceDate"].dt.date >= start_date) &
        (filtered_df["InvoiceDate"].dt.date <= end_date)
    ]

# Apply customer segment filter
if selected_segment != "All Segments":
    filtered_df = filtered_df[
        filtered_df["Customer Segment"] == selected_segment
    ]

# ------------------------------------------
# 6. KEY PERFORMANCE INDICATORS
# ------------------------------------------

if page == "Overview":





    st.subheader("📊 Business Performance")

    # Calculate KPIs using filtered data
    total_revenue = filtered_df["Revenue"].sum()

    total_orders = filtered_df["InvoiceNo"].nunique()

    total_customers = filtered_df["CustomerID"].nunique()

    total_units = filtered_df["Quantity"].sum()

    # Display KPIs in four columns
    col1, col2, col3, col4 = st.columns(4)

    col1.metric(
        "Total Revenue",
        f"£{total_revenue:,.2f}"
    )

    col2.metric(
        "Total Orders",
        f"{total_orders:,}"
    )

    col3.metric(
        "Unique Customers",
        f"{total_customers:,}"
    )

    col4.metric(
        "Units Sold",
        f"{total_units:,}"
    )

    st.divider()
    # Business highlights
    st.subheader("📌 Business Highlights")

    st.info(
        "Explore sales trends, geographical performance "
        "and customer behaviour using the navigation menu. "
        "Use the sidebar filters to customise your analysis."
    )
        # Business Recommendations
    st.divider()
    st.subheader("💡 Business Recommendations")

    st.markdown("""
    - **Customer Retention:** Introduce loyalty rewards to encourage repeat purchases.
    - **VIP Customers:** Offer exclusive benefits to high-value customers.
    - **At-Risk Customers:** Use personalised offers and email campaigns to re-engage inactive customers.
    - **Product Strategy:** Focus on products generating the highest revenue.
    - **Geographical Expansion:** Explore opportunities in countries with growing sales.
    """)
        # Find the country generating the highest revenue
    country_revenue = (
        filtered_df.groupby("Country")["Revenue"]
        .sum()
        .sort_values(ascending=False)
    )

    top_country = country_revenue.index[0]
    top_country_revenue = country_revenue.iloc[0]

    st.subheader("🌍 Top Performing Country")

    st.metric(
        label=top_country,
        value=f"£{top_country_revenue:,.2f}"
    )

# ------------------------------------------
# 7. MONTHLY REVENUE TREND
# ------------------------------------------
if page == "Sales Analysis":

    st.subheader("📈 Monthly Revenue Trend")

    # Group filtered sales by month
    monthly_revenue = (
        filtered_df.groupby("YearMonth")["Revenue"]
        .sum()
        .reset_index()
    )

    # Create interactive line chart
    fig1 = px.line(
        monthly_revenue,
        x="YearMonth",
        y="Revenue",
        markers=True,
        title="Monthly Revenue Performance",
        labels={
            "YearMonth": "Month",
            "Revenue": "Revenue (£)"
        }
    )

    fig1.update_layout(
        hovermode="x unified"
    )

    st.plotly_chart(
        fig1,
        use_container_width=True
    )

    # Explain incomplete December data
    st.caption(
        "Note: December 2011 contains transactions only through "
        "9 December and is therefore an incomplete month."
    )

    st.divider()

# ------------------------------------------
# 8. REVENUE BY COUNTRY
# ------------------------------------------

    st.subheader("🌍 Revenue by Country")

    country_revenue = (
        filtered_df.groupby("Country")["Revenue"]
        .sum()
        .sort_values(ascending=False)
        .reset_index()
    )

    # Display top 10 countries
    top_countries = country_revenue.head(10)

    fig2 = px.bar(
        top_countries,
        x="Revenue",
        y="Country",
        orientation="h",
        title="Top 10 Countries by Revenue",
        color="Revenue",
        labels={"Revenue": "Revenue (£)"}
    )

    fig2.update_layout(
        yaxis={"categoryorder": "total ascending"}
    )

    st.plotly_chart(
        fig2,
        use_container_width=True
    )

    # Display a separate comparison excluding the UK
    non_uk = country_revenue[
        country_revenue["Country"] != "United Kingdom"
    ].head(9)

    fig3 = px.bar(
        non_uk,
        x="Revenue",
        y="Country",
        orientation="h",
        title="Revenue by Country (Excluding United Kingdom)",
        labels={"Revenue": "Revenue (£)"}
    )

    fig3.update_layout(
        yaxis={"categoryorder": "total ascending"}
    )

    st.plotly_chart(
        fig3,
        use_container_width=True
    )

    st.divider()
        # 10. PRODUCT PERFORMANCE
    st.subheader("🛍️ Top 10 Products by Revenue")

    product_data = filtered_df.dropna(subset=["Description"])

    top_products = (
        product_data.groupby("Description")["Revenue"]
        .sum()
        .sort_values(ascending=False)
        .head(10)
        .reset_index()
    )

    fig8 = px.bar(
        top_products,
        x="Revenue",
        y="Description",
        orientation="h",
        title="Top 10 Products by Revenue",
        labels={
            "Revenue": "Total Revenue (£)",
            "Description": "Product"
        },
        text="Revenue"
    )

    fig8.update_layout(
        yaxis={"categoryorder": "total ascending"}
    )

    st.plotly_chart(fig8, use_container_width=True)

# ------------------------------------------
# 9. CUSTOMER SEGMENTATION
# ------------------------------------------
if page == "Customer Insights":

    st.subheader("👥 Customer Segmentation")

    # Count unique customers in each segment
    segment_data = (
        filtered_df.dropna(subset=["CustomerID", "Customer Segment"])
        .groupby("Customer Segment")["CustomerID"]
        .nunique()
        .reset_index(name="Customers")
    )

    fig4 = px.bar(
        segment_data,
        x="Customer Segment",
        y="Customers",
        color="Customer Segment",
        text="Customers",
        title="Customer Distribution Across Segments"
    )

    st.plotly_chart(
        fig4,
        use_container_width=True
    )

# ------------------------------------------
# ------------------------------------------
# 10. CUSTOMER SEGMENT SUMMARY
# ------------------------------------------

st.subheader("📋 Customer Segment Summary")

# Calculate customer metrics for each segment
segment_summary = (
    filtered_df.dropna(subset=["CustomerID", "Customer Segment"])
    .groupby("Customer Segment")
    .agg(
        Customers=("CustomerID", "nunique"),
        Revenue=("Revenue", "sum"),
        Orders=("InvoiceNo", "nunique")
    )
    .reset_index()
)

# Calculate average revenue per customer
segment_summary["Revenue per Customer"] = (
    segment_summary["Revenue"] / segment_summary["Customers"]
)

# Round monetary values
segment_summary["Revenue"] = segment_summary["Revenue"].round(2)
segment_summary["Revenue per Customer"] = (
    segment_summary["Revenue per Customer"].round(2)
)

# Display the summary table
st.dataframe(
    segment_summary,
    use_container_width=True,
    hide_index=True
)

# Visualise revenue by customer segment
fig5 = px.bar(
    segment_summary,
    x="Customer Segment",
    y="Revenue",
    color="Customer Segment",
    text_auto=".2s",
    title="Revenue Contribution by Customer Segment"
)

st.plotly_chart(fig5, use_container_width=True)
# ------------------------------------------
# 11. CUSTOMER INSIGHTS
# ------------------------------------------

st.subheader("🏆 Top 10 Customers by Revenue")

# Exclude transactions without a CustomerID
customer_data = filtered_df.dropna(subset=["CustomerID"])

# Calculate total revenue for each customer
top_customers = (
    customer_data.groupby("CustomerID")["Revenue"]
    .sum()
    .sort_values(ascending=False)
    .head(10)
    .reset_index()
)

# Create an interactive bar chart
fig6 = px.bar(
    top_customers,
    x="Revenue",
    y="CustomerID",
    orientation="h",
    title="Top 10 Highest-Spending Customers",
    labels={
        "Revenue": "Revenue (£)",
        "CustomerID": "Customer ID"
    },
    text_auto=".2s"
)

fig6.update_layout(
    yaxis={"categoryorder": "total ascending"}
)

st.plotly_chart(fig6, use_container_width=True)
# ------------------------------------------
# TOP 10 MOST FREQUENT CUSTOMERS
# ------------------------------------------

st.subheader("🔁 Top 10 Most Frequent Customers")

# Exclude transactions without CustomerID
customer_frequency_data = filtered_df.dropna(
    subset=["CustomerID"]
)

# Count unique orders placed by each customer
top_frequent_customers = (
    customer_frequency_data.groupby("CustomerID")["InvoiceNo"]
    .nunique()
    .sort_values(ascending=False)
    .head(10)
    .reset_index(name="Total Orders")
)

# Create an interactive bar chart

 # Create an interactive customer frequency chart
fig7 = px.bar(
    top_frequent_customers,
    x="Total Orders",
    y="CustomerID",
    orientation="h",
    title="Top 10 Customers by Order Frequency",
    labels={
        "CustomerID": "Customer ID",
        "Total Orders": "Number of Orders"
    },
    text="Total Orders"
)

# Display complete customer IDs
fig7.update_layout(
    yaxis={"categoryorder": "total ascending"}
)

# Treat customer IDs as categories, not numerical values
fig7.update_yaxes(type="category")

# Display the chart
st.plotly_chart(fig7, use_container_width=True)   

# ------------------------------------------
# AVERAGE CUSTOMER SPENDING
# ------------------------------------------

st.subheader("💰 Average Customer Spending")

# Exclude transactions without CustomerID
valid_customers = filtered_df.dropna(
    subset=["CustomerID"]
)

# Calculate total spending for each customer
customer_spending = (
    valid_customers.groupby("CustomerID")["Revenue"]
    .sum()
)

# Calculate average spending across customers
average_spending = customer_spending.mean()

# Display the result
st.metric(
    "Average Revenue per Customer",
    f"£{average_spending:,.2f}"
)
    # Repeat vs One-Time Customer Analysis
st.divider()
st.subheader("👥 Repeat vs One-Time Customers")

# Count unique orders placed by each customer
customer_orders = (
    filtered_df.dropna(subset=["CustomerID"])
    .groupby("CustomerID")["InvoiceNo"]
    .nunique()
)

# Classify customers based on their order count
repeat_customers = (customer_orders > 1).sum()
one_time_customers = (customer_orders == 1).sum()

customer_type_data = pd.DataFrame({
    "Customer Type": ["Repeat Customers", "One-Time Customers"],
    "Number of Customers": [repeat_customers, one_time_customers]
})

# Display customer distribution
fig9 = px.pie(
    customer_type_data,
    names="Customer Type",
    values="Number of Customers",
    title="Repeat vs One-Time Customer Distribution",
    hole=0.45
)

st.plotly_chart(fig9, use_container_width=True)
    # Revenue Contribution by Customer Segment
st.divider()
st.subheader("💰 Revenue Contribution by Customer Segment")

segment_revenue = (
    filtered_df.dropna(subset=["Customer Segment"])
    .groupby("Customer Segment")["Revenue"]
    .sum()
    .reset_index()
)

fig10 = px.pie(
    segment_revenue,
    names="Customer Segment",
    values="Revenue",
    title="Revenue Distribution Across Customer Segments",
    hole=0.45
)

st.plotly_chart(fig10, use_container_width=True)
# ------------------------------------------
# 12. TRANSACTION RECORDS
# ------------------------------------------
if page == "Transaction Records":

    st.subheader("🧾 Transaction Records")

    with st.expander("View Sales Data"):
        st.dataframe(
            filtered_df.head(100),
            use_container_width=True
        )
        # Download filtered transaction data
    csv = filtered_df.to_csv(index=False).encode("utf-8")

    st.download_button(
        label="📥 Download Transaction Data",
        data=csv,
        file_name="shoplytics_filtered_data.csv",
        mime="text/csv"
    )
# ------------------------------------------
# 13. FOOTER
# ------------------------------------------

st.caption(
    "Shoplytics | E-Commerce Sales Intelligence "
    "and Customer Segmentation Using Python"
)
