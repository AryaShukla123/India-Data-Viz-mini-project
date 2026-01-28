import numpy as np
import pandas as pd
import streamlit as st
import plotly.express as px
import scipy.stats as stats

st.set_page_config(layout='wide')

st.markdown("""
    <style>
        /* Keep your professional font */
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;800&display=swap');

        html, body, [class*="css"], .stMarkdown {
            font-family: 'Inter', sans-serif;
        }

        /* 1. NEW SIDEBAR UI: High contrast background and border */
        [data-testid="stSidebar"] {
            min-width: 320px;
            max-width: 320px;
            background-color: #11141c !important; /* Distinct dark shade */
            border-right: 1px solid rgba(255, 255, 255, 0.1);
        }

        /* 2. HIGHLIGHTED DROPDOWNS: Making them visible against the sidebar */
        div[data-baseweb="select"] > div {
            background-color: #1e222d !important;
            border-radius: 8px !important;
            border: 1px solid rgba(255, 255, 255, 0.2) !important;
        }

        /* Highlighting widget labels for better readability */
        [data-testid="stWidgetLabel"] p {
            color: #ffffff !important;
            font-weight: 600 !important;
        }

        /* 3. ORIGINAL KPI STYLING: Preserved exactly as you had it */
        [data-testid="stMetricValue"] {
            font-size: 28px;
            color: #1f77b4;
            font-weight: 800;
        }

        div[data-testid="stMetric"] {
            background-color: rgba(255, 255, 255, 0.05);
            padding: 15px;
            border-radius: 10px;
            border: 1px solid rgba(255, 255, 255, 0.1);
        }

        .sidebar .sidebar-content {
            padding-top: 2rem;
        }
    </style>
""", unsafe_allow_html=True)

df = pd.read_csv('india (1).csv')

if 'female_literate' in df.columns and 'male_literate' in df.columns:
    # Adding 1 to denominator to prevent division by zero errors
    df['Literacy_Gender_Ratio'] = (df['Female_Literate'] / (df['Male_Literate'] + 1)) * 100


list_of_states = list(df['State'].unique())
list_of_states.insert(0,'Overall India')

st.sidebar.title('Indian Data Visualization')

selected_state = st.sidebar.selectbox('Select a state',list_of_states)

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

        st.subheader(f"Outlier Detection: {primary}")


        z_scores = stats.zscore(kpi_df[primary].dropna())
        kpi_df_outliers = kpi_df.dropna(subset=[primary]).copy()
        kpi_df_outliers['z_score'] = z_scores

        # Define threshold (2 is standard, 3 is for extreme outliers)
        threshold = 2
        outliers = kpi_df_outliers[abs(kpi_df_outliers['z_score']) > threshold]

        if not outliers.empty:
            st.warning(f"Found {len(outliers)} districts with unusual {primary} levels (Z-Score > {threshold})")

            # Split into High and Low outliers
            high_outliers = outliers[outliers['z_score'] > 0].sort_values('z_score', ascending=False)
            low_outliers = outliers[outliers['z_score'] < 0].sort_values('z_score', ascending=True)

            col_h, col_l = st.columns(2)

            with col_h:
                st.write("**Significantly Higher than Avg:**")
                st.dataframe(high_outliers[['District', primary, 'z_score']].head(5))

            with col_l:
                st.write("**Significantly Lower than Avg:**")
                st.dataframe(low_outliers[['District', primary, 'z_score']].head(5))
        else:
            st.success(f"No extreme outliers detected for {primary} in this selection.")

        st.subheader("Outliers By Scatter Plot")

        kpi_df['Is_Outlier'] = abs(stats.zscore(kpi_df[primary])) > 2

        fig_scatter = px.scatter(
            kpi_df,
            x=primary,
            y=secondary,
            color='Is_Outlier',
            color_discrete_map={True: 'red', False: 'blue'},
            hover_name='District',
            size=primary,
            size_max = 35 if normalize else 18,
            opacity=0.75,
            trendline='ols',
            title=f"Highlighting Outliers in {primary} vs {secondary}"
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
        st.subheader(f"Statistical Insight: {primary} vs {secondary}")

        corr_df = kpi_df[[primary, secondary]].dropna()
        if len(corr_df) > 1:
            correlation, p_value = stats.pearsonr(corr_df[primary], corr_df[secondary])


            col_corr, col_text = st.columns([1, 2])

            with col_corr:
                st.metric("Correlation (r)", round(correlation, 3))

            with col_text:

                if correlation > 0.7:
                    st.success(f"**Strong Positive Correlation:** As {primary} increases, {secondary} tends to increase significantly.")
                elif correlation > 0.3:
                    st.info(f"**Moderate Positive Correlation:** There is a general upward trend between these parameters.")
                elif correlation < -0.7:
                    st.warning(f"**Strong Negative Correlation:** As {primary} increases, {secondary} tends to decrease significantly.")
                elif correlation < -0.3:
                    st.info(f"**Moderate Negative Correlation:** There is a general downward trend between these parameters.")
                else:
                    st.info("**Weak/No Linear Correlation:** These two parameters don't seem to have a strong linear relationship.")
        else:
            st.error("Not enough data to calculate correlation.")

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










