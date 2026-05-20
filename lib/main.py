import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import yfinance as yf

# ── Page hero ────────────────────────────────────────────────────────────────
st.markdown("""
<div style='padding: 2rem 0 1rem 0;'>
    <h1 style='margin:0; font-size:2.2rem; background: linear-gradient(135deg,#ffffff,#00c864);
               -webkit-background-clip:text; -webkit-text-fill-color:transparent;'>
        Stock Data & Visualization
    </h1>
    <p style='color:#5a7a9a; margin-top:0.4rem; font-size:0.95rem;'>
        Upload a CSV or pull live data from Yahoo Finance to begin forecasting.
    </p>
</div>
""", unsafe_allow_html=True)

REQUIRED_COLUMNS = ['Open', 'High', 'Low', 'Close', 'Volume']

PLOTLY_THEME = dict(
    paper_bgcolor='rgba(0,0,0,0)',
    plot_bgcolor='rgba(0,0,0,0)',
    font=dict(family='Space Grotesk, sans-serif', color='#8899aa'),
    xaxis=dict(gridcolor='rgba(255,255,255,0.04)', linecolor='rgba(255,255,255,0.08)'),
    yaxis=dict(gridcolor='rgba(255,255,255,0.04)', linecolor='rgba(255,255,255,0.08)'),
    legend=dict(bgcolor='rgba(0,0,0,0)', bordercolor='rgba(255,255,255,0.08)'),
    margin=dict(l=10, r=10, t=40, b=10),
)

tab1, tab2 = st.tabs(["📁  Upload CSV", "📡  Yahoo Finance"])

# ── Tab 2 — Yahoo Finance ────────────────────────────────────────────────────
with tab2:
    st.markdown("<div style='height:0.75rem'></div>", unsafe_allow_html=True)
    col1, col2 = st.columns([2, 2])
    with col1:
        stock_symbol = st.text_input("Ticker Symbol", value="AAPL", placeholder="e.g. AAPL, MSFT, TSLA")
    with col2:
        period_options = {"1 Month":"1mo","3 Months":"3mo","6 Months":"6mo",
                          "1 Year":"1y","2 Years":"2y","5 Years":"5y","10 Years":"10y","Max":"max"}
        selected_period = st.selectbox("Time Period", list(period_options.keys()), index=3)

    if st.button("Fetch Data", type="primary", key="fetch_yf"):
        if stock_symbol:
            with st.spinner(f"Fetching {stock_symbol.upper()} from Yahoo Finance…"):
                try:
                    ticker = yf.Ticker(stock_symbol.upper())
                    df = ticker.history(period=period_options[selected_period])
                    if df.empty:
                        st.error(f"No data found for '{stock_symbol.upper()}'. Check the ticker symbol.")
                    else:
                        df = df.reset_index()[['Date'] + REQUIRED_COLUMNS]
                        df['Date'] = pd.to_datetime(df['Date']).dt.date
                        df['Date'] = pd.to_datetime(df['Date'])
                        df = df.set_index('Date').sort_index()
                        st.session_state.df = df
                        st.session_state.stock_name = stock_symbol.upper()
                        st.success(f"✅ Loaded **{len(df):,}** rows for **{stock_symbol.upper()}**")
                except Exception as e:
                    st.error(f"Error: {e}")

# ── Tab 1 — CSV Upload ───────────────────────────────────────────────────────
with tab1:
    st.markdown("<div style='height:0.75rem'></div>", unsafe_allow_html=True)
    file = st.file_uploader("Drop your CSV here", type=["csv", "txt"])
    if st.button("Load File", type="primary", key="fetch_csv"):
        if file:
            try:
                df = pd.read_csv(file).reset_index()
                df = df[['Date'] + [c for c in REQUIRED_COLUMNS if c in df.columns]]
                df['Date'] = pd.to_datetime(df['Date']).dt.date
                df['Date'] = pd.to_datetime(df['Date'])
                df = df.set_index('Date').sort_index()
                st.session_state.df = df
                st.session_state.stock_name = "Stock"
                st.success(f"✅ Loaded **{len(df):,}** rows from file.")
            except Exception as e:
                st.error(f"Error: {e}")
        else:
            st.warning("Please select a CSV file first.")

# ── Dashboard ────────────────────────────────────────────────────────────────
if st.session_state.df is not None:
    df = st.session_state.df

    st.markdown("<div style='height:1.5rem'></div>", unsafe_allow_html=True)
    st.markdown("### 📊 Dataset Overview")

    # KPI row
    k1, k2, k3, k4, k5 = st.columns(5)
    k1.metric("Rows", f"{len(df):,}")
    k2.metric("Columns", len(df.columns))
    k3.metric("From", df.index.min().strftime('%b %Y'))
    k4.metric("To", df.index.max().strftime('%b %Y'))
    if 'Close' in df.columns:
        pct = ((df['Close'].iloc[-1] - df['Close'].iloc[0]) / df['Close'].iloc[0]) * 100
        k5.metric("Total Return", f"{pct:+.1f}%")

    st.markdown("<div style='height:1rem'></div>", unsafe_allow_html=True)
    with st.expander("🔍 Preview Data (first 10 rows)"):
        st.dataframe(df.head(10), use_container_width=True)

    if 'Close' not in df.columns:
        st.error("Missing 'Close' column — required for all models.")
        st.stop()

    st.session_state.stock_name = st.text_input(
        "Stock display name", value=st.session_state.stock_name)

    name = st.session_state.stock_name
    plot_df = df.reset_index()
    x_col = 'Date' if 'Date' in plot_df.columns else plot_df.columns[0]

    st.markdown("<div style='height:1rem'></div>", unsafe_allow_html=True)

    # ── Closing price ──────────────────────────────────────────────────────
    st.markdown("#### 💹 Closing Price")
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=plot_df[x_col], y=plot_df['Close'],
        mode='lines', name='Close',
        line=dict(color='#00c864', width=1.8),
        fill='tozeroy',
        fillcolor='rgba(0,200,100,0.06)'
    ))
    fig.update_layout(title=f"{name} — Closing Price", height=360, **PLOTLY_THEME)
    st.plotly_chart(fig, use_container_width=True)

    # ── OHLC ──────────────────────────────────────────────────────────────
    ohlc_cols = [c for c in ['Open','High','Low','Close'] if c in df.columns]
    if len(ohlc_cols) >= 2:
        st.markdown("#### 📊 OHLC Prices")
        colors = ['#4a9eff','#00c864','#ff4a6e','#ffd84a']
        fig2 = go.Figure()
        for col, clr in zip(ohlc_cols, colors):
            fig2.add_trace(go.Scatter(x=plot_df[x_col], y=plot_df[col],
                                      mode='lines', name=col,
                                      line=dict(color=clr, width=1.4)))
        fig2.update_layout(title=f"{name} — OHLC", height=360, **PLOTLY_THEME)
        st.plotly_chart(fig2, use_container_width=True)

    # ── Volume ────────────────────────────────────────────────────────────
    if 'Volume' in df.columns:
        st.markdown("#### 📦 Trading Volume")
        fig3 = go.Figure()
        fig3.add_trace(go.Bar(
            x=plot_df[x_col], y=plot_df['Volume'],
            marker_color='rgba(74,158,255,0.55)',
            marker_line_width=0,
            name='Volume'
        ))
        fig3.update_layout(title=f"{name} — Volume", height=300, **PLOTLY_THEME)
        st.plotly_chart(fig3, use_container_width=True)

    # ── Rolling means ─────────────────────────────────────────────────────
    st.markdown("#### 📉 Moving Averages")
    rx = df.copy()
    windows = {'7d':'#ffd84a','20d':'#4a9eff','30d':'#ff4a6e'}
    fig4 = go.Figure()
    fig4.add_trace(go.Scatter(x=rx.index, y=rx['Close'], mode='lines',
                              name='Close', line=dict(color='rgba(255,255,255,0.2)', width=1)))
    for label, clr in windows.items():
        rx[label] = rx['Close'].rolling(int(label[:-1])).mean()
        fig4.add_trace(go.Scatter(x=rx.index, y=rx[label], mode='lines',
                                  name=f"{label} MA", line=dict(color=clr, width=1.8)))
    fig4.update_layout(title=f"{name} — Moving Averages", height=360, **PLOTLY_THEME)
    st.plotly_chart(fig4, use_container_width=True)

    # ── Stats ─────────────────────────────────────────────────────────────
    st.markdown("#### 📋 Descriptive Statistics")
    st.dataframe(df.describe().style.format("{:.2f}"), use_container_width=True)

else:
    # ── Empty state ────────────────────────────────────────────────────────
    st.markdown("""
    <div style='margin-top:3rem; text-align:center; padding:3rem 2rem;
                background:rgba(255,255,255,0.02); border:1px dashed rgba(0,200,100,0.2);
                border-radius:16px;'>
        <div style='font-size:3rem; margin-bottom:1rem;'>📡</div>
        <div style='color:#ffffff; font-size:1.2rem; font-weight:600; margin-bottom:0.5rem;'>
            No data loaded yet
        </div>
        <div style='color:#5a7a9a; font-size:0.9rem;'>
            Use the tabs above to upload a CSV or fetch live data from Yahoo Finance.
        </div>
    </div>
    """, unsafe_allow_html=True)
