# 📈 Stock Trend Forecasting

**Stock Trend Forecasting** is a comprehensive stock price forecasting platform built with Python and Streamlit. It leverages multiple machine learning and deep learning models to provide accurate stock price predictions with interactive visualizations.

---

## 👨‍💻 Developer

| | |
|---|---|
| **Name** | Mohd Ayan |
| **Email** | mohdayan8896@gmail.com |
| **Phone** | 7355339397 |
| **LinkedIn** | [mohd-ayan-39725b334](https://www.linkedin.com/in/mohd-ayan-39725b334) |
| **GitHub** | [Ayan9397](https://github.com/Ayan9397) |
| **College** | Bansal Institute of Engineering and Technology, Lucknow |
| **Degree** | B.Tech Computer Science (2022 – 2026) |
| **CGPA** | 8.3 |

---

## 🚀 Features

### 📊 Multiple Model Support
- **Classical Models**: ARIMA, SARIMA
- **Deep Learning Models**: LSTM, CNN, RNN, GRU
- **Hybrid Models**: LSTM-CNN-RNN, LSTM-GRU
- **Time Series Models**: Prophet

### 📈 Data Sources
- **CSV Upload**: Upload your own stock data with OHLC (Open, High, Low, Close) prices and volume
- **Yahoo Finance Integration**: Real-time stock data fetching using yfinance
- **Date Range Selection**: Flexible date range for historical data

### 🎛️ Customizable Parameters
- **Neural Network Models**: Epochs, Lookback Window, Units, Batch Size, Future Prediction Days and Test-Train Split
- **ARIMA/SARIMA**: Manual parameter setting or automatic optimization with RMSE-based selection
- **Prophet**: Tuning modes (Quick/Comprehensive), Frequency settings (Business/Daily), Uncertainty samples

### 📊 Interactive Visualizations
- **Plotly Charts**: Interactive training, testing, and forecast visualizations
- **Residual Analysis**: Model performance evaluation with residual plots
- **Error Metrics**: MAE, RMSE, MAPE, and other statistical measures

---

## 🛠️ Installation

### Prerequisites
- Python 3.8 or higher
- pip package manager

### Quick Setup

```bash
# Clone the repository
git clone https://github.com/Ayan9397/Stock-Trend-Forecasting.git
cd Stock-Trend-Forecasting

# Install required packages
pip install -r requirements.txt

# Run the application
streamlit run streamlit_app.py
```

---

## 📱 Usage

### 1. Launch the Application
```bash
streamlit run streamlit_app.py
```

### 2. Select Data Source
- **Upload CSV**: Upload a CSV file with columns: Date, Open, High, Low, Close, Volume
- **Yahoo Finance**: Enter stock ticker symbol (e.g., AAPL, GOOGL, TSLA)

### 3. Choose a Model
- ARIMA, SARIMA
- LSTM, CNN, RNN, GRU
- Prophet
- LSTM-CNN-RNN (Hybrid), LSTM-GRU (Hybrid)

### 4. Configure Parameters & Train
Click **"Train Model"** to start forecasting and view results.

---

## 📊 Model Details

| Model | Type | Best For |
|---|---|---|
| ARIMA | Classical | Trend-based forecasting |
| SARIMA | Classical | Seasonal patterns |
| LSTM | Deep Learning | Long-term dependencies |
| CNN | Deep Learning | Pattern recognition |
| RNN | Deep Learning | Sequential data |
| GRU | Deep Learning | Efficient sequence modeling |
| LSTM-GRU | Hybrid | Memory + Efficiency |
| LSTM-CNN-RNN | Hybrid | Combined strengths |
| Prophet | Time Series | Strong seasonality |

---

## 📈 Performance Metrics

- **Mean Absolute Error (MAE)**
- **Root Mean Square Error (RMSE)**
- **Mean Absolute Percentage Error (MAPE)**
- **R-squared (R²)**

---

## 🙏 Acknowledgments

- **Streamlit** for the amazing web app framework
- **Yahoo Finance** for providing free stock data
- **TensorFlow/Keras** for deep learning capabilities
- **Prophet** for time series forecasting
- **Plotly** for interactive visualizations

---

⭐ **If you find this project helpful, please consider giving it a star!** ⭐

*Developed by [Mohd Ayan](https://github.com/Ayan9397) — B.Tech CSE, Bansal Institute of Engineering and Technology, Lucknow*
