import pandas as pd
import streamlit as st
import plotly.graph_objects as go
from plotly.subplots import make_subplots



def set_default_layout(fig):
    fig.update_layout(
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
        height=650, 
        margin=dict(autoexpand=True),
        # template="seaborn",
    )
    return fig


def plot_weather_data(df):
    #fig = go.Figure()
    fig = make_subplots(specs=[[{"secondary_y": True}]])

    fig.add_trace(go.Scatter(x=df.index, y=df['Temp Out'], name='Temperature'), secondary_y=False)
    fig.add_trace(go.Scatter(x=df.index, y=df['Wind Speed'], name='Wind Speed'), secondary_y=False)
    fig.add_trace(go.Scatter(x=df.index, y=df['Solar Rad.'], name='Solar radiation'), secondary_y=True)

    

    fig.update_layout(
        xaxis=dict(
            rangeselector=dict(buttons=list([dict(count=1, label="day", step="day", stepmode="backward"),
                                             dict(count=7, label="week", step="day", stepmode="backward"),
                                             dict(step="all")])),
            rangeslider=dict(visible=True), 
            type="date"),

        yaxis=dict(title="Temperature, °C / Wind Speed, m/s"),
        yaxis2=dict(title="Solar Radiation, W/m2", side='right', showgrid=False),
    )

    fig = set_default_layout(fig)
    st.plotly_chart(fig, use_container_width=True)


def plot_processed_data(df, parameters):
    # fig = go.Figure()
    fig = make_subplots(specs=[[{"secondary_y": True}]])

    for param in parameters:
        if param!='Solar Rad.':
            fig.add_trace(go.Scatter(x=df.index, y=df[f'{param}'], name=f'{param}'))
        else:
            fig.add_trace(go.Scatter(x=df.index, y=df[f'{param}'], name=f'{param}'), secondary_y=True)
       
    fig.update_layout(
        xaxis=dict(
            rangeselector=dict(buttons=list([dict(count=1, label="day", step="day", stepmode="backward"),
                                             dict(step="all")])),
            rangeslider=dict(visible=True), 
            type="date"),

        yaxis=dict(title="Temperature, °C / Wind Speed, m/s"),
        yaxis2=dict(title="Solar Radiation, W/m2", side='right', showgrid=False),
    )
    
    fig = set_default_layout(fig)
    st.plotly_chart(fig)



if __name__ == '__main__':
    print('plotting file')