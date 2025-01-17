import streamlit as st
import pandas as pd
import altair as alt

# Load data
file_path = 'olympics.csv'  # Update with the correct path if necessary
data = pd.read_csv(file_path)

# Streamlit App Title
st.title("Olympics Statistics Dashboard")

# Sidebar Filters
st.sidebar.header("Filters")
regions = st.sidebar.multiselect("Select Region(s):", options=data["region"].unique(), default=data["region"].unique())
gdp_range = st.sidebar.slider("GDP Range (in billions):", 
                              float(data["gdp"].min()), float(data["gdp"].max()), 
                              (float(data["gdp"].min()), float(data["gdp"].max())))
pop_range = st.sidebar.slider("Population Range (in millions):", 
                               float(data["population"].min()), float(data["population"].max()), 
                               (float(data["population"].min()), float(data["population"].max())))

# Filter Data
filtered_data = data[(data["region"].isin(regions)) &
                     (data["gdp"] >= gdp_range[0]) &
                     (data["gdp"] <= gdp_range[1]) &
                     (data["population"] >= pop_range[0]) &
                     (data["population"] <= pop_range[1])]

# Overview Statistics
st.header("Overview")
col1, col2, col3 = st.columns(3)
with col1:
    st.metric("Total Medals", int(filtered_data["total"].sum()))
with col2:
    st.metric("Average GDP", f"${filtered_data["gdp"].mean():,.2f} B")
with col3:
    st.metric("Average Population", f"{filtered_data["population"].mean():,.2f} M")

# Data Table
st.subheader("Data Table")
st.dataframe(filtered_data)

# Visualizations
st.header("Visualizations")

# Medal Counts by Country
st.subheader("Medal Counts by Country")
bar_chart = alt.Chart(filtered_data).mark_bar().encode(
    x=alt.X("country", sort="-y"),
    y="total",
    color="region"
).properties(width=700, height=400)
st.altair_chart(bar_chart)

# GDP vs Total Medals
st.subheader("GDP vs Total Medals")
scatter_plot = alt.Chart(filtered_data).mark_circle(size=60).encode(
    x="gdp",
    y="total",
    color="region",
    tooltip=["country", "gdp", "total"]
).properties(width=700, height=400)
st.altair_chart(scatter_plot)

# Medal Distribution by Region
st.subheader("Medal Distribution by Region")
region_data = filtered_data.groupby("region")["total"].sum().reset_index()
pie_chart = alt.Chart(region_data).mark_arc().encode(
    theta="total",
    color="region",
    tooltip=["region", "total"]
).properties(width=400, height=400)
st.altair_chart(pie_chart)

# Detailed View
st.header("Detailed Country Statistics")
selected_country = st.selectbox("Select a Country:", options=filtered_data["country"].unique())
if selected_country:
    country_data = filtered_data[filtered_data["country"] == selected_country]
    st.write(country_data)
