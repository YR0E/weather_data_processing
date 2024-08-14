import streamlit as st

from data_processing import read_weather_data, process_weather_data
from plotting import  plot_weather_data, plot_processed_data


st.title('Weather data processing')


uploaded_file = st.file_uploader('Choose a weather data file', type='txt')
is_sample = st.checkbox('Use sample data', value=True*(uploaded_file is None),
                        help='As an example, data from the weather station in Aktau for the period from March 21 to April 4, 2024 will be used. Use when no data is uploaded')
if (is_sample) and (uploaded_file is None):
    uploaded_file = './data/meteo_2103-040424.txt'

st.markdown('***')


if uploaded_file is not None:
    # read uploaded file and process data
    df_raw = read_weather_data(uploaded_file, is_sample)
    df = process_weather_data(df_raw.copy())


    ### SECTION 1
    st.subheader('Looking at raw data')

    # expander 1
    with st.expander("See uploaded data"):
        st.dataframe(df_raw, height=280)

    # plot 1
    plot_weather_data(df)




    ### SECTION 2
    st.markdown('***')
    st.subheader('Processing data')

    # multiselect
    options = st.multiselect('Select parameters:', options=df.columns, default=['Temp Out', 'Solar Rad.', 'Wind Speed'])


    # time range
    d = st.date_input('Select time range:', (df.index[0], df.index[-1]), 
                      min_value=df.index[0], max_value=df.index[-1], format="DD.MM.YYYY")
    df_processed = df[options].loc[d[0]:d[-1]].copy()
    
    # plot 2
    plot_processed_data(df_processed, options)


    # interpolate
    col1, col2 = st.columns([1, 3])
    is_interp = col1.checkbox('Interpolate data')
    if is_interp:
        interp_interval = col2.select_slider('Select interpolation interval:', 
                                             options=['10s', '30s', '1min', '5min'], value='30s')
        df_processed = df_processed.resample(f'{interp_interval}').interpolate('linear')
        filename = f"processed_weather_data_{d[0].strftime('%d%m')}_{d[-1].strftime('%d%m')}_interp.csv"
    
    else:
        filename = f"processed_weather_data_{d[0].strftime('%d%m')}_{d[-1].strftime('%d%m')}.csv"


    # expander 2
    with st.expander("See processed data"):
        st.dataframe(df_processed, height=280)


    # download
    st.download_button(
    label="Download processed data as CSV",
    data=df_processed.to_csv(),
    file_name=filename,
    mime="text/csv", )