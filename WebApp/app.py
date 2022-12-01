import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objects as go
import plotly.subplots as subplots
import numpy as np
import pandas as pd
from datetime import date
from dash.dependencies import Input, Output

app = dash.Dash(__name__,
                meta_tags=[{"name": "viewport", "content": "width=device-width, initial-scale=1"}]
                )

df = pd.read_csv('time_use_environment.csv', parse_dates=['time'])
dfmessages = pd.read_csv('messages.csv', sep="@")

app.config.suppress_callback_exceptions = True
server = app.server

x = np.arange(10)

app.layout = html.Div(children=[
    # Header
    html.Div(className="header", children=[
        # Image
        html.Img(src=app.get_asset_url('rainy-day_128x128.ico'), className="header-emoji"),
        # Header title
        html.H1(children='TABLERO DE PROYECCIONES ENERGÉTICAS', className="header-title"),
        # Header description
        html.P(
            children='En esta aplicación podrás ver el consumo energético actual y el consumo energético esperado en los días próximos a la fecha seleccionada.',
            className="header-description"
        ),
    ]),
    # First graph - Month
    html.Div(className="row", style={'padding-top': '20px'}, children=[
        html.Div(id='month-graph-card', className="card", children=[
            dcc.Graph(
                id='month-graph'
            )
        ])
    ]),
    # Two columns to show info
    html.Div(className="row_info", children=[
        # Left part
        html.Div(className="column left", children=[
        # html.Div(className="three-columns-grid", children=[
            html.Div(className="card_info", children=[
                # Title
                html.Div("Fecha", className="menu-title"),
                # Date picker
                html.Div(
                    dcc.DatePickerSingle(
                        id='my-date-picker-single',
                        min_date_allowed=date(2016, 1, 1),
                        max_date_allowed=date(2016, 12, 31),
                        initial_visible_month=date(2016, 1, 1),
                        date=date(2016, 1, 1),
                        clearable=False,
                        className="date_picker",
                        display_format='DD/MM/YYYY',
                        day_size=40
                    ),
                ),
                # Title
                html.Div("Variable de interés", className="menu-title", style={'padding-top': '20px'}),
                # Dropdown menu
                html.Div(
                    dcc.Dropdown(
                        id='variables-dropdown', style={'font-family': 'Arial, Helvetica, sans-serif'},
                        options=[
                            {'label': 'Consumo', 'value': 'use'},
                            {'label': 'Temperatura', 'value': 'temperature'},
                            {'label': 'Humedad', 'value': 'humidity'},
                            {'label': 'Presión', 'value': 'pressure'}
                        ],
                        value='use',
                        clearable=False,
                        className='dropdown'
                    )
                )
            ])
        ]),
        # Right part
        html.Div(className="column mid", children=[
        # html.Div(className="three-columns-grid", children=[
            html.Div(className="card_info", children=[
                # Row to show the expected day consumption
                html.Div(className="row", style={'padding-top': '15px'}, children=[
                    # Current consumption text
                    html.Div(className='three-columns', children=[
                        html.P("Tu consumo en el día: ", className='info'),
                    ]),
                    # Current consumption
                    html.Div(className='three-columns', children=[
                        html.P(id='output-day-consumption', className='info'),
                    ]),
                    # Current price
                    html.Div(className="three-columns", children=[
                        html.P(id='output-day-price', className='info')
                    ]),
                ]),
                # Row to show the current hour consumption
                html.Div(className="row", style={'padding-top': '20px'}, children=[
                    # Current consumption text
                    html.Div(className='three-columns', children=[
                        html.P("Tu consumo por hora: ", className='info'),
                    ]),
                    # Current consumption
                    html.Div(className='three-columns', children=[
                        html.P(id='output-hour-consumption', className='info')
                    ]),
                    # Current price
                    html.Div(className="three-columns", children=[
                        html.P(id='output-hour-price', className='info')
                    ]),
                ]),
            ])
        ]),
        # Nueva columna - Predicción
        html.Div(className="column right", children=[
        # html.Div(className="three-columns-grid", children=[
            html.Div(className="card_info", children=[
                # Title
                html.Div("Consumo estimado para el siguiente día", className="header-box"),
                # Prediction box
                html.Div(className="column-box", children=[
                    html.P(id='output-use-prediction', className='info')
                ]),
            ])
        ])
    ]),
    # Second graph - Day
    html.Div(className="row", children=[
        html.Div(id='day-graph-card', className="card", children=[
            dcc.Graph(
                id='day-graph'
            )
        ])
    ]),
    # Message
    html.Div(className="row", style={'padding-top': '20px', 'padding-bottom': '20px'}, children=[
        html.Div(id='message-card', className="message", children=[
            html.P(id='output-message', className='info'),
            html.P("El nivel de importancia de otras variables de tu consumo lo puedes ver aquí: ", className='info'),
            html.Img(src=app.get_asset_url('shap.png'), className="header-emoji"),
            html.P("Detectamos 4 tipos de comportamientos, que corresponden a las clases 0,1,2,3. ", className='info'),
            html.P("Para más información, consulta la documentación.", className='info'),

        ])
    ]),
    # Footer
    html.Div(className="footer", children=[
        # Row 1
        html.Div(className="row", children=[
            html.P(className="column complete footer_title", children=['REALIZADO POR']),
        ]),
        # Row 2
        html.Div(className="row", style={'position': 'relative', 'top': '-20px'}, children=[
            # Column 1 name
            html.P(className="column mid footer_text", children=['Alejandra Guerrero']),
            # Column 2 name
            html.P(className="column mid footer_text", children=['Luis Enrique García']),
            # Column 3 name
            html.P(className="column mid footer_text", children=['Diego Alejandro Peña']),
        ])
    ])
])


# Month graph
@app.callback(
    Output(component_id='month-graph', component_property='figure'),
    [Input(component_id='my-date-picker-single', component_property='date')],
    prevent_initial_call=True
)
def update_month(input_date):
    data = []
    if input_date is not None:
        df_pred = pd.read_csv('Data_demonstration.csv', parse_dates=['time'])
        df_pred_head = df_pred.head(360)
        df_pred_tail = df_pred.tail(360)
        fig_pred = go.Figure()
        fig_pred.add_trace(go.Scatter(x=df_pred_head["time"], y=df_pred_head['use [kW]'], name='uso'))
        fig_pred.add_trace(go.Scatter(x=df_pred_tail["time"], y=df_pred_tail['use [kW]'], mode='lines',
                                      marker_color=df_pred_tail['use [kW]'], name='predicción'))

        fig_pred.layout = {'title': 'Consumo energético en el mes', 'plot_bgcolor': 'rgba(0,0,0,0)'}
        fig_pred.update_xaxes(showgrid=True, gridcolor='rgba(225,225,225,0.25)')
        fig_pred.update_yaxes(showgrid=True, gridcolor='rgba(225,225,225,0.25)')

        return fig_pred

# Day graph
@app.callback(
    [Output(component_id='day-graph', component_property='figure'),
     Output(component_id='output-day-consumption', component_property='children'),
     Output(component_id='output-use-prediction', component_property='children'),
     Output(component_id='output-hour-consumption', component_property='children'),
     Output(component_id='output-day-price', component_property='children'),
     Output(component_id='output-hour-price', component_property='children'),
     Output(component_id='output-message', component_property='children')],
    [Input(component_id='my-date-picker-single', component_property='date'),
     Input(component_id='variables-dropdown', component_property='value')],
    prevent_initial_call=True
)
def update_day(input_date, input_variable):
    data = []
    if input_date is not None:
        date_object = date.fromisoformat(input_date)

        day = date_object.day
        month = date_object.month
        year = date_object.year

        df_day = df[(df['day'] == day) & (df['month'] == month) & (df['year'] == year)]

        # Retrieving message
        try:
            day_msg = dfmessages[(dfmessages['day'] == day) & (dfmessages['month'] == month)].iloc[0,3]
        except:
            day_msg = 'Todavía no tenemos información de este día para ti.'
        # Checking the consumption in the day
        day_consumption = df_day.resample('D', on='time')['use'].sum().to_frame().reset_index()
        # Creating the figure
        trace = go.Scatter(x=df_day["time"], y=df_day[input_variable], line=dict(color='firebrick'))
        data.append(trace)
        # fig = go.Figure()
        #fig.add_trace(go.Scatter(x=df_day["time"], y=df_day[input_variable]))
        #fig.add_trace(go.Scatter(x=day_consumption["time"], y=day_consumption["use"]))

        # Consumption in the day
        consumption_in_day = round((day_consumption.use[0] / 60), 2)
        consumption_day_text = str(consumption_in_day) + ' [kWh]'
        # Consumption in one hour
        consumption_in_hour = round(consumption_in_day / 24, 2)
        consumption_hour_text = str(consumption_in_hour) + ' [kWh]'

        # Price kW / Hour
        price = 500
        price_day = round(consumption_in_day) * price
        price_day_text = '$ ' + str(round(price_day))
        price_hour = price_day / 24
        price_hour_text = '$ ' + str(round(price_hour))

        consumption_next_day_text = str(consumption_in_day) + ' [kWh]'

        text = ""
        if input_variable == "use":
            text = "Consumo (en kWh)"
        elif input_variable == "humidity":
            text = "Humedad (%)"
        elif input_variable == "pressure":
            text = "Presión (mmHg)"
        elif input_variable == "temperature":
            text = "Temperatura (°F)"
        elif input_variable == "windSpeed":
            text = "Velocidad del viento (m/s)"

        layout = {'title': text + ' en el día'}


        return ({'data': data, 'layout': layout},
                consumption_day_text, consumption_next_day_text, consumption_hour_text, price_day_text, price_hour_text, day_msg)

        # return fig, consumption_day_text, consumption_hour_text, price_day_text, price_hour_text


if __name__ == '__main__':
    app.run_server(debug=True)
