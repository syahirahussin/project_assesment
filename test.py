import streamlit as st
import numpy as np
import pandas as pd
import seaborn as sns
import plotly.express as px
import plotly.graph_objects as go  # New import
import matplotlib.pyplot as plt

# Load data
df = pd.read_csv('dataset.csv')

# Binning ages into groups
age_bins = [0, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100]
age_labels = ['0-10', '11-20', '21-30', '31-40', '41-50', '51-60', '61-70', '71-80', '81-90', '91-100']
df['Age Group'] = pd.cut(df['AGE'], bins=age_bins, labels=age_labels, right=False)

# Counts by sex
sex_counts = df['SEX'].value_counts()
labels = sex_counts.index.map({1: 'Male', 2: 'Female'})

# Streamlit configuration and sidebar navigation
st.set_page_config(
    page_title="Interactive Charts App",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.sidebar.title("Navigation")
st.sidebar.subheader("Choose a page")
page = st.sidebar.radio("Go to", ["Home", "Health Charts"])

# Home page
if page == "Home":
    st.title("Covid-19 in Mexico")
    st.write("This app helps you explore Covid-19 status in 2020.")
    from PIL import Image
    flag = Image.open('Flag_of_Mexico.svg.png')
    shrdc = Image.open('shrdc_logo.png')
    st.image(flag)
    st.image(shrdc, use_column_width=True)

# Health Charts page
elif page == "Health Charts":
    st.title("Interactive Charts")

    # Tabs for different charts
    tabs = st.tabs(["Admission Cases in 2020", "Cases by Age", "Cases by Sex"])

    # Line chart for Admission Cases
    with tabs[0]:
        st.subheader("Admission Cases in 2020")
        df['ADMISSION DATE'] = pd.to_datetime(df['ADMISSION DATE'], errors='coerce')
        filtered_data = df.dropna(subset=['ADMISSION DATE'])
        admissions_by_date = filtered_data.groupby('ADMISSION DATE').size().reset_index(name='Admission Count')

        line_chart = px.line(
            admissions_by_date,
            x='ADMISSION DATE',
            y='Admission Count',
            title='Trend of Hospital Admissions Over Time',
            labels={'ADMISSION DATE': 'Admission Date', 'Admission Count': 'Number of Admissions'}
        )
        line_chart.update_traces(mode="lines+markers", hovertemplate="Date: %{x}<br>Admissions: %{y}")
        st.plotly_chart(line_chart, use_container_width=True)

        # Interactive bar chart for Cases by Age
    with tabs[1]:
        st.subheader("Cases by Age")
        selected_age_groups = st.multiselect("Select Age Groups to display", age_labels)

        filtered_df = df[df['Age Group'].isin(selected_age_groups)] if selected_age_groups else df
        age_counts = filtered_df['Age Group'].value_counts().reindex(selected_age_groups or age_labels)

        bar_chart = px.bar(
            x=age_counts.index,
            y=age_counts.values,
            title="Distribution of Cases by Selected Age Groups",
            labels={'x': 'Age Group', 'y': 'Number of Cases'},
            hover_name=age_counts.index
        )
        bar_chart.update_traces(marker_color='teal', hovertemplate="Age Group: %{x}<br>Cases: %{y}")
        st.plotly_chart(bar_chart, use_container_width=True)


    # Semi-circle donut chart using Plotly
    with tabs[2]:
        st.subheader("Cases by Sex")
        
        # Plotly Pie chart for gender distribution
        fig = px.pie(
            df, 
            names=labels, 
            values=sex_counts.values,
            hole=0.4,  # Creates a donut effect
        )
        
        # Rotate to show as a half circle and hide upper half
        fig.update_traces(textinfo='percent+label', rotation=180, pull=[0.1, 0], 
                          marker=dict(colors=['#636EFA', '#EF553B']))
        fig.update_layout(
            title_text="Gender Distribution (Semi-circle Donut Chart)",
            showlegend=True,
        )
    
        # Display the Plotly figure
        st.plotly_chart(fig)
