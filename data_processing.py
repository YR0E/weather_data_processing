import numpy as np
import pandas as pd
import streamlit as st


@st.cache_data(max_entries=1)
def read_weather_data(uploaded):
    ''' read txt file with weather data
    '''

    # Read the header rows separately
    header_rows = pd.read_csv(uploaded, sep='\t', nrows=2, header=None)

    # Combine the two header rows to create a single row of column names
    header_rows = header_rows.replace(np.nan, str())
    combined_headers = [' '.join(col).strip() for col in zip(*header_rows.values)]

    # Read the data using the combined headers
    uploaded.seek(0,0)
    data = pd.read_csv(uploaded, sep='\t', skiprows=2, names=combined_headers)
    return data


@st.cache_data(max_entries=1)
def process_weather_data(df):
    ''' process txt file with weather data
    '''

    df['Date'] = pd.to_datetime(df['Date'] + df['Time'], format='%d.%m.%y%H:%M')
    df = df.replace(['---', '------'], np.nan)
    df = df.drop(columns=['Time'])
    
    df = df.set_index('Date')
    df = df.reindex(pd.date_range(df.index[0] - pd.Timedelta(5, "min"), df.index[-1], freq='5min'))
    df = df.apply(pd.to_numeric, downcast='float', errors='ignore')
    # df[['Wind Dir', 'Hi Dir']] = df[['Wind Dir', 'Hi Dir']].astype('category')

    # df.index.name = 'Time'
    # df = df.interpolate()

    return df

if __name__ == '__main__':
    print('processing file')