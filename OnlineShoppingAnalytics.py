import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import datetime
from PIL import Image
import plotly.express as px


#'''Load Data'''

df = pd.read_csv(r"C:\Users\HP\Desktop\vs code coding\.vscode\online_shopping_analytics.csv")
df["OrderDate"] = pd.to_datetime(df["OrderDate"], errors="coerce")


#'''Page Config & Theme'''

st.set_page_config(layout="wide", page_title="Online Shopping Analytics", page_icon="🛒")

# Custom CSS 
st.markdown("""
    <style>
    body {background-color: #f9f9f9;}
    .title-test {
        color: #008080;
        font-weight: bold;
        padding: 10px;
        border-radius: 8px;
        background-color: red;
    }
    .stMetric {
        background-color: ;
        border: 1px solid #008080;
        border-radius: 8px;
        padding: 10px;
    }
    </style>
""", unsafe_allow_html=True)


#'''Header'''

image = Image.open(r"C:\Users\HP\Downloads\logo.jpg")
col1, col2 = st.columns([0.2, 0.8])
with col1:
    st.image(image, use_container_width=True)
with col2:
    st.markdown('<h1 class="title-test">Online Shopping Analytics Dashboard</h1>', unsafe_allow_html=True)

st.write(f"📅 Last updated: {datetime.datetime.now().strftime('%d %B %Y')}")


'''Sidebar  with Filters'''

st.sidebar.header("Filters")

# Date filter
min_date, max_date = df["OrderDate"].min(), df["OrderDate"].max()
start_date = st.sidebar.date_input("Start Date", min_date)
end_date = st.sidebar.date_input("End Date", max_date)

# Category filter
category = st.sidebar.selectbox("Product Category", ["All"] + list(df["ProductCategory"].unique()))

# Payment filter
payment = st.sidebar.selectbox("Payment Method", ["All"] + list(df["PaymentMethod"].unique()))

# Gender filter
gender = st.sidebar.selectbox("Gender", ["All"] + list(df["Gender"].unique()))

# Age filter
min_age, max_age = int(df["Age"].min()), int(df["Age"].max())
age_range = st.sidebar.slider("Age Range", min_age, max_age, (min_age, max_age))

# Location filter
location = st.sidebar.selectbox("Location", ["All"] + list(df["Location"].unique()))

# Apply filters
filtered_df = df.copy()
filtered_df = filtered_df[(filtered_df["OrderDate"] >= pd.to_datetime(start_date)) &
                          (filtered_df["OrderDate"] <= pd.to_datetime(end_date))]
if category != "All":
    filtered_df = filtered_df[filtered_df["ProductCategory"] == category]
if payment != "All":
    filtered_df = filtered_df[filtered_df["PaymentMethod"] == payment]
if gender != "All":
    filtered_df = filtered_df[filtered_df["Gender"] == gender]
filtered_df = filtered_df[(filtered_df["Age"] >= age_range[0]) & (filtered_df["Age"] <= age_range[1])]
if location != "All":
    filtered_df = filtered_df[filtered_df["Location"] == location]


''' Tabs'''

tab1, tab2, tab3, tab4 = st.tabs(["📈 Sales", "👥 Customers", "📦 Products", "🚚 Delivery"])


#'''Sales Dashboard'''
with tab1:
    st.subheader("Revenue Trend")
    sales_trend = filtered_df.groupby("OrderDate")["TotalAmount"].sum().reset_index()
    fig = px.line(sales_trend, x="OrderDate", y="TotalAmount", template="plotly_white",
                  color_discrete_sequence=["#008080"], markers=True)
    st.plotly_chart(fig, use_container_width=True)

    st.subheader("Payment Method Distribution")
    payment_dist = filtered_df["PaymentMethod"].value_counts().reset_index()
    payment_dist.columns = ["PaymentMethod", "Count"]  # Rename columns

    fig = px.pie(payment_dist,
                 names="PaymentMethod",   # category column
                 values="Count",          # frequency column
                 color_discrete_sequence=px.colors.sequential.Teal,
                 title="Payment Method Distribution")
    st.plotly_chart(fig, use_container_width=True)


#'''Customer Dashboard'''
with tab2:
    st.subheader("Key Metrics")
    col1, col2, col3 = st.columns(3)
    col1.metric("Total Customers", filtered_df["CustomerID"].nunique())
    col2.metric("Avg Spend per Customer", f"{filtered_df.groupby('CustomerID')['TotalAmount'].sum().mean():.2f}")
    col3.metric("Avg Orders per Customer", f"{filtered_df.groupby('CustomerID')['OrderID'].count().mean():.2f}")

    st.subheader("Gender Distribution")
    fig = px.histogram(filtered_df, x="Gender", color="Gender", template="plotly_white",
                       color_discrete_sequence=["#008080", "#ff9933"])
    st.plotly_chart(fig, use_container_width=True)

    st.subheader("Age vs Spending")
    age_spend = filtered_df.groupby("Age")["TotalAmount"].sum().reset_index()
    fig = px.line(age_spend, x="Age", y="TotalAmount", template="plotly_white",
                  color_discrete_sequence=["#008080"], markers=True)
    st.plotly_chart(fig, use_container_width=True)

#'''Product Dashboard'''

with tab3:
    st.subheader("Top Products by Revenue")
    top_products = filtered_df.groupby("ProductName")["TotalAmount"].sum().nlargest(10).reset_index()
    fig = px.bar(top_products, x="ProductName", y="TotalAmount", template="plotly_white",
                 color="TotalAmount", color_continuous_scale="Tealgrn")
    st.plotly_chart(fig, use_container_width=True)

    st.subheader("Average Rating by Category")
    category_rating = filtered_df.groupby("ProductCategory")["Rating"].mean().reset_index()
    fig = px.bar(category_rating, x="ProductCategory", y="Rating", template="plotly_white",
                 color="Rating", color_continuous_scale="Oranges")
    st.plotly_chart(fig, use_container_width=True)


#'''Delivery Dashboard'''

with tab4:
    st.subheader("Delivery Status Distribution")
    delivery_status = filtered_df["DeliveryStatus"].value_counts().reset_index()
    delivery_status.columns = ["DeliveryStatus", "Count"]  # Rename columns

    fig = px.pie(delivery_status,
                 names="DeliveryStatus",   # category column
                 values="Count",           # frequency column
                 color_discrete_sequence=["#18A91F", "#F2F20D", "#BE1616", "#0E0BDC"],
                 title="Delivery Status Distribution")
    st.plotly_chart(fig, use_container_width=True)

    st.subheader("Delivery vs Ratings")
    fig = px.box(filtered_df, x="DeliveryStatus", y="Rating", template="plotly_white",
                 color="DeliveryStatus", color_discrete_sequence=["#E51515", "#daff33"])
    st.plotly_chart(fig, use_container_width=True)



#'''Data Preview'''

st.subheader("Filtered Data Preview")
st.dataframe(filtered_df.head(20))
