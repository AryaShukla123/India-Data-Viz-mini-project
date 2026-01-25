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
    st.warning("Primary and Secondary parameters should be different")

plot = st.sidebar.button('Plot Graph')

st.title("Indian Data Visualization Dashboard")

st.markdown("---")

map_section = st.container()

st.markdown("""
This interactive dashboard helps visualize **district-wise Indian data**
using maps and dynamic parameters like population, literacy rate, sex ratio etc.
""")
kpi_section = st.container()


if plot:

    if selected_state == 'Overall India':
        kpi_df = df.copy()
    else:
        kpi_df = df[df['State'] == selected_state]

    tab1, tab2, tab3 = st.tabs(["Overview", "Analysis", "Map View"])

    with tab1:

        st.subheader("Key Performance Indicators")

        total_population = int(kpi_df['Population'].sum())
        avg_literacy = round(kpi_df['literacy_rate'].mean(), 2)
        avg_sex_ratio = round(kpi_df['sex_ratio'].mean(), 2)
        total_districts = kpi_df['District'].nunique()

        col1, col2, col3, col4 = st.columns(4)

        col1.metric("👥 Total Population", f"{total_population:,}")
        col2.metric("📚 Avg Literacy Rate (%)", avg_literacy)
        col3.metric("⚖️ Avg Sex Ratio", avg_sex_ratio)
        col4.metric("🏘️ Total Districts", total_districts)

        st.subheader("Top 5 States by Population")

        state_pop = (
            kpi_df
            .groupby('State')['Population']
            .sum()
            .sort_values(ascending=False)
            .head(5)
            .reset_index()
        )

        fig_state = px.bar(
            state_pop,
            x='State',
            y='Population',
            color='Population',
            color_continuous_scale='Viridis',
            text_auto='.2s',
            title="Top 5 States by Population"
        )

        fig_state.update_layout(
            template='plotly_dark',
            title_font_size=22,
            xaxis_title="State",
            yaxis_title="Population",
            height=450
        )

        st.plotly_chart(fig_state, use_container_width=True)

        st.markdown("---")

    with tab2:

        st.subheader(f"Analysis for: {primary}")

        primary_total = int(kpi_df[primary].sum())
        primary_avg = round(kpi_df[primary].mean(), 2)
        primary_max = kpi_df[primary].max()
        primary_min = kpi_df[primary].min()

        col1, col2, col3, col4 = st.columns(4)

        col1.metric(f"🔢 Total {primary}", f"{primary_total:,}")
        col2.metric(f"📊 Avg {primary}", primary_avg)
        col3.metric(f"⬆️ Max {primary}", primary_max)
        col4.metric(f"⬇️ Min {primary}", primary_min)

        st.subheader(f"Top 10 Districts by {primary}")

        top_districts = (
            kpi_df
            .sort_values(by=primary, ascending=False)
            .head(10)
        )

        fig_top = px.bar(
            top_districts,
            x=primary,
            y='District',
            orientation='h',
            color=primary,
            color_continuous_scale='Blues',
            text_auto='.2s',
            title=f"Top 10 Districts by {primary}"
        )

        fig_top.update_layout(
            title_font_size=22,
            xaxis_title=primary,
            yaxis_title="District",
            template='plotly_dark',
            height=500
        )

        st.plotly_chart(fig_top, use_container_width=True)

        st.subheader(f"Relationship between {primary} & {secondary}")

        fig_scatter = px.scatter(
            kpi_df,
            x=primary,
            y=secondary,
            color='State',
            hover_name='District',
            size=primary,
            size_max=18,
            opacity=0.75,
            trendline='ols',
            title=f"{primary} vs {secondary} (District-wise)"
        )

        fig_scatter.update_layout(
            template='plotly_dark',
            title_font_size=22,
            xaxis_title=primary,
            yaxis_title=secondary,
            legend_title="State",
            height=600
        )

        st.plotly_chart(fig_scatter, use_container_width=True)

        st.markdown("---")

    with tab3:
        st.subheader("Geographical Visualization")
        st.caption("🔵 Size = Primary | 🎨 Color = Secondary")

        if selected_state == 'Overall India':
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
        else:
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

    st.subheader("Download Report")

    csv = kpi_df.to_csv(index=False).encode('utf-8')

    st.download_button(
        label="⬇️ Download District-wise Data (CSV)",
        data=csv,
        file_name=f"{selected_state}_india_report.csv",
        mime='text/csv'
    )






