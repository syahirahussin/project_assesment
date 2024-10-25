import streamlit as st
import numpy as np
import pandas as pd
import seaborn as sns
import plotly.express as px
import matplotlib.pyplot as plt

df = pd.read_csv('dataset.csv')

#for Age
age_bins = [0, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100]
age_labels = ['0-10', '11-20', '21-30', '31-40', '41-50', '51-60', '61-70', '71-80', '81-90', '91-100']
# Create an Age Group column
df['Age Group'] = pd.cut(df['AGE'], bins=age_bins, labels=age_labels, right=False)

#For Sex
sex_counts = df['SEX'].value_counts()
labels = sex_counts.index.map({1: 'Male', 2: 'Female'})

# multipage, nav bar
st.set_page_config(
    page_title="Interactive Charts App",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.sidebar.title("Navigation")
st.sidebar.subheader("Choose a page")
page = st.sidebar.radio("Go to", ["Home", "Health Charts"])

if page == "Home":
    st.title("Covid-19 in Mexico")
    st.write("This app helps you explore Covid-19 status in 2020.")
    from PIL import Image
    shrdc = Image.open('shrdc_logo.png')
    #st.image(shrdc)
    st.markdown("<div style='text-align: center;'>", unsafe_allow_html=True)
    st.image(shrdc, use_column_width=True)
    st.markdown("</div>", unsafe_allow_html=True)
    
elif page == "Health Charts":
    st.title("Interactive Charts")

    # Create tabs for different chart types
    tabs = st.tabs(["Admission Cases in 2020", "Cases by Age", "Cases by Sex"])

    # Line Chart Tab
    with tabs[0]:
        st.subheader("Admission Cases in 2020")
        # Convert 'ADMISSION DATE' to datetime format
        df['ADMISSION DATE'] = pd.to_datetime(df['ADMISSION DATE'], errors='coerce')

        # Filter out rows with missing or invalid 'ADMISSION DATE'
        filtered_data = df.dropna(subset=['ADMISSION DATE'])

        # Group by the 'ADMISSION DATE' and count the number of admissions per day
        admissions_by_date = filtered_data.groupby('ADMISSION DATE').size().reset_index(name='Admission Count')


        # Create a line chart to visualize the trend of admissions over time
        line_chart = px.line(admissions_by_date, 
            x='ADMISSION DATE', 
            y='Admission Count', 
            title='Trend of Hospital Admissions Over Time',
            labels={'ADMISSION DATE': 'Admission Date', 'Admission Count': 'Number of Admissions'}
        )

        st.plotly_chart(line_chart, use_container_width=True)

    # Bar Chart Tab
    with tabs[1]:
        st.subheader("Cases by Age")

        # Multi-select for selecting age groups
        selected_age_groups = st.multiselect("Select Age Groups to display", age_labels)


        # Default to all age groups if none are selected
        if selected_age_groups:
            filtered_df = df[df['Age Group'].isin(selected_age_groups)]
        else:
            filtered_df = df
            selected_age_groups = age_labels  # Display all age groups

        # Calculate counts for the selected age groups
        age_counts = filtered_df['Age Group'].value_counts().reindex(selected_age_groups)

        # Plotting the filtered data
        plt.figure(figsize=(10, 6))
        sns.barplot(x=age_counts.index, y=age_counts.values, palette="viridis")
        plt.title("Distribution of Cases by Selected Age Groups")
        plt.xlabel("Age Group")
        plt.ylabel("Number of Cases")
        st.pyplot(plt)
    
    
    # semi-circle donut chart
    with tabs[2]:
        st.subheader("Cases by Sex")
        
        fig, ax = plt.subplots(figsize=(8, 4), subplot_kw=dict(aspect="equal"))

        # Plotting the donut chart with a semi-circle
        wedges, texts, autotexts = ax.pie(
            sex_counts,
            startangle=90,         # Start angle to make it a semi-circle
            radius=1.2,            # Radius of the pie chart
            counterclock=False,    # Draw counterclockwise
            labels=labels,
            autopct='%1.1f%%',     # Percentage format
            wedgeprops=dict(width=0.4)  # Creates a donut hole
        )

        center_circle = plt.Circle((0, 0), 0.6, color='white', fc='white')
        ax.add_artist(center_circle)

        # Limit the view to half (semi-circle)
        ax.set_ylim(-1, 0.1)

        plt.title("Gender Distribution \n (Semi-circle Donut Chart)")
        st.pyplot(fig)  # Display the figure in Streamlit
