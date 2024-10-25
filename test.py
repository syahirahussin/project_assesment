import streamlit as st
import pandas as pd
import plotly.express as px

# Load dataset
file_path = 'dataset.csv'  # Replace with the correct path to your CSV file
data = pd.read_csv(file_path)

# Convert 'ADMISSION DATE' to datetime format
data['ADMISSION DATE'] = pd.to_datetime(data['ADMISSION DATE'], errors='coerce')

# Remove rows with missing 'ADMISSION DATE'
filtered_data = data.dropna(subset=['ADMISSION DATE'])

# Set up multipage and nav bar
st.set_page_config(
    page_title="Interactive Charts App",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.sidebar.title("Navigation")
st.sidebar.subheader("Choose a page")
page = st.sidebar.radio("Go to", ["Home", "Charts"])

if page == "Home":
    st.title("Welcome to the Interactive Charts App")
    st.write("Use the navigation bar to start.")
    from PIL import Image
    logo = Image.open('shrdc_logo.png')
    st.image(logo)


elif page == "Charts":
    st.title("Interactive Charts")

    # Create tabs for different chart types
    tabs = st.tabs(["Line Chart", "Bar Chart", "Scatter Plot"])

    # Line Chart Tab
    with tabs[0]:
        st.subheader("Line Chart")
        
        # Group by 'ADMISSION DATE' and count the number of admissions per day
        admissions_by_date = filtered_data.groupby('ADMISSION DATE').size().reset_index(name='Admission Count')
        
        # Line chart
        line_chart = px.line(
            admissions_by_date, 
            x='ADMISSION DATE', 
            y='Admission Count', 
            labels={'ADMISSION DATE': 'Admission Date', 'Admission Count': 'Number of Admissions'},
            title="Hospital Admissions Over Time"
        )
        line_chart.update_traces(mode='lines+markers', hovertemplate='Date: %{x}<br>Count: %{y}')
        
        st.plotly_chart(line_chart, use_container_width=True)

    # Bar Chart Tab
    with tabs[1]:
        st.subheader("Bar Chart")
        
        # Data for bar chart - showing counts by 'TREATMENT_LOCATION'
        treatment_counts = data['TREATMENT_LOCATION'].value_counts().reset_index()
        treatment_counts.columns = ['TREATMENT_LOCATION', 'Count']
        
        # Multiselect to choose specific treatment locations
        selected_locations = st.multiselect("Select Treatment Locations", treatment_counts['TREATMENT_LOCATION'].unique(), default=treatment_counts['TREATMENT_LOCATION'].unique())

        if not selected_locations:
            st.write("Please select treatment locations to display the bar chart.")
        else:
            # Filter by selected locations
            filtered_treatment_counts = treatment_counts[treatment_counts['TREATMENT_LOCATION'].isin(selected_locations)]
            
            # Bar chart
            bar_chart = px.bar(
                filtered_treatment_counts, 
                x='TREATMENT_LOCATION', 
                y='Count', 
                title="Patient Counts by Treatment Location",
                labels={'TREATMENT_LOCATION': 'Treatment Location', 'Count': 'Number of Patients'}
            )
            bar_chart.update_traces(hovertemplate='Location: %{x}<br>Count: %{y}')
            
            st.plotly_chart(bar_chart, use_container_width=True)

    # Scatter Plot Tab
    with tabs[2]:
        st.subheader("3D Scatter Plot")
        
        # Data for 3D scatter plot - using 'PATIENT_LOCATION', 'MUNICIPALITY', and 'HOSPITALIZED'
        scatter_3d = px.scatter_3d(
            filtered_data, 
            x='PATIENT_LOCATION', 
            y='MUNICIPALITY', 
            z='HOSPITALIZED',
            labels={'PATIENT_LOCATION': 'Patient Location', 'MUNICIPALITY': 'Municipality', 'HOSPITALIZED': 'Hospitalized'},
            title="3D Scatter Plot of Patients"
        )
        scatter_3d.update_traces(hovertemplate='Location: %{x}<br>Municipality: %{y}<br>Hospitalized: %{z}')
        
        st.plotly_chart(scatter_3d, use_container_width=True)