from dash import Dash, dcc, html, Input, Output
import plotly.express as px

import pandas as pd

df = pd.read_csv('https://raw.githubusercontent.com/resbaz/r-novice-gapminder-files/d215697ae64dd34814cd7534d19100679e0f2cd9/data/gapminder-FiveYearData.csv')

app = Dash(__name__,)

app.layout = html.Div([

    dcc.Graph(id='graph-with-slider'),
    dcc.Slider(
        df['year'].min(),
        df['year'].max(),
        step=None,
        value=df['year'].min(),
        marks={str(year): str(year) for year in df['year'].unique()},
        id='year-slider'
    ),

    dcc.Dropdown(
        options=df['year'].unique(),
        className='dropdown',
        value=df['year'].min(),
        id='year-ddl'
    ),
    dcc.Graph(id='graph-with-ddl')
])


@app.callback(
    Output('graph-with-slider', 'figure'),
    Input('year-slider', 'value'))
def update_slider_chart(selected_year):
    filtered_df = df[df.year == selected_year]

    fig = px.scatter(filtered_df, x="gdpPercap", y="lifeExp",
                     size="pop", color="continent", hover_name="country",
                     log_x=True, size_max=55)

    fig.update_layout(transition_duration=500)

    return fig


@app.callback(
    Output('graph-with-ddl', 'figure'),
    Input('year-ddl', 'value'))
def update_ddl_chart(selected_year):
    filtered_df = df[df.year == selected_year]

    fig = px.scatter(filtered_df, x="gdpPercap", y="lifeExp",
                     size="pop", color="continent", hover_name="country",
                     log_x=False, size_max=55)

    fig.update_layout(transition_duration=500)

    return fig


if __name__ == '__main__':
    app.run_server(debug=True)
