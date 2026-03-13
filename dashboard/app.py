import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import joblib
import time
from datetime import datetime

st.set_page_config(
    page_title="Executive Sales Hub",
    layout="wide",
)

MAIN_BG = "#f0f2f6"
CARD_BG = "#ffffff"
PRIMARY_BLUE = "#007bff"
TEXT_COLOR = "#2c3e50"
SIDEBAR_COLOR = "#1e293b"

st.markdown(f"""
    <style>
    .stApp {{
        background-color: {MAIN_BG};
    }}
    [data-testid="stSidebar"] {{
        background-color: {SIDEBAR_COLOR};
    }}
    [data-testid="stSidebar"] * {{
        color: white !important;
    }}
    .main-header-box {{
        background: linear-gradient(90deg, #1e3a8a 0%, #3b82f6 100%);
        padding: 30px;
        border-radius: 15px;
        color: white;
        text-align: center;
        margin-bottom: 25px;
        box-shadow: 0 10px 20px rgba(0,0,0,0.1);
    }}
    .main-header-box h1 {{
        color: white !important;
        margin: 0;
        font-size: 36px;
        font-weight: 800;
    }}
    .main-header-box p {{
        margin-top: 10px;
        font-size: 16px;
        opacity: 0.9;
    }}
    .metric-card {{
        background-color: white;
        padding: 20px;
        border-radius: 12px;
        box-shadow: 0 4px 10px rgba(0,0,0,0.05);
        border-bottom: 4px solid {PRIMARY_BLUE};
        text-align: center;
    }}
    .metric-label {{
        font-size: 15px;
        color: #666;
        font-weight: 500;
    }}
    .metric-value {{
        font-size: 28px;
        font-weight: 800;
        margin-top: 8px;
    }}
    .stPlotlyChart {{
        background-color: {CARD_BG};
        border-radius: 15px;
        padding: 15px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.08);
    }}
    .stButton > button {{
        width: 100%;
        border-radius: 10px;
        border: none;
        background-color: {PRIMARY_BLUE};
        color: white;
        font-weight: bold;
        transition: 0.3s;
    }}
    .stButton > button:hover {{
        opacity: 0.8;
        transform: translateY(-2px);
    }}
    h1, h2, h3 {{
        color: {TEXT_COLOR};
        font-family: 'Inter', sans-serif;
    }}
    </style>
    """, unsafe_allow_html=True)

def make_card_style(fig):
    fig.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        margin=dict(l=10, r=10, t=40, b=10),
        font=dict(color=TEXT_COLOR)
    )
    return fig

@st.cache_data
def load_data():
    try:
        df = pd.read_csv("data/superstore.csv", encoding="latin-1")
        df['Order Date'] = pd.to_datetime(df['Order Date'])
        return df
    except:
        return pd.DataFrame()

df = load_data()

with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/3081/3081559.png", width=60)
    st.title("Business Panel")
    region = st.multiselect("Region", df["Region"].unique(), default=df["Region"].unique())
    category = st.multiselect("Category", df["Category"].unique(), default=df["Category"].unique())
    st.divider()
    st.caption("v3.2 Premium Edition")

filtered_df = df[df["Region"].isin(region) & df["Category"].isin(category)]

st.markdown("""
    <div class="main-header-box">
        <h1>E-Commerce Strategic Hub</h1>
        <p>Real-time data visualization with predictive intelligence</p>
    </div>
    """, unsafe_allow_html=True)

k1, k2, k3, k4 = st.columns(4)
total_sales = filtered_df['Sales'].sum() if not filtered_df.empty else 0
total_profit = filtered_df['Profit'].sum() if not filtered_df.empty else 0

with k1:
    st.markdown(f'<div class="metric-card"><div class="metric-label">Gross Revenue</div><div class="metric-value" style="color: #1e3a8a;">${total_sales:,.0f}</div></div>', unsafe_allow_html=True)
with k2:
    st.markdown(f'<div class="metric-card"><div class="metric-label">Net Profit</div><div class="metric-value" style="color: #10b981;">${total_profit:,.0f}</div></div>', unsafe_allow_html=True)
with k3:
    st.markdown(f'<div class="metric-card"><div class="metric-label">Order Volume</div><div class="metric-value" style="color: #1e293b;">{filtered_df["Order ID"].nunique() if not filtered_df.empty else 0:,}</div></div>', unsafe_allow_html=True)
with k4:
    st.markdown(f'<div class="metric-card"><div class="metric-label">Growth Status</div><div class="metric-value" style="color: #3b82f6;">Stable <span style="font-size: 14px;">+2.4%</span></div></div>', unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

col1, col2 = st.columns([1.6, 1])

with col1:
    st.subheader("Revenue Trend")
    line_data = filtered_df.set_index('Order Date').resample('M')['Sales'].sum().reset_index()
    fig_line = px.area(line_data, x='Order Date', y='Sales', color_discrete_sequence=[PRIMARY_BLUE])
    st.plotly_chart(make_card_style(fig_line), use_container_width=True)

with col2:
    st.subheader("Segment Split")
    fig_pie = px.pie(filtered_df, values='Sales', names='Segment', hole=0.7, color_discrete_sequence=px.colors.qualitative.Pastel)
    st.plotly_chart(make_card_style(fig_pie), use_container_width=True)

col3, col4 = st.columns(2)

with col3:
    st.subheader("Sub-Category Sales")
    sub_cat = filtered_df.groupby("Sub-Category")["Sales"].sum().sort_values(ascending=True).reset_index()
    fig_bar = px.bar(sub_cat, x='Sales', y='Sub-Category', orientation='h', color='Sales', color_continuous_scale='Blues')
    st.plotly_chart(make_card_style(fig_bar), use_container_width=True)

with col4:
    st.subheader("Profitability Matrix")
    fig_scatter = px.scatter(filtered_df, x="Discount", y="Profit", size="Sales", color="Category", opacity=0.6)
    st.plotly_chart(make_card_style(fig_scatter), use_container_width=True)

st.divider()
st.subheader("Forecasting Engine")

f_col1, f_col2 = st.columns([1, 2.5])

with f_col1:
    st.write("Calculate next month's estimated performance.")
    predict_btn = st.button("Generate Forecast", type="primary")

with f_col2:
    placeholder = st.empty()
    
    if not predict_btn:
        fig_init = go.Figure(go.Indicator(
            mode="gauge+number", 
            value=0, 
            title={'text': "Awaiting Input...", 'font': {'size': 18, 'color': 'gray'}}
        ))
        fig_init.update_layout(height=280, paper_bgcolor='rgba(0,0,0,0)', margin=dict(t=50, b=20))
        placeholder.plotly_chart(fig_init, use_container_width=True, key="init_chart")
    
    else:
        target_val = 292700 
        try:
            model = joblib.load("model/revenue_model.pkl")
            last_date = df['Order Date'].max()
            next_date = last_date + pd.DateOffset(months=1)
            target_val = model.predict([[next_date.year, next_date.month]])[0]
        except: pass

        steps = 40
        for i in range(steps + 1):
            current_val = (target_val / steps) * i
            
            fig_gauge = go.Figure(go.Indicator(
                mode = "gauge+number",
                value = current_val,
                number = {'prefix': "$", 'valueformat': ",.0f", 'font': {'size': 40}},
                title = {'text': "Projected Revenue", 'font': {'size': 20}},
                gauge = {
                    'axis': {'range': [0, target_val * 1.2], 'tickwidth': 1},
                    'bar': {'color': PRIMARY_BLUE},
                    'bgcolor': "#f1f1f1",
                    'borderwidth': 0,
                }
            ))
            
            fig_gauge.update_layout(
                height=300, 
                paper_bgcolor='rgba(0,0,0,0)', 
                margin=dict(t=50, b=20),
                datarevision=i
            )
            
            placeholder.plotly_chart(fig_gauge, use_container_width=True, key=f"anim_{i}")
            time.sleep(0.01)            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
