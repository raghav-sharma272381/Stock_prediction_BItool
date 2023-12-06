import streamlit as st
from datetime import date

import yfinance as yf
from prophet import Prophet
from prophet.plot import plot_plotly
from plotly import graph_objs as go 


# refrences for external apis

# Prophet Development Team. (2023, December 5). Prophet - Automatic Forecasting Procedure. Facebook Open Source. https://facebook.github.io/prophet/

# Yahoo Finance. (2022, December 5). Yahoo Finance - Business Finance, Stock Market, Quotes, News. Yahoo Finance. https://finance.yahoo.com/

START = "2015-01-01"
TODAY = date.today().strftime("%Y-%m-%d")

st.title("Stock Prediction App")

stocks = ("AAPL", "GOOG", "MSFT", "TSLA")
selected_stocks = st.selectbox("Select dataset for prediction", stocks)

n_years = st.slider("Years of predictions:", 1, 4)
period = n_years * 365

#Alisha and Sumeet
# loading data from yahoo finanace 
def load_data(ticker):
    data = yf.download(ticker, START, TODAY)
    data.reset_index(inplace=True)
    return data


data_load_state = st.text('Loading data...')
data = load_data(selected_stocks)
data_load_state.text('Loading data... done!')

st.subheader('Raw data')
st.write(data.tail())

print(data)
# Plot raw data

# raghav and jasdeep 
class ScatterGraph:
    def plot_raw_data():
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=data['Date'], y=data['Open'], name="stock_open"))
        fig.add_trace(go.Scatter(x=data['Date'], y=data['Close'], name="stock_close"))
        fig.layout.update(title_text='Stock open and close', xaxis_rangeslider_visible=True)
        st.plotly_chart(fig)

class CandlestickGraph:
    def plot_raw_data():
        fig = go.Figure(data=[go.Candlestick(x=data['Date'],
                                                        open=data['Open'],
                                                        high=data['High'],
                                                        low=data['Low'],
                                                        close=data['Close'],
                                                        name="Candlestick")])
        fig.update_layout(title_text='Candlestick Chart', xaxis_rangeslider_visible=True)
        st.plotly_chart(fig)

ScatterGraph.plot_raw_data()
CandlestickGraph.plot_raw_data()

# Predict forecast with Prophet.
# Aishmitta and Agam 

#adapter
class Adapter:
    def __init__(self, date_column='Date', close_column='Close'):
        self.date_column = date_column
        self.close_column = close_column

    def transform_data(self, data):
        df_train = data[[self.date_column, self.close_column]]
        df_train = df_train.rename(columns={self.date_column: "ds", self.close_column: "y"})
        return df_train


adapter = Adapter()
df_train = adapter.transform_data(data)

#singleton
m = None;

if (m == None):
    m =  Prophet()



m.fit(df_train)
future = m.make_future_dataframe(periods=period)
forecast = m.predict(future)

# Show and plot forecast
st.subheader('Forecast data')
st.write(forecast.tail())

st.write(f'Forecast plot for {n_years} years')
fig1 = plot_plotly(m, forecast)
st.plotly_chart(fig1)

st.write("Forecast components")
fig2 = m.plot_components(forecast)
st.write(fig2)


