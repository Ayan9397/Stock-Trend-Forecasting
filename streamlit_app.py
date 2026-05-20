import streamlit as st

# Configure page
st.set_page_config(
    page_title="Stock Trend Forecasting",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ── Global CSS ──────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap');

/* ── Base ── */
html, body, [class*="css"] {
    font-family: 'Space Grotesk', sans-serif;
}

/* Dark background */
.stApp {
    background: #050a0f;
    background-image:
        radial-gradient(ellipse 80% 50% at 50% -20%, rgba(0,200,100,0.08) 0%, transparent 60%),
        radial-gradient(ellipse 60% 40% at 80% 80%, rgba(0,150,255,0.05) 0%, transparent 50%);
}

/* ── Sidebar ── */
[data-testid="stSidebar"] {
    background: #080e15 !important;
    border-right: 1px solid rgba(0,200,100,0.12);
}
[data-testid="stSidebar"] .stMarkdown p,
[data-testid="stSidebar"] label,
[data-testid="stSidebar"] span {
    color: #8899aa !important;
}
[data-testid="stSidebarNav"] a {
    color: #8899aa !important;
    font-size: 0.88rem;
    letter-spacing: 0.02em;
    padding: 0.45rem 0.75rem;
    border-radius: 6px;
    transition: all 0.2s;
}
[data-testid="stSidebarNav"] a:hover {
    color: #00c864 !important;
    background: rgba(0,200,100,0.07);
}
[data-testid="stSidebarNav"] a[aria-current="page"] {
    color: #00c864 !important;
    background: rgba(0,200,100,0.1);
    border-left: 2px solid #00c864;
}

/* ── Headings ── */
h1, h2, h3 {
    font-family: 'Space Grotesk', sans-serif !important;
    font-weight: 700 !important;
    letter-spacing: -0.02em;
}
h1 { color: #ffffff !important; font-size: 2rem !important; }
h2 { color: #e0eaf5 !important; font-size: 1.4rem !important; }
h3 { color: #a0b8d0 !important; font-size: 1.1rem !important; }

/* ── Metric cards ── */
[data-testid="stMetric"] {
    background: linear-gradient(135deg, #0d1520, #0a1018);
    border: 1px solid rgba(0,200,100,0.15);
    border-radius: 12px;
    padding: 1rem 1.25rem;
}
[data-testid="stMetricLabel"] { color: #5a7a9a !important; font-size: 0.78rem !important; text-transform: uppercase; letter-spacing: 0.08em; }
[data-testid="stMetricValue"] { color: #00c864 !important; font-size: 1.8rem !important; font-weight: 700; font-family: 'JetBrains Mono', monospace !important; }

/* ── Buttons ── */
.stButton > button {
    background: linear-gradient(135deg, #00c864, #00a050) !important;
    color: #000 !important;
    font-weight: 600 !important;
    border: none !important;
    border-radius: 8px !important;
    padding: 0.5rem 1.5rem !important;
    letter-spacing: 0.03em;
    transition: all 0.2s !important;
    box-shadow: 0 4px 20px rgba(0,200,100,0.25) !important;
}
.stButton > button:hover {
    transform: translateY(-1px) !important;
    box-shadow: 0 6px 28px rgba(0,200,100,0.4) !important;
}

/* ── Inputs ── */
.stTextInput > div > div > input,
.stSelectbox > div > div > div {
    background: #0d1520 !important;
    border: 1px solid rgba(0,200,100,0.2) !important;
    color: #c8dce8 !important;
    border-radius: 8px !important;
    font-family: 'JetBrains Mono', monospace !important;
    font-size: 0.9rem !important;
}
.stTextInput > div > div > input:focus {
    border-color: #00c864 !important;
    box-shadow: 0 0 0 2px rgba(0,200,100,0.15) !important;
}

/* ── Tabs ── */
.stTabs [data-baseweb="tab-list"] {
    background: #0a1018;
    border-radius: 10px;
    padding: 4px;
    gap: 4px;
    border: 1px solid rgba(255,255,255,0.05);
}
.stTabs [data-baseweb="tab"] {
    background: transparent;
    color: #5a7a9a;
    border-radius: 7px;
    font-weight: 500;
    padding: 0.4rem 1.2rem;
    transition: all 0.2s;
}
.stTabs [aria-selected="true"] {
    background: linear-gradient(135deg, #00c864, #00a050) !important;
    color: #000 !important;
}

/* ── Dataframe ── */
[data-testid="stDataFrame"] {
    border: 1px solid rgba(0,200,100,0.1);
    border-radius: 10px;
    overflow: hidden;
}

/* ── Alerts & info ── */
.stAlert {
    border-radius: 10px;
    border-left: 3px solid #00c864 !important;
    background: rgba(0,200,100,0.06) !important;
}

/* ── Spinner ── */
.stSpinner > div { border-top-color: #00c864 !important; }

/* ── Scrollbar ── */
::-webkit-scrollbar { width: 5px; height: 5px; }
::-webkit-scrollbar-track { background: #080e15; }
::-webkit-scrollbar-thumb { background: rgba(0,200,100,0.3); border-radius: 10px; }

/* ── Section divider ── */
hr { border-color: rgba(255,255,255,0.05) !important; }

/* General text */
p, li, .stMarkdown { color: #8899aa; }
</style>
""", unsafe_allow_html=True)

# ── Session state ────────────────────────────────────────────────────────────
if 'df' not in st.session_state:
    st.session_state.df = None
if 'stock_name' not in st.session_state:
    st.session_state.stock_name = "Stock"

# ── Pages ────────────────────────────────────────────────────────────────────
main_page        = st.Page("lib/main.py",          title="Data & Visualization",    icon="📊")
arima_page       = st.Page("lib/arima.py",         title="ARIMA",                   icon="📈")
sarima_page      = st.Page("lib/sarima.py",        title="SARIMA",                  icon="🔄")
lstm_page        = st.Page("lib/lstm.py",          title="LSTM",                    icon="🧠")
rnn_page         = st.Page("lib/rnn.py",           title="RNN",                     icon="🔗")
cnn_page         = st.Page("lib/cnn.py",           title="CNN",                     icon="🖼️")
gru_page         = st.Page("lib/gru.py",           title="GRU",                     icon="🌐")
lstm_gru_page    = st.Page("lib/lstm_gru.py",      title="LSTM-GRU",                icon="⚡")
prophet_page     = st.Page("lib/prophet_model.py", title="Prophet",                 icon="🔮")
lstm_cnn_rnn_page= st.Page("lib/lstm_cnn_rnn.py",  title="LSTM-CNN-RNN",            icon="🤖")

pg = st.navigation({
    "🏠 Home": [main_page],
    "📐 Classical Models": [arima_page, sarima_page],
    "🤖 Deep Learning": [lstm_page, gru_page, rnn_page, cnn_page],
    "⚡ Hybrid Models": [lstm_gru_page, lstm_cnn_rnn_page, prophet_page],
})

# ── Sidebar header ───────────────────────────────────────────────────────────
st.sidebar.markdown("""
<div style='padding: 1rem 0 1.5rem 0;'>
    <div style='display:flex; align-items:center; gap:10px; margin-bottom:4px;'>
        <span style='font-size:1.6rem;'>📈</span>
        <div>
            <div style='color:#ffffff; font-weight:700; font-size:1rem; letter-spacing:-0.01em;'>Stock Trend</div>
            <div style='color:#00c864; font-size:0.72rem; font-weight:500; letter-spacing:0.1em; text-transform:uppercase;'>Forecasting Platform</div>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

pg.run()

# ── Sidebar footer ───────────────────────────────────────────────────────────
st.sidebar.markdown("---")
st.sidebar.markdown("""
<div style='padding: 0.5rem 0; text-align:center;'>
    <div style='color:#ffffff; font-weight:600; font-size:0.9rem; margin-bottom:2px;'>Mohd Ayan</div>
    <div style='color:#5a7a9a; font-size:0.75rem; margin-bottom:10px;'>B.Tech CSE · BIET Lucknow</div>
    <div style='display:flex; justify-content:center; gap:12px; margin-bottom:8px;'>
        <a href='https://github.com/Ayan9397' target='_blank'
           style='color:#00c864; text-decoration:none; font-size:0.78rem; font-weight:500;'>⌥ GitHub</a>
        <a href='https://www.linkedin.com/in/mohd-ayan-39725b334' target='_blank'
           style='color:#00c864; text-decoration:none; font-size:0.78rem; font-weight:500;'>in LinkedIn</a>
    </div>
    <div style='color:#3a5a7a; font-size:0.72rem;'>mohdayan8896@gmail.com</div>
</div>
""", unsafe_allow_html=True)
