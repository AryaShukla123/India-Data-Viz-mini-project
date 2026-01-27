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

primary = st.sidebar.selectbox('Select Primary Parameter',sorted(numeric_cols))

secondary = st.sidebar.selectbox('Select Secondary Parameter',sorted(numeric_cols))

normalize = st.sidebar.checkbox("Normalize values")


if primary == secondary:
    st.warning("Primary and Secondary parameters should be different")

plot = st.sidebar.button("Build Dashboard",type="primary",use_container_width=True)


if plot:

    st.title("Indian Data Visualization Dashboard")

    st.markdown("---")

    map_section = st.container()

    st.markdown("""
    This interactive dashboard helps visualize **district-wise Indian data**
    using maps and dynamic parameters like population, literacy rate, sex ratio etc.
    """)
    kpi_section = st.container()

    if selected_state == 'Overall India':
        kpi_df = df.copy()
    else:
        kpi_df = df[df['State'] == selected_state]

    if normalize:
        kpi_df = kpi_df.copy()
        kpi_df[primary] = (kpi_df[primary] - kpi_df[primary].min()) / (kpi_df[primary].max() - kpi_df[primary].min())
        kpi_df[secondary] = (kpi_df[secondary] - kpi_df[secondary].min()) / (
                    kpi_df[secondary].max() - kpi_df[secondary].min())

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

        if normalize:
            st.info("Values are normalized (0–1 scale) for fair comparison")
        else:
            st.info("Showing raw values")

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
            color_continuous_scale='Turbo' if normalize else 'Blues',
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

        st.subheader(f"Top 10 Districts (Table) – {primary}")

        top10_table = (
            kpi_df
            .sort_values(by=primary, ascending=False)
            .head(10)[['District', 'State', primary]]
        )

        st.dataframe(top10_table, use_container_width=True)

        st.subheader(f"Bottom 10 Districts (Table) – {primary}")

        bottom10_table = (
            kpi_df
            .sort_values(by=primary, ascending=True)
            .head(10)[['District', 'State', primary]]
        )

        st.dataframe(bottom10_table, use_container_width=True)

        st.markdown("---")

        st.subheader(f"Relationship between {primary} & {secondary}")

        fig_scatter = px.scatter(
            kpi_df,
            x=primary,
            y=secondary,
            color='State',
            hover_name='District',
            size=primary,
            size_max = 35 if normalize else 18,
            opacity=0.75,
            trendline='ols',
            title=f"{primary} vs {secondary} (District-wise)"
        )

        fig_scatter.update_layout(
            template='plotly_dark',
            title_font_size=22,
            xaxis_title=f"{primary} (Normalized)" if normalize else primary,
            yaxis_title=f"{secondary} (Normalized)" if normalize else secondary,
            legend_title="State",
            height=600
        )

        st.plotly_chart(fig_scatter, use_container_width=True)

        st.markdown("---")

    with tab3:

        if normalize:
            st.caption("Map values are normalized (0–1 scale)")
        else:
            st.caption("Map shows raw values")

        st.subheader("Geographical Visualization")
        st.caption("🔵 Size = Primary | 🎨 Color = Secondary")

        if selected_state == 'Overall India':
            fig = px.scatter_mapbox(
                kpi_df,
                lat="Latitude",
                lon="Longitude",
                size=primary,
                color=secondary,
                color_continuous_scale='Turbo' if normalize else 'Viridis',
                zoom=4,
                mapbox_style="carto-positron",
                size_max = 60 if normalize else 35,
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
                color_continuous_scale='Turbo' if normalize else 'Viridis',
                zoom=6,
                mapbox_style="carto-positron",
                size_max = 60 if normalize else 35,
                height=650,
                hover_name='District'
            )

        st.plotly_chart(fig, use_container_width=True)

        st.markdown("---")

    st.subheader("Download Report")

    csv = kpi_df.to_csv(index=False).encode('utf-8')

    st.download_button(
        label="⬇️ Download District-wise Data (CSV)",
        data=csv,
        file_name=f"{selected_state}_india_report.csv",
        mime='text/csv'
    )

else:

    welcome_html = """
    <style>
        .welcome-card {
            max-width: 800px;
            margin: 20px auto;
            padding: 40px;
            background: rgba(255, 255, 255, 0.05);
            border-radius: 20px;
            border: 1px solid rgba(255, 255, 255, 0.1);
            font-family: 'Source Sans Pro', sans-serif;
        }
        .step {
            display: flex;
            align-items: center;
            margin-bottom: 15px;
        }
        .step-number {
            background: #FF4B4B;
            color: white;
            border-radius: 50%;
            width: 30px;
            height: 30px;
            display: flex;
            justify-content: center;
            align-items: center;
            margin-right: 15px;
            font-weight: bold;
        }
    </style>

    <div class="welcome-card">
        <h1 style="text-align:center;">🇮🇳 Indian Data Visualization Dashboard</h1>
        <p style="text-align:center; color: #FAFAFA;">
            Explore district-wise Indian data using interactive charts, maps, and analytical insights.
        </p>
        <hr style="border: 0.5px solid #333; margin: 30px 0;">
        <div style="margin-left: 20px;">
            <h3 style="margin-bottom: 20px;">Get Started:</h3>
            <div class="step">
                <div class="step-number">1</div>
                <div>Select a <b>State</b> from the sidebar.</div>
            </div>
            <div class="step">
                <div class="step-number">2</div>
                <div>Choose <b>Primary & Secondary</b> parameters.</div>
            </div>
            <div class="step">
                <div class="step-number">3</div>
                <div>Click the <b>Build Dashboard</b> button.</div>
            </div>
        </div>
    </div>
    """
    st.markdown(welcome_html, unsafe_allow_html=True)










