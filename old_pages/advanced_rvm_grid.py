import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import numpy as np
import subprocess
import json
import warnings
from datetime import datetime, timedelta
import logging
from typing import Dict, List, Optional, Any

# Suppress warnings
warnings.filterwarnings('ignore')

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class XTrillionClient:
    """Client for XTrillion service integration"""
    
    @staticmethod
    def get_data(command: str) -> Optional[Dict]:
        """Get data from XTrillion services"""
        try:
            result = subprocess.run(
                ['python3', '/app/xtrillion_wrapper.sh', command], 
                capture_output=True, 
                text=True,
                timeout=30
            )
            if result.returncode == 0 and result.stdout:
                return json.loads(result.stdout)
            return None
        except Exception as e:
            logger.error(f"XTrillion API error: {e}")
            return None
    
    @staticmethod
    def get_databases() -> List[str]:
        """Get available databases"""
        try:
            data = XTrillionClient.get_data("@dbase")
            if data and isinstance(data, dict):
                return data.get('databases', [])
            return []
        except Exception as e:
            logger.error(f"Database fetch error: {e}")
            return []
    
    @staticmethod
    def get_market_data(market: str = "us markets") -> Dict:
        """Get market data"""
        try:
            command = f"@{market}"
            data = XTrillionClient.get_data(command)
            return data if data else {}
        except Exception as e:
            logger.error(f"Market data error: {e}")
            return {}

class ThemeManager:
    """Manages dark theme configuration"""
    
    @staticmethod
    def apply_dark_theme():
        """Apply dark theme styling to Streamlit"""
        st.markdown("""
        <style>
        .stApp {
            background-color: #0e1117;
            color: #fafafa;
        }
        
        .stSidebar {
            background-color: #262730;
        }
        
        .stSelectbox label, .stSlider label, .stCheckbox label {
            color: #fafafa !important;
        }
        
        .stMetric {
            background-color: #262730;
            padding: 10px;
            border-radius: 5px;
            border: 1px solid #464646;
        }
        
        .stDataFrame {
            background-color: #262730;
        }
        
        .stMarkdown h1, .stMarkdown h2, .stMarkdown h3 {
            color: #00d4ff !important;
        }
        
        .plotly-graph-div {
            background-color: #0e1117 !important;
        }
        
        .stAlert {
            background-color: #262730;
            border: 1px solid #464646;
        }
        
        div[data-testid="stExpander"] {
            background-color: #262730;
            border: 1px solid #464646;
        }
        </style>
        """, unsafe_allow_html=True)
    
    @staticmethod
    def get_plotly_theme():
        """Get Plotly dark theme configuration"""
        return {
            'layout': {
                'plot_bgcolor': '#0e1117',
                'paper_bgcolor': '#0e1117',
                'font': {'color': '#fafafa'},
                'colorway': ['#00d4ff', '#ff6b6b', '#4ecdc4', '#45b7d1', '#96ceb4', '#feca57'],
                'xaxis': {
                    'gridcolor': '#464646',
                    'linecolor': '#464646',
                    'tickcolor': '#464646'
                },
                'yaxis': {
                    'gridcolor': '#464646',
                    'linecolor': '#464646',
                    'tickcolor': '#464646'
                }
            }
        }

class RVMDataGenerator:
    """Generates synthetic RVM (Risk-Value Matrix) grid data"""
    
    @staticmethod
    def generate_sample_data(rows: int = 50) -> pd.DataFrame:
        """Generate sample RVM data"""
        np.random.seed(42)
        
        assets = [f"Asset_{i:03d}" for i in range(1, rows + 1)]
        sectors = ['Technology', 'Healthcare', 'Finance', 'Energy', 'Consumer', 'Industrial']
        regions = ['North America', 'Europe', 'Asia Pacific', 'Emerging Markets']
        
        data = {
            'Asset': assets,
            'Sector': np.random.choice(sectors, rows),
            'Region': np.random.choice(regions, rows),
            'Risk_Score': np.random.normal(5, 2, rows).clip(1, 10),
            'Value_Score': np.random.normal(5, 2, rows).clip(1, 10),
            'Market_Cap': np.random.lognormal(10, 1.5, rows),
            'Beta': np.random.normal(1, 0.3, rows).clip(0.1, 2.5),
            'Volatility': np.random.normal(0.2, 0.1, rows).clip(0.05, 0.6),
            'Returns_1Y': np.random.normal(0.08, 0.15, rows),
            'ESG_Score': np.random.normal(7, 2, rows).clip(1, 10),
            'Liquidity_Score': np.random.normal(6, 2, rows).clip(1, 10)
        }
        
        df = pd.DataFrame(data)
        
        # Add quadrant classification
        df['Quadrant'] = df.apply(lambda row: 
            'High Risk/High Value' if row['Risk_Score'] > 6 and row['Value_Score'] > 6
            else 'High Risk/Low Value' if row['Risk_Score'] > 6 and row['Value_Score'] <= 6
            else 'Low Risk/High Value' if row['Risk_Score'] <= 6 and row['Value_Score'] > 6
            else 'Low Risk/Low Value', axis=1)
        
        return df

class GridVisualizer:
    """Creates RVM grid visualizations"""
    
    def __init__(self, theme_config: Dict):
        self.theme = theme_config
    
    def create_scatter_matrix(self, df: pd.DataFrame, color_by: str = 'Sector') -> go.Figure:
        """Create RVM scatter plot matrix"""
        try:
            fig = px.scatter(
                df, 
                x='Risk_Score', 
                y='Value_Score',
                color=color_by,
                size='Market_Cap',
                hover_data=['Asset', 'Beta', 'Volatility', 'Returns_1Y'],
                title='Risk-Value Matrix Grid',
                labels={'Risk_Score': 'Risk Score (1-10)', 'Value_Score': 'Value Score (1-10)'}
            )
            
            # Apply dark theme
            fig.update_layout(self.theme['layout'])
            fig.update_layout(
                title={'x': 0.5, 'font': {'size': 20}},
                width=800,
                height=600
            )
            
            # Add quadrant lines
            fig.add_hline(y=6, line_dash="dash", line_color="gray", opacity=0.5)
            fig.add_vline(x=6, line_dash="dash", line_color="gray", opacity=0.5)
            
            # Add quadrant labels
            fig.add_annotation(x=8, y=8, text="High Risk<br>High Value", 
                             showarrow=False, font=dict(size=12, color="lightgray"))
            fig.add_annotation(x=8, y=3, text="High Risk<br>Low Value", 
                             showarrow=False, font=dict(size=12, color="lightgray"))
            fig.add_annotation(x=3, y=8, text="Low Risk<br>High Value", 
                             showarrow=False, font=dict(size=12, color="lightgray"))
            fig.add_annotation(x=3, y=3, text="Low Risk<br>Low Value", 
                             showarrow=False, font=dict(size=12, color="lightgray"))
            
            return fig
        except Exception as e:
            logger.error(f"Scatter matrix creation error: {e}")
            return go.Figure()
    
    def create_heatmap(self, df: pd.DataFrame) -> go.Figure:
        """Create risk-value heatmap"""
        try:
            # Create bins for heatmap
            risk_bins = pd.cut(df['Risk_Score'], bins=10, labels=False)
            value_bins = pd.cut(df['Value_Score'], bins=10, labels=False)
            
            # Create heatmap data
            heatmap_data = np.zeros((10, 10))
            for r, v in zip(risk_bins, value_bins):
                if not (pd.isna(r) or pd.isna(v)):
                    heatmap_data[int(v), int(r)] += 1
            
            fig = go.Figure(data=go.Heatmap(
                z=heatmap_data,
                x=[f'R{i+1}' for i in range(10)],
                y=[f'V{i+1}' for i in range(10)],
                colorscale='Viridis',
                showscale=True
            ))
            
            fig.update_layout(
                title='Asset Distribution Heatmap',
                xaxis_title='Risk Score Bins',
                yaxis_title='Value Score Bins',
                **self.theme['layout']
            )
            
            return fig
        except Exception as e:
            logger.error(f"Heatmap creation error: {e}")
            return go.Figure()
    
    def create_3d_scatter(self, df: pd.DataFrame) -> go.Figure:
        """Create 3D scatter plot"""
        try:
            fig = go.Figure(data=go.Scatter3d(
                x=df['Risk_Score'],
                y=df['Value_Score'],
                z=df['ESG_Score'],
                mode='markers',
                marker=dict(
                    size=df['Market_Cap'] / df['Market_Cap'].max() * 20,
                    color=df['Returns_1Y'],
                    colorscale='Viridis',
                    showscale=True,
                    colorbar=dict(title="1Y Returns")
                ),
                text=df['Asset'],
                hovertemplate='<b>%{text}</b><br>' +
                             'Risk: %{x:.2f}<br>' +
                             'Value: %{y:.2f}<br>' +
                             'ESG: %{z:.2f}<br>' +
                             '<extra></extra>'
            ))
            
            fig.update_layout(
                title='3D Risk-Value-ESG Analysis',
                scene=dict(
                    xaxis_title='Risk Score',
                    yaxis_title='Value Score',
                    zaxis_title='ESG Score',
                    bgcolor='rgba(0,0,0,0)'
                ),
                **self.theme['layout']
            )
            
            return fig
        except Exception as e:
            logger.error(f"3D scatter creation error: {e}")
            return go.Figure()

class DashboardAnalytics:
    """Analytics and metrics for the dashboard"""
    
    @staticmethod
    def calculate_metrics(df: pd.DataFrame) -> Dict[str, Any]:
        """Calculate key metrics from RVM data"""
        try:
            metrics = {
                'total_assets': len(df),
                'avg_risk': df['Risk_Score'].mean(),
                'avg_value': df['Value_Score'].mean(),
                'high_value_assets': len(df[df['Value_Score'] > 7]),
                'low_risk_assets': len(df[df['Risk_Score'] < 4]),
                'optimal_assets': len(df[(df['Risk_Score'] < 4) & (df['Value_Score'] > 7)]),
                'avg_return': df['Returns_1Y'].mean(),
                'sharpe_ratio': df['Returns_1Y'].mean() / df['Volatility'].mean() if df['Volatility'].mean() > 0 else 0,
                'sectors': df['Sector'].nunique(),
                'regions': df['Region'].nunique()
            }
            return metrics
        except Exception as e:
            logger.error(f"Metrics calculation error: {e}")
            return {}
    
    @staticmethod
    def get_quadrant_analysis(df: pd.DataFrame) -> Dict[str, int]:
        """Analyze assets by quadrants"""
        try:
            return df['Quadrant'].value_counts().to_dict()
        except Exception as e:
            logger.error(f"Quadrant analysis error: {e}")
            return {}

def create_sidebar_controls():
    """Create sidebar controls"""
    st.sidebar.title("🎛️ Dashboard Controls")
    
    # Data controls
    st.sidebar.subheader("Data Settings")
    num_assets = st.sidebar.slider("Number of Assets", 20, 200, 50, 10)
    
    # Visualization controls
    st.sidebar.subheader("Visualization Settings")
    color_by = st.sidebar.selectbox(
        "Color By", 
        ['Sector', 'Region', 'Quadrant', 'ESG_Score'],
        index=0
    )
    
    show_3d = st.sidebar.checkbox("Show 3D Visualization", False)
    show_heatmap = st.sidebar.checkbox("Show Heatmap", True)
    
    # Filter controls
    st.sidebar.subheader("Filters")
    risk_range = st.sidebar.slider("Risk Score Range", 1.0, 10.0, (1.0, 10.0), 0.1)
    value_range = st.sidebar.slider("Value Score Range", 1.0, 10.0, (1.0, 10.0), 0.1)
    
    return {
        'num_assets': num_assets,
        'color_by': color_by,
        'show_3d': show_3d,
        'show_heatmap': show_heatmap,
        'risk_range': risk_range,
        'value_range': value_range
    }

def display_metrics(metrics: Dict[str, Any]):
    """Display key metrics"""
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total Assets", f"{metrics.get('total_assets', 0):,}")
        st.metric("Sectors", metrics.get('sectors', 0))
    
    with col2:
        st.metric("Avg Risk Score", f"{metrics.get('avg_risk', 0):.2f}")
        st.metric("Low Risk Assets", metrics.get('low_risk_assets', 0))
    
    with col3:
        st.metric("Avg Value Score", f"{metrics.get('avg_value', 0):.2f}")
        st