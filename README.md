# Indian Census Data Explorer & Analytics Dashboard

![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=Streamlit&logoColor=white)
![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Plotly](https://img.shields.io/badge/Plotly-3F4F75?style=for-the-badge&logo=plotly&logoColor=white)
![Pandas](https://img.shields.io/badge/Pandas-150458?style=for-the-badge&logo=pandas&logoColor=white)

A high-performance, interactive analytical dashboard built with **Streamlit** to visualize and interpret district-level 2011 Indian Census data. This tool transforms raw geospatial and demographic data into actionable insights through statistical modeling and modern UI components.

## 🚀 Live Demo


## Key Features

### 1. Statistical Analysis & Insights
- **Pearson Correlation Engine:** Dynamically calculates the linear relationship ($r$) between any two selected parameters with automated natural language interpretations.
- **Z-Score Outlier Detection:** Implements automated anomaly detection to identify districts that perform significantly above or below the statistical mean ($Threshold > 2\sigma$).
- **Trendline Integration:** Visualizes linear regressions directly within scatter plots to validate data correlations.

### 2. Advanced Visualizations
- **Geospatial Intelligence:** Interactive Mapbox integration allowing for dual-parameter analysis (Size = Primary Metric | Color = Secondary Metric).
- **Data Normalization:** Built-in feature to scale variables (0-1) for fair comparison between districts with vastly different population scales.
- **Dynamic KPIs:** Real-time calculation of State/National averages, literacy rates, and sex ratios.

### 3. Modern UI/UX
- **Professional Theming:** Customized CSS for high-contrast sidebars, glassmorphism effects on KPI cards, and "Inter" typography.
- **User-Centric Navigation:** Tabbed interface separating high-level Overview, deep-dive Analysis, and Geographical mapping.

## Tech Stack & Engineering
- **Frontend:** Streamlit, HTML5/CSS3 (Custom Injection)
- **Data Processing:** Pandas, NumPy
- **Statistics:** Scipy.stats (Z-Scores, PearsonR)
- **Visualization:** Plotly Express (Bar, Scatter, Mapbox)
- **Geospatial:** Mapbox (Carto-positron)

## Project Structure
```text
├── app.py                # Main Streamlit application logic
├── india (1).csv         # 2011 Census Dataset with Lat/Lon
├── requirements.txt      # Project dependencies
└── README.md             # Documentation
```

## Installation & Setup
**1. Clone the repository:**

git clone https://github.com/AryaShukla123/India-Data-Viz-mini-project.git


**2. Install requirements:**

```
pip install -r requirements.txt
```

**3. Launch the dashboard:**

```
streamlit run app.py
```

## Data Source
This project utilizes the India Census 2011 dataset with geospatial indexing, featuring 640+ districts across 35 states and union territories.

## Contact
Arya Shukla - [LinkedIn](https://www.linkedin.com/in/arya-shukla-3517a3322) - arya.bnsd@gmail.com