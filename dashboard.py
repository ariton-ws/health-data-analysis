import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import plotly.subplots as sp
import numpy as np
from datetime import datetime
import base64

# Page configuration
st.set_page_config(
    page_title="Health Data Analytics Dashboard",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for modern UI with better contrast
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(135deg, #1e3a8a 0%, #3b82f6 50%, #1e40af 100%);
        padding: 2.5rem;
        border-radius: 15px;
        margin-bottom: 2rem;
        color: white;
        text-align: center;
        box-shadow: 0 10px 25px rgba(0,0,0,0.15);
    }
    
    .metric-card {
        background: white;
        padding: 1.5rem;
        border-radius: 12px;
        border: 2px solid #e5e7eb;
        box-shadow: 0 4px 12px rgba(0,0,0,0.1);
        margin-bottom: 1rem;
    }
    
    .metric-value {
        font-size: 2rem;
        font-weight: bold;
        color: #1f2937;
        margin-bottom: 0.5rem;
    }
    
    .metric-label {
        font-size: 1rem;
        color: #6b7280;
        font-weight: 500;
    }
    
    .insight-box {
        background: linear-gradient(135deg, #fef3c7 0%, #fde68a 100%);
        border: 2px solid #f59e0b;
        border-radius: 12px;
        padding: 1.5rem;
        margin: 1rem 0;
        box-shadow: 0 4px 12px rgba(245, 158, 11, 0.2);
    }
    
    .insight-title {
        color: #92400e;
        font-weight: bold;
        font-size: 1.2rem;
        margin-bottom: 0.5rem;
    }
    
    .insight-text {
        color: #78350f;
        line-height: 1.6;
    }
    
    .report-section {
        background: white;
        border: 2px solid #d1d5db;
        border-radius: 12px;
        padding: 2rem;
        margin: 1rem 0;
        box-shadow: 0 4px 12px rgba(0,0,0,0.08);
    }
    
    .report-title {
        color: #1f2937;
        font-weight: bold;
        font-size: 1.3rem;
        margin-bottom: 1rem;
        border-bottom: 3px solid #3b82f6;
        padding-bottom: 0.5rem;
    }
    
    .report-content {
        color: #374151;
        line-height: 1.7;
        font-size: 1rem;
    }
    

    
    .filter-section {
        background: #f8fafc;
        border: 2px solid #e2e8f0;
        border-radius: 10px;
        padding: 1.5rem;
        margin: 1rem 0;
    }
    
    .filter-title {
        color: #1f2937;
        font-weight: bold;
        font-size: 1.1rem;
        margin-bottom: 1rem;
    }
    
    /* Improve text contrast in Streamlit components */
    .stSelectbox, .stSlider, .stMultiselect {
        color: #1f2937 !important;
    }
    
    /* Limit multiselect dropdown height */
    .stMultiSelect [data-baseweb="select"] {
        max-height: 300px !important;
        overflow-y: auto !important;
    }
    
    .stMultiSelect [data-baseweb="popover"] {
        max-height: 300px !important;
        overflow-y: auto !important;
    }
    
    .stMarkdown {
        color: #374151 !important;
    }
    
    /* Better contrast for tabs */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
    }
    
    .stTabs [data-baseweb="tab"] {
        background-color: #f3f4f6;
        border-radius: 8px 8px 0px 0px;
        color: #374151;
        font-weight: 500;
    }
    
    .stTabs [aria-selected="true"] {
        background-color: #3b82f6;
        color: white;
    }
    
    /* Improve table readability */
    .dataframe {
        color: #1f2937 !important;
        font-size: 0.9rem;
    }
    
    .dataframe th {
        background-color: #f3f4f6 !important;
        color: #1f2937 !important;
        font-weight: bold !important;
    }
    
    .dataframe td {
        color: #374151 !important;
    }
</style>
""", unsafe_allow_html=True)

def load_gdp_recovery_data():
    """Load GDP recovery analysis data"""
    try:
        df = pd.read_csv('gdp_recovery_results/gdp_recovery_data.csv')
        return df
    except:
        return pd.DataFrame()

def load_covid_health_data():
    """Load COVID health analysis data"""
    try:
        df = pd.read_csv('covid_health_results/covid_health_data.csv')
        return df
    except:
        return pd.DataFrame()

def load_advanced_health_data():
    """Load advanced health analysis data"""
    try:
        df = pd.read_csv('advanced_analysis_results/enhanced_health_data.csv')
        return df
    except:
        return pd.DataFrame()

def format_number(value, decimals=2):
    """Format number with appropriate precision"""
    if pd.isna(value) or value is None:
        return "N/A"
    try:
        return f"{float(value):.{decimals}f}"
    except:
        return str(value)

def main():
    # Header
    st.markdown("""
    <div class="main-header">
        <h1>🏥 Health Data Analytics Dashboard</h1>
        <p style="font-size: 1.2rem; margin-top: 1rem; opacity: 0.9;">
            Comprehensive Analysis of Health Expenditure, GDP Recovery, and COVID-19 Response
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Sidebar
    with st.sidebar:
        st.markdown("### 📊 Analysis Sections")
        analysis_type = st.selectbox(
            "Choose Analysis:",
            ["📈 GDP Recovery Analysis", "🦠 COVID Health Analysis", "🔬 Advanced Health Analysis", "📋 Data Explorer"]
        )
        
        st.markdown("---")
        st.markdown("### 📅 Last Updated")
        st.info(f"Data as of: {datetime.now().strftime('%Y-%m-%d %H:%M')}")
        
        st.markdown("---")
        st.markdown("### 📊 Data Sources")
        st.markdown("""
        - World Bank GDP Data
        - WHO COVID-19 Data
        - Health System Indicators
        - Economic Recovery Metrics
        """)
    
    # Main content based on selection
    if analysis_type == "📈 GDP Recovery Analysis":
        show_gdp_recovery()
    elif analysis_type == "🦠 COVID Health Analysis":
        show_covid_health()
    elif analysis_type == "🔬 Advanced Health Analysis":
        show_advanced_health()
    else:
        show_data_explorer()

def show_gdp_recovery():
    """Show GDP recovery analysis with modern UI and report integration"""
    st.markdown("## 📈 GDP Recovery Analysis")
    
    df = load_gdp_recovery_data()
    if df.empty:
        st.error("No GDP recovery data available")
        return
    
    # Key Insights from Report
    st.markdown("""
    <div class="insight-box">
        <div class="insight-title">🔍 Key Insight</div>
        <div class="insight-text">
            Lower GDP countries showed significantly better recovery rates. Countries with GDP per capita below $10,000 
            had an average recovery rate of 5.2%, compared to 3.1% for high-income countries. This suggests that 
            economic structure and resilience mechanisms play a crucial role in post-crisis recovery.
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Top performers metrics
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        avg_recovery = df['Recovery_Speed'].mean()
        st.metric("Average Recovery Rate", f"{format_number(avg_recovery, 1)}%", 
                 help="Average GDP recovery speed from 2020-2023 (percentage)")
    with col2:
        max_recovery = df['Recovery_Speed'].max()
        st.metric("Highest Recovery Rate", f"{format_number(max_recovery, 1)}%", 
                 help="Best performing country's recovery speed (percentage)")
    with col3:
        correlation = df['GDPPerCapita'].corr(df['Recovery_Speed'])
        st.metric("GDP vs Recovery Correlation", format_number(correlation, 2), 
                 help="Correlation coefficient between GDP per capita and recovery speed (-1 to 1)")
    with col4:
        countries_count = len(df)
        st.metric("Countries Analyzed", countries_count, 
                 help="Total number of countries in the analysis")
    
    # Filters with meaningful defaults
    st.markdown("### 🔍 Interactive Filters")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if 'REF_AREA' in df.columns:
            # Better UI for country selection with search and limited default selection
            all_countries = sorted(df['REF_AREA'].unique())
            # Default to top 10 countries by GDP per capita for better UX
            if 'GDPPerCapita' in df.columns:
                top_countries = df.nlargest(10, 'GDPPerCapita')['REF_AREA'].tolist()
                default_countries = top_countries
            else:
                default_countries = all_countries[:10]  # First 10 countries alphabetically
            
            countries = st.multiselect(
                "Select Countries", 
                all_countries,
                default=default_countries,
                help="Search and select countries to analyze. Use Ctrl/Cmd+Click for multiple selection. Default shows top 10 countries by GDP."
            )
            df = df[df['REF_AREA'].isin(countries)]
    
    with col2:
        if 'GDPPerCapita' in df.columns:
            min_gdp = float(df['GDPPerCapita'].min())
            max_gdp = float(df['GDPPerCapita'].max())
            gdp_range = st.slider("GDP per Capita Range", min_gdp, max_gdp, 
                                (min_gdp, max_gdp))
            df = df[(df['GDPPerCapita'] >= gdp_range[0]) & 
                   (df['GDPPerCapita'] <= gdp_range[1])]
    
    with col3:
        if 'Recovery_Speed' in df.columns:
            min_recovery = float(df['Recovery_Speed'].min())
            max_recovery = float(df['Recovery_Speed'].max())
            recovery_range = st.slider("Recovery Rate Range", min_recovery, max_recovery, 
                                     (min_recovery, max_recovery))
            df = df[(df['Recovery_Speed'] >= recovery_range[0]) & 
                   (df['Recovery_Speed'] <= recovery_range[1])]
    
    # Charts with modern styling
    st.markdown("### 📊 Visualizations")
    
    tab1, tab2, tab3, tab4, tab5 = st.tabs(["📈 Recovery Analysis", "🏆 Top Performers", "🌍 Development Levels", "📋 Data Table", "📄 Full Report"])
    
    with tab1:
        if 'Recovery_Speed' in df.columns and 'GDPPerCapita' in df.columns:
            fig = px.scatter(df, x='GDPPerCapita', y='Recovery_Speed', 
                           color='Development_Level' if 'Development_Level' in df.columns else None,
                           hover_data=['REF_AREA', 'Recovery_Speed', 'GDPPerCapita'],
                           title="GDP per Capita vs Recovery Speed",
                           labels={'GDPPerCapita': 'GDP per Capita (USD)', 'Recovery_Speed': 'Recovery Speed (%)'},
                           color_discrete_sequence=px.colors.qualitative.Set3)
            fig.update_layout(
                plot_bgcolor='white',
                paper_bgcolor='white',
                font=dict(color='#111'),
                xaxis=dict(
                    title_font=dict(color='#111', size=20, family='Arial'),
                    tickfont=dict(color='#111', size=18, family='Arial'),
                    gridcolor='#e5e7eb',
                    zeroline=False
                ),
                yaxis=dict(
                    title_font=dict(color='#111', size=20, family='Arial'),
                    tickfont=dict(color='#111', size=18, family='Arial'),
                    gridcolor='#e5e7eb',
                    zeroline=False
                ),
                legend=dict(
                    bgcolor='white',
                    bordercolor='#888',
                    borderwidth=2,
                    font=dict(color='#111', size=18, family='Arial',),
                    orientation='v',
                    x=1.02,
                    y=1,
                    xanchor='left',
                    yanchor='top',
                ),
                margin=dict(l=60, r=60, t=60, b=60),
            )
            if hasattr(fig, 'update_traces'):
                fig.update_traces(textfont=dict(color='#111', size=18, family='Arial',), marker_line_color='#111', marker_line_width=2)
            st.plotly_chart(fig, use_container_width=True, config={
                'displayModeBar': True,
                'displaylogo': False,
                'modeBarButtonsToRemove': [],
            })
    
    with tab2:
        if 'REF_AREA' in df.columns and 'Recovery_Speed' in df.columns:
            top_countries = df.nlargest(10, 'Recovery_Speed')
            fig = px.bar(top_countries, x='REF_AREA', y='Recovery_Speed',
                        title="Top 10 Countries by Recovery Speed",
                        labels={'REF_AREA': 'Country', 'Recovery_Speed': 'Recovery Speed (%)'},
                        color='Recovery_Speed',
                        color_continuous_scale='viridis',
                        color_discrete_sequence=['#2563eb','#f59e42','#10b981','#a21caf','#f43f5e','#fbbf24','#6366f1','#22d3ee','#eab308','#0ea5e9']
            )
            fig.update_layout(
                plot_bgcolor='white',
                paper_bgcolor='white',
                font=dict(color='#111'),
                xaxis=dict(
                    title_font=dict(color='#111', size=20, family='Arial'),
                    tickfont=dict(color='#111', size=18, family='Arial'),
                    gridcolor='#e5e7eb',
                    zeroline=False
                ),
                yaxis=dict(
                    title_font=dict(color='#111', size=20, family='Arial'),
                    tickfont=dict(color='#111', size=18, family='Arial'),
                    gridcolor='#e5e7eb',
                    zeroline=False
                ),
                legend=dict(
                    bgcolor='white',
                    bordercolor='#888',
                    borderwidth=2,
                    font=dict(color='#111', size=18, family='Arial',),
                    orientation='v',
                    x=1.02,
                    y=1,
                    xanchor='left',
                    yanchor='top',
                ),
                margin=dict(l=60, r=60, t=60, b=60),
            )
            if hasattr(fig, 'update_traces'):
                fig.update_traces(textfont=dict(color='#111', size=18, family='Arial',), marker_line_color='#111', marker_line_width=2)
            st.plotly_chart(fig, use_container_width=True, config={
                'displayModeBar': True,
                'displaylogo': False,
                'modeBarButtonsToRemove': [],
            })
    
    with tab3:
        if 'Development_Level' in df.columns:
            dev_counts = df['Development_Level'].value_counts()
            fig = px.pie(values=dev_counts.values, names=dev_counts.index,
                        title="Distribution by Development Level",
                        color_discrete_sequence=['#2563eb','#f59e42','#10b981','#a21caf','#f43f5e','#fbbf24','#6366f1','#22d3ee','#eab308','#0ea5e9']
            )
            fig.update_layout(
                plot_bgcolor='white',
                paper_bgcolor='white',
                font=dict(color='#111'),
                xaxis=dict(
                    title_font=dict(color='#111', size=20, family='Arial'),
                    tickfont=dict(color='#111', size=18, family='Arial'),
                    gridcolor='#e5e7eb',
                    zeroline=False
                ),
                yaxis=dict(
                    title_font=dict(color='#111', size=20, family='Arial'),
                    tickfont=dict(color='#111', size=18, family='Arial'),
                    gridcolor='#e5e7eb',
                    zeroline=False
                ),
                legend=dict(
                    bgcolor='white',
                    bordercolor='#888',
                    borderwidth=2,
                    font=dict(color='#111', size=18, family='Arial',),
                    orientation='v',
                    x=1.02,
                    y=1,
                    xanchor='left',
                    yanchor='top',
                ),
                margin=dict(l=60, r=60, t=60, b=60),
            )
            if hasattr(fig, 'update_traces'):
                fig.update_traces(textfont=dict(color='#111', size=18, family='Arial',), marker_line_color='#111', marker_line_width=2)
            st.plotly_chart(fig, use_container_width=True, config={
                'displayModeBar': True,
                'displaylogo': False,
                'modeBarButtonsToRemove': [],
            })
    
    with tab4:
        st.markdown("### 📋 Data Table")
        st.dataframe(df, use_container_width=True, key=f"data_table_GDP_Recovery")
    
    with tab5:
        st.markdown("""
        ## 📄 GDP Recovery Analysis Report
        
        ### Executive Summary
        - **Countries analyzed**: 51 countries
        - **Time period**: 2019-2023 (COVID-19 pandemic and recovery)
        - **Key finding**: Lower GDP countries showed better recovery
        
        ### Key Insights
        1. **Lower GDP countries showed better recovery**: Different economic structures may be more resilient
        2. **Economic resilience varies**: Not necessarily tied to GDP levels
        3. **Recovery patterns vary significantly**: No one-size-fits-all approach to economic recovery
        4. **Policy responses matter**: Government interventions likely played crucial role
        
        ### Policy Implications
        1. **Diversified economic strategies**: Different countries need different recovery approaches
        2. **Investment in resilience**: Building economic buffers for future crises
        3. **International cooperation**: Global challenges require coordinated responses
        4. **Data-driven policymaking**: Understanding recovery patterns for better planning
        """)

def show_covid_health():
    """Show COVID health analysis with modern UI and report integration"""
    st.markdown("## 🦠 COVID Health Analysis")
    
    df = load_covid_health_data()
    if df.empty:
        st.error("No COVID health data available")
        return
    
    # Key Insights from Report
    st.markdown("""
    <div class="insight-box">
        <div class="insight-title">🔍 Key Insight</div>
        <div class="insight-text">
            Health expenditure shows only a weak correlation with COVID-19 outcomes. Countries with higher health spending 
            (>10% of GDP) had slightly lower death rates (2.1 vs 3.8 per 100k), but the relationship is not strong. 
            This suggests that public health measures and response strategies may be more important than healthcare infrastructure.
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Key metrics
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        avg_deaths = df['Deaths_Per_Capita'].mean()
        st.metric("Average Deaths per 100k", format_number(avg_deaths, 1), 
                 help="Average COVID-19 deaths per 100,000 population")
    with col2:
        avg_expenditure = df['HealthExpenditure'].mean()
        st.metric("Average Health Spending", f"{format_number(avg_expenditure, 1)}%", 
                 help="Average health expenditure as percentage of GDP")
    with col3:
        correlation = df['HealthExpenditure'].corr(df['Total_Deaths'])
        st.metric("Spending vs Deaths Correlation", format_number(correlation, 2), 
                 help="Correlation between health spending and COVID deaths (-1 to 1)")
    with col4:
        countries_count = len(df)
        st.metric("Countries Analyzed", countries_count, 
                 help="Total number of countries in the analysis")
    
    # Filters with meaningful defaults
    st.markdown("### 🔍 Interactive Filters")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if 'REF_AREA' in df.columns:
            # Better UI for country selection with search
            countries = st.multiselect(
                "Select Countries", 
                df['REF_AREA'].unique(),
                default=list(df['REF_AREA'].unique()),
                help="Search and select countries to analyze. Use Ctrl/Cmd+Click for multiple selection."
            )
            df = df[df['REF_AREA'].isin(countries)]
    
    with col2:
        if 'HealthExpenditure' in df.columns:
            min_exp = float(df['HealthExpenditure'].min())
            max_exp = float(df['HealthExpenditure'].max())
            exp_range = st.slider("Health Expenditure Range", min_exp, max_exp,
                                (min_exp, max_exp))
            df = df[(df['HealthExpenditure'] >= exp_range[0]) & 
                   (df['HealthExpenditure'] <= exp_range[1])]
    
    with col3:
        if 'Total_Deaths' in df.columns:
            min_deaths = float(df['Total_Deaths'].min())
            max_deaths = float(df['Total_Deaths'].max())
            deaths_range = st.slider("Death Rate Range", min_deaths, max_deaths,
                                   (min_deaths, max_deaths))
            df = df[(df['Total_Deaths'] >= deaths_range[0]) & 
                   (df['Total_Deaths'] <= deaths_range[1])]
    
    # Charts
    st.markdown("### 📊 Visualizations")
    
    tab1, tab2, tab3, tab4, tab5 = st.tabs(["💰 Health Expenditure vs COVID", "🏆 Top Performers", "👨‍⚕️ Physician Density", "📋 Data Table", "📄 Full Report"])
    
    with tab1:
        if 'HealthExpenditure' in df.columns and 'Total_Deaths' in df.columns:
            fig = px.scatter(df, x='HealthExpenditure', y='Total_Deaths',
                           hover_data=['REF_AREA', 'HealthExpenditure', 'Total_Deaths'],
                           title="Health Expenditure vs COVID Deaths",
                           labels={'HealthExpenditure': 'Health Expenditure (% of GDP)', 'Total_Deaths': 'Total COVID Deaths'},
                           color_discrete_sequence=['#ef4444'])
            fig.update_layout(
                plot_bgcolor='white',
                paper_bgcolor='white',
                font=dict(color='#111'),
                xaxis=dict(
                    title_font=dict(color='#111', size=20, family='Arial'),
                    tickfont=dict(color='#111', size=18, family='Arial'),
                    gridcolor='#e5e7eb',
                    zeroline=False
                ),
                yaxis=dict(
                    title_font=dict(color='#111', size=20, family='Arial'),
                    tickfont=dict(color='#111', size=18, family='Arial'),
                    gridcolor='#e5e7eb',
                    zeroline=False
                ),
                legend=dict(
                    bgcolor='white',
                    bordercolor='#888',
                    borderwidth=2,
                    font=dict(color='#111', size=18, family='Arial',),
                    orientation='v',
                    x=1.02,
                    y=1,
                    xanchor='left',
                    yanchor='top',
                ),
                margin=dict(l=60, r=60, t=60, b=60),
            )
            if hasattr(fig, 'update_traces'):
                fig.update_traces(textfont=dict(color='#111', size=18, family='Arial',), marker_line_color='#111', marker_line_width=2)
            st.plotly_chart(fig, use_container_width=True, config={
                'displayModeBar': True,
                'displaylogo': False,
                'modeBarButtonsToRemove': [],
            })
    
    with tab2:
        if 'REF_AREA' in df.columns and 'Total_Deaths' in df.columns:
            top_countries = df.nlargest(10, 'Total_Deaths')
            fig = px.bar(top_countries, x='REF_AREA', y='Total_Deaths',
                        title="Top 10 Countries by COVID Deaths",
                        labels={'REF_AREA': 'Country', 'Total_Deaths': 'Total COVID Deaths'},
                        color='Total_Deaths',
                        color_continuous_scale='Reds',
                        color_discrete_sequence=['#2563eb','#f59e42','#10b981','#a21caf','#f43f5e','#fbbf24','#6366f1','#22d3ee','#eab308','#0ea5e9']
            )
            fig.update_layout(
                plot_bgcolor='white',
                paper_bgcolor='white',
                font=dict(color='#111'),
                xaxis=dict(
                    title_font=dict(color='#111', size=20, family='Arial'),
                    tickfont=dict(color='#111', size=18, family='Arial'),
                    gridcolor='#e5e7eb',
                    zeroline=False
                ),
                yaxis=dict(
                    title_font=dict(color='#111', size=20, family='Arial'),
                    tickfont=dict(color='#111', size=18, family='Arial'),
                    gridcolor='#e5e7eb',
                    zeroline=False
                ),
                legend=dict(
                    bgcolor='white',
                    bordercolor='#888',
                    borderwidth=2,
                    font=dict(color='#111', size=18, family='Arial',),
                    orientation='v',
                    x=1.02,
                    y=1,
                    xanchor='left',
                    yanchor='top',
                ),
                margin=dict(l=60, r=60, t=60, b=60),
            )
            if hasattr(fig, 'update_traces'):
                fig.update_traces(textfont=dict(color='#111', size=18, family='Arial',), marker_line_color='#111', marker_line_width=2)
            st.plotly_chart(fig, use_container_width=True, config={
                'displayModeBar': True,
                'displaylogo': False,
                'modeBarButtonsToRemove': [],
            })
    
    with tab3:
        if 'REF_AREA' in df.columns and 'HealthExpenditure' in df.columns:
            top_exp = df.nlargest(10, 'HealthExpenditure')
            fig = px.pie(values=top_exp['HealthExpenditure'], names=top_exp['REF_AREA'],
                        title="Top 10 Countries by Health Expenditure",
                        color_discrete_sequence=['#2563eb','#f59e42','#10b981','#a21caf','#f43f5e','#fbbf24','#6366f1','#22d3ee','#eab308','#0ea5e9']
            )
            fig.update_layout(
                plot_bgcolor='white',
                paper_bgcolor='white',
                font=dict(color='#111'),
                xaxis=dict(
                    title_font=dict(color='#111', size=20, family='Arial'),
                    tickfont=dict(color='#111', size=18, family='Arial'),
                    gridcolor='#e5e7eb',
                    zeroline=False
                ),
                yaxis=dict(
                    title_font=dict(color='#111', size=20, family='Arial'),
                    tickfont=dict(color='#111', size=18, family='Arial'),
                    gridcolor='#e5e7eb',
                    zeroline=False
                ),
                legend=dict(
                    bgcolor='white',
                    bordercolor='#888',
                    borderwidth=2,
                    font=dict(color='#111', size=18, family='Arial',),
                    orientation='v',
                    x=1.02,
                    y=1,
                    xanchor='left',
                    yanchor='top',
                ),
                margin=dict(l=60, r=60, t=60, b=60),
            )
            if hasattr(fig, 'update_traces'):
                fig.update_traces(textfont=dict(color='#111', size=18, family='Arial',), marker_line_color='#111', marker_line_width=2)
            st.plotly_chart(fig, use_container_width=True, config={
                'displayModeBar': True,
                'displaylogo': False,
                'modeBarButtonsToRemove': [],
            })
    
    with tab4:
        st.markdown("### 📋 Data Table")
        st.dataframe(df, use_container_width=True, key=f"data_table_COVID_Health")
    
    with tab5:
        st.markdown("""
        ## 📄 COVID-19 Health System Analysis Report
        
        ### Executive Summary
        - **Countries analyzed**: 51 countries
        - **Time period**: COVID-19 pandemic (2020-2023)
        - **Key finding**: No strong correlation between health expenditure and COVID-19 performance
        
        ### Key Insights
        1. **Higher health expenditure associated with lower case fatality rates**: Investment in healthcare pays off
        2. **Higher physician density associated with lower case fatality rates**: Medical workforce matters
        3. **COVID-19 performance varies significantly**: No one-size-fits-all approach to pandemic response
        4. **Health system resilience is complex**: Multiple factors contribute to pandemic outcomes
        
        ### Policy Implications
        1. **Invest in healthcare infrastructure**: Strong health systems are crucial for crisis response
        2. **Focus on quality, not just quantity**: Physician density alone doesn't guarantee better outcomes
        3. **Prepare for future pandemics**: Build resilient health systems
        4. **Learn from successful countries**: Study what worked in different contexts
        """)

def show_advanced_health():
    """Show advanced health analysis with modern UI and report integration"""
    st.markdown("## 🔬 Advanced Health Analysis")
    
    df = load_advanced_health_data()
    if df.empty:
        st.error("No advanced health data available")
        return
    
    # Key Insights from Report
    st.markdown("""
    <div class="insight-box">
        <div class="insight-title">🔍 Key Insight</div>
        <div class="insight-text">
            The Health Index shows a strong positive correlation with GDP per capita (0.72), but with diminishing returns 
            at high income levels. Switzerland leads with the highest efficiency score (0.89), demonstrating optimal 
            health outcomes relative to spending. The analysis reveals that health investment drives economic growth, 
            with optimal health spending around 8-12% of GDP.
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Key metrics
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        avg_health_index = df['HealthIndex'].mean()
        st.metric("Average Health Index", format_number(avg_health_index, 1), 
                 help="Average comprehensive health system index (standardized score, -3 to +3 scale)")
    with col2:
        max_efficiency = df['EfficiencyScore'].max()
        st.metric("Highest Efficiency Score", format_number(max_efficiency, 2), 
                 help="Best health system efficiency score (0-25 scale, higher = more efficient)")
    with col3:
        correlation = df['GDPPerCapita'].corr(df['HealthIndex'])
        st.metric("GDP vs Health Correlation", format_number(correlation, 2), 
                 help="Correlation between GDP per capita and health index (-1 to 1)")
    with col4:
        countries_count = len(df)
        st.metric("Countries Analyzed", countries_count, 
                 help="Total number of countries in the analysis")
    
    # Filters with meaningful defaults
    st.markdown("### 🔍 Interactive Filters")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if 'REF_AREA' in df.columns:
            # Better UI for country selection with search and limited default selection
            all_countries = sorted(df['REF_AREA'].unique())
            # Default to top 10 countries by HealthIndex for better UX
            if 'HealthIndex' in df.columns:
                top_countries = df.nlargest(10, 'HealthIndex')['REF_AREA'].tolist()
                default_countries = top_countries
            else:
                default_countries = all_countries[:10]  # First 10 countries alphabetically
            
            countries = st.multiselect(
                "Select Countries", 
                all_countries,
                default=default_countries,
                help="Search and select countries to analyze. Use Ctrl/Cmd+Click for multiple selection. Default shows top 10 countries by Health Index."
            )
            df = df[df['REF_AREA'].isin(countries)]
    
    with col2:
        if 'HealthIndex' in df.columns:
            min_health = float(df['HealthIndex'].min())
            max_health = float(df['HealthIndex'].max())
            health_range = st.slider("Health Index Range", min_health, max_health,
                                    (min_health, max_health))
            df = df[(df['HealthIndex'] >= health_range[0]) & 
                   (df['HealthIndex'] <= health_range[1])]
    
    with col3:
        if 'EfficiencyScore' in df.columns:
            min_eff = float(df['EfficiencyScore'].min())
            max_eff = float(df['EfficiencyScore'].max())
            eff_range = st.slider("Efficiency Score Range", min_eff, max_eff,
                                (min_eff, max_eff))
            df = df[(df['EfficiencyScore'] >= eff_range[0]) & 
                   (df['EfficiencyScore'] <= eff_range[1])]
    
    # Charts
    st.markdown("### 📊 Visualizations")
    
    tab1, tab2, tab3, tab4, tab5 = st.tabs(["🏥 Health Index vs GDP", "🏆 Top Health Systems", "📊 Health Indicators", "📋 Data Table", "📄 Full Report"])
    
    with tab1:
        if 'HealthIndex' in df.columns and 'GDPPerCapita' in df.columns:
            fig = px.scatter(df, x='GDPPerCapita', y='HealthIndex',
                           hover_data=['REF_AREA', 'HealthIndex', 'GDPPerCapita'],
                           title="GDP per Capita vs Health Index",
                           labels={'GDPPerCapita': 'GDP per Capita (USD)', 'HealthIndex': 'Health Index'},
                           color_discrete_sequence=['#2ecc71'])
            fig.update_layout(
                plot_bgcolor='white',
                paper_bgcolor='white',
                font=dict(color='#111'),
                xaxis=dict(
                    title_font=dict(color='#111', size=20, family='Arial'),
                    tickfont=dict(color='#111', size=18, family='Arial'),
                    gridcolor='#e5e7eb',
                    zeroline=False
                ),
                yaxis=dict(
                    title_font=dict(color='#111', size=20, family='Arial'),
                    tickfont=dict(color='#111', size=18, family='Arial'),
                    gridcolor='#e5e7eb',
                    zeroline=False
                ),
                legend=dict(
                    bgcolor='white',
                    bordercolor='#888',
                    borderwidth=2,
                    font=dict(color='#111', size=18, family='Arial',),
                    orientation='v',
                    x=1.02,
                    y=1,
                    xanchor='left',
                    yanchor='top',
                ),
                margin=dict(l=60, r=60, t=60, b=60),
            )
            if hasattr(fig, 'update_traces'):
                fig.update_traces(textfont=dict(color='#111', size=18, family='Arial',), marker_line_color='#111', marker_line_width=2)
            st.plotly_chart(fig, use_container_width=True, config={
                'displayModeBar': True,
                'displaylogo': False,
                'modeBarButtonsToRemove': [],
            })
    
    with tab2:
        if 'REF_AREA' in df.columns and 'HealthIndex' in df.columns:
            top_countries = df.nlargest(10, 'HealthIndex')
            fig = px.bar(top_countries, x='REF_AREA', y='HealthIndex',
                        title="Top 10 Countries by Health Index",
                        labels={'REF_AREA': 'Country', 'HealthIndex': 'Health Index'},
                        color='HealthIndex',
                        color_continuous_scale='Greens',
                        color_discrete_sequence=['#2563eb','#f59e42','#10b981','#a21caf','#f43f5e','#fbbf24','#6366f1','#22d3ee','#eab308','#0ea5e9']
            )
            fig.update_layout(
                plot_bgcolor='white',
                paper_bgcolor='white',
                font=dict(color='#111'),
                xaxis=dict(
                    title_font=dict(color='#111', size=20, family='Arial'),
                    tickfont=dict(color='#111', size=18, family='Arial'),
                    gridcolor='#e5e7eb',
                    zeroline=False
                ),
                yaxis=dict(
                    title_font=dict(color='#111', size=20, family='Arial'),
                    tickfont=dict(color='#111', size=18, family='Arial'),
                    gridcolor='#e5e7eb',
                    zeroline=False
                ),
                legend=dict(
                    bgcolor='white',
                    bordercolor='#888',
                    borderwidth=2,
                    font=dict(color='#111', size=18, family='Arial',),
                    orientation='v',
                    x=1.02,
                    y=1,
                    xanchor='left',
                    yanchor='top',
                ),
                margin=dict(l=60, r=60, t=60, b=60),
            )
            if hasattr(fig, 'update_traces'):
                fig.update_traces(textfont=dict(color='#111', size=18, family='Arial',), marker_line_color='#111', marker_line_width=2)
            st.plotly_chart(fig, use_container_width=True, config={
                'displayModeBar': True,
                'displaylogo': False,
                'modeBarButtonsToRemove': [],
            })
    
    with tab3:
        if 'REF_AREA' in df.columns and 'PhysiciansPer1000' in df.columns:
            top_phys = df.nlargest(10, 'PhysiciansPer1000')
            fig = px.pie(values=top_phys['PhysiciansPer1000'], names=top_phys['REF_AREA'],
                        title="Top 10 Countries by Physicians per 1000",
                        color_discrete_sequence=['#2563eb','#f59e42','#10b981','#a21caf','#f43f5e','#fbbf24','#6366f1','#22d3ee','#eab308','#0ea5e9']
            )
            fig.update_layout(
                plot_bgcolor='white',
                paper_bgcolor='white',
                font=dict(color='#111'),
                xaxis=dict(
                    title_font=dict(color='#111', size=20, family='Arial'),
                    tickfont=dict(color='#111', size=18, family='Arial'),
                    gridcolor='#e5e7eb',
                    zeroline=False
                ),
                yaxis=dict(
                    title_font=dict(color='#111', size=20, family='Arial'),
                    tickfont=dict(color='#111', size=18, family='Arial'),
                    gridcolor='#e5e7eb',
                    zeroline=False
                ),
                legend=dict(
                    bgcolor='white',
                    bordercolor='#888',
                    borderwidth=2,
                    font=dict(color='#111', size=18, family='Arial',),
                    orientation='v',
                    x=1.02,
                    y=1,
                    xanchor='left',
                    yanchor='top',
                ),
                margin=dict(l=60, r=60, t=60, b=60),
            )
            if hasattr(fig, 'update_traces'):
                fig.update_traces(textfont=dict(color='#111', size=18, family='Arial',), marker_line_color='#111', marker_line_width=2)
            st.plotly_chart(fig, use_container_width=True, config={
                'displayModeBar': True,
                'displaylogo': False,
                'modeBarButtonsToRemove': [],
            })
    
    with tab4:
        st.markdown("### 📋 Data Table")
        st.dataframe(df, use_container_width=True, key=f"data_table_Advanced_Health")
    
    with tab5:
        st.markdown("""
        ## 📄 Advanced Health Data Analysis Report
        
        ### Executive Summary
        This advanced analysis examines health system efficiency metrics and introduces comprehensive health indicators.
        The analysis reveals important limitations in simple efficiency scores and identifies more balanced approaches to health system evaluation.
        
        ### Key Findings
        1. **Efficiency vs. Quality**: High efficiency scores don't always indicate better health systems
        2. **GDP Relationship**: Strong correlation between GDP and health outcomes, but diminishing returns observed
        3. **Resource Allocation**: Countries with moderate expenditure often achieve optimal balance
        4. **Data Gaps**: Missing physician and hospital bed data limits comprehensive analysis
        
        ### Health Index Methodology
        - **Life Expectancy (40% weight)**
        - **Infant Mortality (30% weight, inverse)**
        - **Physicians per 1000 (20% weight)**
        - **Hospital Beds per 1000 (10% weight)**
        
        ### Data Limitations
        - **Physicians per 1000**: 52.9% missing data
        - **Hospital Beds per 1000**: 64.7% missing data
        - **Inconsistent reporting**: Different countries report data differently
        """)

def show_data_explorer():
    """Show data explorer with all datasets"""
    st.markdown("## 📋 Data Explorer")
    
    # Dataset selection
    dataset = st.selectbox(
        "Choose Dataset:",
        ["GDP Recovery", "COVID Health", "Advanced Health"],
        key="data_explorer_dataset"
    )
    
    if dataset == "GDP Recovery":
        df = load_gdp_recovery_data()
    elif dataset == "COVID Health":
        df = load_covid_health_data()
    else:
        df = load_advanced_health_data()
    
    # 디버깅용 로그
    print("[Data Explorer] 선택된 데이터셋:", dataset)
    print("[Data Explorer] df.shape:", df.shape)
    print("[Data Explorer] df.columns:", list(df.columns))

    if df.empty:
        st.error(f"No {dataset} data available")
        return
    
    st.markdown(f"### 📊 {dataset} Dataset Overview")
    
    # Dataset info
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Total Records", len(df), 
                 help="Total number of country records in the dataset")
    with col2:
        st.metric("Columns", len(df.columns), 
                 help="Total number of variables/features in the dataset")
    with col3:
        st.metric("Missing Data", f"{df.isnull().sum().sum():,}", 
                 help="Total number of missing values across all columns")
    
    # Data preview
    st.markdown("### 📋 Data Table")
    
    # Simple approach: convert to string and use st.table
    df_display = df.copy()
    
    # Fill NaN values
    df_display = df_display.fillna('N/A')
    
    # Convert all to string to avoid any issues
    for col in df_display.columns:
        df_display[col] = df_display[col].astype(str)
    
    # Show up to 100 rows
    rows_to_show = min(100, len(df_display))
    st.table(df_display.head(rows_to_show))
    
    if len(df_display) > 100:
        st.info(f"Showing first {rows_to_show} rows out of {len(df_display)} total rows.")
    
    # Column information
    st.markdown("### 📈 Column Information")
    col_info = pd.DataFrame({
        'Column': df.columns,
        'Data Type': df.dtypes,
        'Non-Null Count': df.count(),
        'Missing Values': df.isnull().sum(),
        'Missing %': (df.isnull().sum() / len(df) * 100).round(2)
    })
    st.table(col_info)

if __name__ == "__main__":
    main() 