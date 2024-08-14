import streamlit as st
import plotly.graph_objects as go
from plotly.subplots import make_subplots


# Set the configuration for the Plotly chart, including the resolution settings
config = {
    "toImageButtonOptions": {
        "format": "png",  # The format of the exported image (png, svg, etc.)
        "filename": "weather_data_plot",  # Default filename
        # "height": 1080,  # Image height
        # "width": 1920,   # Image width
        "scale": 2.5       # Increase the resolution (scales up the image)
    }
}


def set_default_layout(fig):
    fig.update_layout(
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
        height=650, 
        margin=dict(autoexpand=True),
        template="seaborn",
    )
    return fig


def plot_weather_data(df):
    #fig = go.Figure()
    fig = make_subplots(specs=[[{"secondary_y": True}]])

    fig.add_trace(go.Scatter(x=df.index, y=df['Temp Out'], name='Temperature'), secondary_y=False)
    fig.add_trace(go.Scatter(x=df.index, y=df['Solar Rad.'], name='Solar radiation'), secondary_y=True)

    fig.update_layout(
        xaxis=dict(
            rangeselector=dict(buttons=list([dict(count=1, label="day", step="day", stepmode="backward"),
                                             dict(count=7, label="week", step="day", stepmode="backward"),
                                             dict(step="all")])),
            rangeslider=dict(visible=True), 
            type="date"),

        yaxis=dict(title="Temperature, °C"),
        yaxis2=dict(title="Solar Radiation, W/m2", side='right', showgrid=False),
    )

    fig = set_default_layout(fig)
    st.plotly_chart(fig, use_container_width=True, config=config)


def plot_processed_data(df, parameters):
    # fig = go.Figure()
    fig = make_subplots(specs=[[{"secondary_y": True}]])

    yaxis_label = []
    for param in parameters:
        if param!='Solar Rad.':
            fig.add_trace(go.Scatter(x=df.index, y=df[f'{param}'], name=f'{param}'))
            yaxis_label.append(param)
        else:
            fig.add_trace(go.Scatter(x=df.index, y=df[f'{param}'], name=f'{param}'), secondary_y=True)
       
    fig.update_layout(
        xaxis=dict(
            rangeselector=dict(buttons=list([dict(count=1, label="day", step="day", stepmode="backward"),
                                             dict(step="all")])),
            rangeslider=dict(visible=True), 
            type="date"),

        yaxis=dict(title=f"{' /  '.join(yaxis_label)}"),
        yaxis2=dict(title="Solar Rad., W/m2", side='right', showgrid=False),
    )
    
    fig = set_default_layout(fig)
    st.plotly_chart(fig, use_container_width=True, config=config)



if __name__ == '__main__':
    print('plotting file')