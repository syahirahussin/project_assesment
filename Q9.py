import streamlit as st
import numpy as np
import pandas as pd
import plotly.express as px

# multipage, nav bar
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
    st.write("Navigation bar is the way for you to start")
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
        
        # Data
        x = np.arange(0, 10, 0.1)
        freq = st.slider("Select Frequency", min_value=1, max_value=10, value=1)
        y = np.sin(freq * x)

        # Line chart
        line_chart = px.line(x=x, y=y, labels={'x': 'X-axis', 'y': 'Y-axis'}, title="Sine Wave")
        line_chart.update_traces(mode='lines+markers', hovertemplate='X: %{x:.2f}<br>Y: %{y:.2f}')
        
        st.plotly_chart(line_chart, use_container_width=True)

    # Bar Chart Tab
    with tabs[1]:
        st.subheader("Bar Chart")
        
        # Data
        data = {'A': np.random.randint(1, 100, 5),
                'B': np.random.randint(1, 100, 5),
                'C': np.random.randint(1, 100, 5)}
        df = pd.DataFrame(data)

        # Multiselect
        columns = st.multiselect("Select columns to display", df.columns.tolist(), default=[])

        if not columns:
            st.write("Please select columns to display the bar chart.")
        else:
            # Bar chart created
            bar_chart = px.bar(df[columns], title="Bar Chart", labels={'index': 'Category', 'value': 'Values'})
            bar_chart.update_traces(hovertemplate='Category: %{x}<br>Value: %{y}')
            
            st.plotly_chart(bar_chart, use_container_width=True)

    # Scatter Plot Tab
    with tabs[2]:
        st.subheader("3D Scatter Plot")
        
        # Data for 3D scatter plot
        x = np.random.randn(100)
        y = np.random.randn(100)
        z = np.random.randn(100)

        # Create 3D scatter plot
        scatter_3d = px.scatter_3d(
            x=x,
            y=y,
            z=z,
            labels={'x': 'X-axis', 'y': 'Y-axis', 'z': 'Z-axis'},
            title="3D Scatter Plot"
        )
        scatter_3d.update_traces(hovertemplate='X: %{x:.2f}<br>Y: %{y:.2f}<br>Z: %{z:.2f}')
        
        st.plotly_chart(scatter_3d, use_container_width=True)