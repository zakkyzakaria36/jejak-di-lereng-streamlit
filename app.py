import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime
import requests
from io import BytesIO
import qrcode

# ============================================================================
# PAGE CONFIG & THEME
# ============================================================================

st.set_page_config(
    page_title="Jejak di Lereng",
    page_icon="🏔️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Antigravity Theme - Dark + Gradient
st.markdown("""
<style>
    * {
        margin: 0;
        padding: 0;
    }
    
    body, .main {
        background: linear-gradient(135deg, #0a0e1a 0%, #1a1f3a 100%);
        color: #e0e6ff;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }
    
    .stApp {
        background: linear-gradient(135deg, #0a0e1a 0%, #1a1f3a 100%);
    }
    
    /* Header */
    .header-container {
        background: linear-gradient(90deg, rgba(255,107,107,0.1) 0%, rgba(168,85,247,0.1) 100%);
        border-bottom: 2px solid rgba(255,107,107,0.3);
        padding: 2rem;
        margin-bottom: 2rem;
        border-radius: 15px;
        backdrop-filter: blur(10px);
    }
    
    .header-title {
        font-size: 3rem;
        font-weight: 900;
        background: linear-gradient(90deg, #FF6B6B, #A855F7);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        margin: 0;
    }
    
    .header-subtitle {
        color: #b0b8d4;
        font-size: 1.1rem;
        margin-top: 0.5rem;
    }
    
    /* Cards */
    .metric-card {
        background: linear-gradient(135deg, rgba(255,107,107,0.1) 0%, rgba(168,85,247,0.05) 100%);
        border: 1px solid rgba(255,107,107,0.2);
        border-radius: 12px;
        padding: 1.5rem;
        margin: 0.5rem 0;
        backdrop-filter: blur(10px);
        transition: all 0.3s ease;
    }
    
    .metric-card:hover {
        border-color: rgba(255,107,107,0.5);
        box-shadow: 0 8px 32px rgba(255,107,107,0.1);
        transform: translateY(-2px);
    }
    
    .metric-value {
        font-size: 2.5rem;
        font-weight: 900;
        color: #FF6B6B;
        margin: 0.5rem 0;
    }
    
    .metric-label {
        color: #b0b8d4;
        font-size: 0.9rem;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    
    /* Chart Container */
    .chart-container {
        background: linear-gradient(135deg, rgba(30,35,60,0.5) 0%, rgba(50,55,90,0.3) 100%);
        border: 1px solid rgba(255,107,107,0.15);
        border-radius: 15px;
        padding: 1.5rem;
        margin: 1rem 0;
        backdrop-filter: blur(10px);
    }
    
    /* Tabs */
    .stTabs [data-baseweb="tab-list"] {
        border-bottom: 2px solid rgba(255,107,107,0.2);
    }
    
    .stTabs [data-baseweb="tab"] {
        color: #b0b8d4;
        border-radius: 8px 8px 0 0;
    }
    
    .stTabs [aria-selected="true"] {
        color: #FF6B6B;
        border-bottom: 3px solid #FF6B6B;
    }
    
    /* Button */
    .stButton > button {
        background: linear-gradient(90deg, #FF6B6B, #A855F7);
        color: white;
        border: none;
        border-radius: 8px;
        padding: 0.75rem 1.5rem;
        font-weight: 600;
        transition: all 0.3s ease;
    }
    
    .stButton > button:hover {
        box-shadow: 0 8px 24px rgba(255,107,107,0.3);
        transform: translateY(-2px);
    }
    
    /* Text */
    h1, h2, h3 {
        color: #e0e6ff;
    }
    
    p {
        color: #b0b8d4;
    }
</style>
""", unsafe_allow_html=True)

# ============================================================================
# DATA LOADING
# ============================================================================

@st.cache_data
def load_data():
    """Load CSV data dari folder /data"""
    data = {
        'choropleth': pd.DataFrame({
            'Wilayah': ['Kulon Progo', 'Sleman', 'Gunungkidul', 'Bantul', 'Kota Yogyakarta'],
            'Kejadian': [41, 25, 22, 13, 11],
            'Persentase': [36.6, 22.3, 19.6, 11.6, 9.8],
            'Warna': ['#d62728', '#ff7f0e', '#2ca02c', '#1f77b4', '#9467bd']
        }),
        'temporal': pd.DataFrame({
            'Bulan': ['Jan', 'Feb', 'Mar', 'Apr', 'Mei', 'Jun', 'Jul', 'Agu', 'Sep', 'Okt', 'Nov', 'Des'],
            'Kejadian': [9, 17, 13, 4, 1, 1, 1, 1, 4, 11, 16, 17],
            'Musim': ['Hujan', 'Hujan', 'Hujan', 'Kemarau', 'Kemarau', 'Kemarau', 
                     'Kemarau', 'Kemarau', 'Kemarau', 'Hujan', 'Hujan', 'Hujan']
        }),
        'tahunan': pd.DataFrame({
            'Tahun': list(range(2016, 2027)),
            'Kejadian': [4, 8, 12, 20, 15, 24, 11, 9, 8, 6, 0],
            'Highlight': ['No', 'No', 'No', 'No', 'Yes', 'No', 'No', 'No', 'No', 'No', 'No']
        }),
        'dampak': pd.DataFrame({
            'Kategori': ['Mengungsi', 'Rumah Rusak', 'Terluka', 'Meninggal'],
            'Jumlah': [11141, 268, 25, 20],
            'Persentase': [97.3, 2.3, 0.2, 0.2]
        }),
        'statistics': {
            'total_kejadian': 112,
            'hotspot': 'Kulon Progo',
            'hotspot_value': 41,
            'musim_hujan': 96,
            'puncak_tahun': 2021,
            'puncak_value': 24,
            'fatality_rate_post_2020': '0%'
        }
    }
    return data

data = load_data()

# ============================================================================
# HEADER
# ============================================================================

st.markdown("""
<div class="header-container">
    <h1 class="header-title">🏔️ Jejak di Lereng</h1>
    <p class="header-subtitle">Analisis Spasio-Temporal Longsor DIY (2016-2026)</p>
</div>
""", unsafe_allow_html=True)

# ============================================================================
# NAVIGATION TABS
# ============================================================================

tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "📊 Dashboard Utama",
    "🗺️ Analisis Spasial",
    "📈 Analisis Temporal",
    "⚠️ Dampak & Mitigasi",
    "📥 Data & Download"
])

# ============================================================================
# TAB 1: DASHBOARD UTAMA
# ============================================================================

with tab1:
    st.markdown("### Ringkasan Utama")
    
    col1, col2, col3, col4, col5 = st.columns(5)
    
    with col1:
        st.markdown("""
        <div class="metric-card">
            <div class="metric-label">Total Kejadian</div>
            <div class="metric-value">112</div>
            <div class="metric-label" style="color: #FF6B6B; margin-top: 0.5rem;">2016-2026</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="metric-card">
            <div class="metric-label">Hotspot</div>
            <div class="metric-value">41</div>
            <div class="metric-label" style="color: #FF6B6B; margin-top: 0.5rem;">Kulon Progo</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="metric-card">
            <div class="metric-label">Musim Hujan</div>
            <div class="metric-value">96</div>
            <div class="metric-label" style="color: #FF6B6B; margin-top: 0.5rem;">86% total</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown("""
        <div class="metric-card">
            <div class="metric-label">Puncak Tertinggi</div>
            <div class="metric-value">24</div>
            <div class="metric-label" style="color: #FF6B6B; margin-top: 0.5rem;">Tahun 2021</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col5:
        st.markdown("""
        <div class="metric-card">
            <div class="metric-label">Fatality (2020-2026)</div>
            <div class="metric-value">0</div>
            <div class="metric-label" style="color: #2ecc71; margin-top: 0.5rem;">Hasil Mitigasi</div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.info("""
        **Temuan 1: Hotspot Geografis**
        
        Kulon Progo mencatat 41 kejadian (36.6% dari total), menjadi wilayah dengan risiko tertinggi.
        """)
    
    with col2:
        st.success("""
        **Temuan 2: Dampak Mitigasi**
        
        Sejak 2020, fatality rate turun ke 0% (sebelumnya 45.5%).
        """)

# ============================================================================
# TAB 2: ANALISIS SPASIAL
# ============================================================================

with tab2:
    st.markdown("### Distribusi Wilayah")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        fig_bar = go.Figure(data=[
            go.Bar(
                x=data['choropleth']['Wilayah'],
                y=data['choropleth']['Kejadian'],
                marker=dict(color=data['choropleth']['Warna']),
                text=data['choropleth']['Kejadian'],
                textposition='auto'
            )
        ])
        
        fig_bar.update_layout(
            title="Jumlah Kejadian per Wilayah",
            template="plotly_dark",
            paper_bgcolor='rgba(10, 14, 26, 0)',
            plot_bgcolor='rgba(30, 35, 60, 0.2)',
            font=dict(color='#e0e6ff'),
            height=400
        )
        
        st.plotly_chart(fig_bar, use_container_width=True)
    
    with col2:
        st.markdown("#### Persentase")
        for idx, row in data['choropleth'].iterrows():
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-label">{row['Wilayah']}</div>
                <div class="metric-value" style="color: {row['Warna']};">{row['Persentase']:.1f}%</div>
            </div>
            """, unsafe_allow_html=True)

# ============================================================================
# TAB 3: ANALISIS TEMPORAL
# ============================================================================

with tab3:
    st.markdown("### Pola Temporal & Musiman")
    
    fig_line = go.Figure()
    
    fig_line.add_trace(go.Scatter(
        x=data['temporal']['Bulan'],
        y=data['temporal']['Kejadian'],
        mode='lines+markers',
        name='Kejadian',
        line=dict(color='#FF6B6B', width=3),
        marker=dict(size=10),
        fill='tozeroy',
        fillcolor='rgba(255, 107, 107, 0.2)'
    ))
    
    fig_line.update_layout(
        title="Pola Bulanan Longsor (10 Tahun)",
        template="plotly_dark",
        paper_bgcolor='rgba(10, 14, 26, 0)',
        plot_bgcolor='rgba(30, 35, 60, 0.2)',
        font=dict(color='#e0e6ff'),
        height=400
    )
    
    st.plotly_chart(fig_line, use_container_width=True)
    
    st.markdown("---")
    st.markdown("### Trend Tahunan")
    
    fig_bar_tahunan = go.Figure()
    
    colors = ['#A855F7' if h == 'No' else '#FF6B6B' for h in data['tahunan']['Highlight']]
    
    fig_bar_tahunan.add_trace(go.Bar(
        x=data['tahunan']['Tahun'],
        y=data['tahunan']['Kejadian'],
        marker=dict(color=colors),
        text=data['tahunan']['Kejadian'],
        textposition='auto'
    ))
    
    fig_bar_tahunan.update_layout(
        title="Trend Kejadian per Tahun (2016-2026)",
        template="plotly_dark",
        paper_bgcolor='rgba(10, 14, 26, 0)',
        plot_bgcolor='rgba(30, 35, 60, 0.2)',
        font=dict(color='#e0e6ff'),
        height=400
    )
    
    st.plotly_chart(fig_bar_tahunan, use_container_width=True)

# ============================================================================
# TAB 4: DAMPAK & MITIGASI
# ============================================================================

with tab4:
    st.markdown("### Dampak Longsor (2016-2026)")
    
    col1, col2 = st.columns([1.5, 1])
    
    with col1:
        fig_donut = go.Figure(data=[go.Pie(
            labels=data['dampak']['Kategori'],
            values=data['dampak']['Jumlah'],
            hole=0.4,
            marker=dict(colors=['#FF6B6B', '#A855F7', '#3B82F6', '#1abc9c']),
            textposition='inside',
            textinfo='label+percent'
        )])
        
        fig_donut.update_layout(
            template="plotly_dark",
            paper_bgcolor='rgba(10, 14, 26, 0)',
            font=dict(color='#e0e6ff'),
            height=400,
            title="Breakdown Dampak"
        )
        
        st.plotly_chart(fig_donut, use_container_width=True)
    
    with col2:
        st.markdown("#### Detail Dampak")
        for idx, row in data['dampak'].iterrows():
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-label">{row['Kategori']}</div>
                <div class="metric-value">{row['Jumlah']:,}</div>
            </div>
            """, unsafe_allow_html=True)
    
    st.markdown("---")
    st.markdown("### Program Mitigasi")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div class="metric-card">
            <div class="metric-label">SMS Warning</div>
            <div class="metric-value">15K</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="metric-card">
            <div class="metric-label">Relokasi</div>
            <div class="metric-value">2.5K</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="metric-card">
            <div class="metric-label">Walls</div>
            <div class="metric-value">45</div>
        </div>
        """, unsafe_allow_html=True)

# ============================================================================
# TAB 5: DATA & DOWNLOAD
# ============================================================================

with tab5:
    st.markdown("### Data & Export")
    
    dataset_choice = st.selectbox(
        "Pilih data yang ingin diunduh:",
        ["Ringkasan Wilayah", "Data Temporal", "Dampak"]
    )
    
    if dataset_choice == "Ringkasan Wilayah":
        df_export = data['choropleth']
        filename = "jejak_wilayah.csv"
    elif dataset_choice == "Data Temporal":
        df_export = data['temporal']
        filename = "jejak_temporal.csv"
    else:
        df_export = data['dampak']
        filename = "jejak_dampak.csv"
    
    csv = df_export.to_csv(index=False)
    st.download_button(
        label="📥 Download CSV",
        data=csv,
        file_name=filename,
        mime="text/csv"
    )
    
    st.dataframe(df_export, use_container_width=True)

st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #b0b8d4; font-size: 0.9rem;">
    <p>🏔️ Jejak di Lereng | Longsor DIY 2016-2026</p>
</div>
""", unsafe_allow_html=True)
