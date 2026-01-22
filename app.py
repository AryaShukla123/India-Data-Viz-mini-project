import numpy as np
import pandas as pd
import streamlit as st
import plotly.express as px

st.set_page_config(layout='wide')

df = pd.read_csv('india (1).csv')

list_of_states = list(df['State'].unique())
list_of_states.insert(0,'Overall India')

st.sidebar.title('Indian Data Visualization')

selected_state = st.sidebar.selectbox('Select a state',list_of_states)

# select only numeric columns for parameters
numeric_cols = df.select_dtypes(include=np.number).columns.tolist()

primary = st.sidebar.selectbox(
    'Select Primary Parameter',
    sorted(numeric_cols)
)

secondary = st.sidebar.selectbox(
    'Select Secondary Parameter',
    sorted(numeric_cols)
)

if primary == secondary:
    st.sidebar.warning("Primary and Secondary parameters should be different")

plot = st.sidebar.button('Plot Graph')

st.title("📊 Indian Data Visualization Dashboard")

st.markdown("---")

map_section = st.container()

st.markdown("""
This interactive dashboard helps visualize **district-wise Indian data**
using maps and dynamic parameters like population, literacy rate, sex ratio etc.
""")
kpi_section = st.container()


if plot:


    with map_section:

        st.subheader("🗺️ Geographical Visualization")

        st.caption("🔵 Size represents primary parameter | 🎨 Color represents secondary parameter")

        if selected_state == 'Overall India':
            kpi_df = df.copy()

            fig = px.scatter_mapbox(
                df,
                lat="Latitude",
                lon="Longitude",
                size=primary,
                color=secondary,
                zoom=4,
                mapbox_style="carto-positron",
                size_max=35,
                height=650,
                hover_name='District'
            )

            st.plotly_chart(fig, use_container_width=True)

        else:
            kpi_df = df[df['State'] == selected_state]

            fig = px.scatter_mapbox(
                kpi_df,
                lat="Latitude",
                lon="Longitude",
                size=primary,
                color=secondary,
                zoom=6,
                mapbox_style="carto-positron",
                size_max=35,
                height=650,
                hover_name='District'
            )

            st.plotly_chart(fig, use_container_width=True)

            total_population = int(kpi_df['Population'].sum())
            avg_literacy = round(kpi_df['literacy_rate'].mean(), 2)
            avg_sex_ratio = round(kpi_df['sex_ratio'].mean(), 2)
            total_districts = kpi_df['District'].nunique()

            with kpi_section:
                col1, col2, col3, col4 = st.columns(4)

                col1.metric("👥 Total Population", f"{total_population:,}")
                col2.metric("📚 Avg Literacy Rate (%)", avg_literacy)
                col3.metric("⚖️ Avg Sex Ratio", avg_sex_ratio)
                col4.metric("🏘️ Total Districts", total_districts)

            st.markdown("---")



