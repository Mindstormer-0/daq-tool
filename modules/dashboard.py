import random
import datetime

def run_dash():
  import datetime
  from dash_bootstrap_templates import load_figure_template
  from dash import Dash, dcc, html, Input, Output
  import plotly.express as px
  import dash_bootstrap_components as dbc
  import pandas as pd
  import numpy as np
  # select the Bootstrap stylesheet and figure template for the theme here:
  template_theme = "vapor"
  url_theme = dbc.themes.VAPOR
  # -----------------------------
  
  #Configure the app
  app = Dash(__name__, external_stylesheets=[url_theme], update_title=None)
  load_figure_template(template_theme)

  def get_initial(data):
    y = random.random()
    x = datetime.datetime.now()
    data.update({'time': [x], 'mL': [y]})
    return data

  #Get initial data
  data = {'time': [], 'mL': []}
  data = get_initial(data)
  df = pd.DataFrame.from_dict(data, orient='index').T
  fig_tv = px.line(df, x="time", y="mL")
  fig_bf = px.scatter(df, x="time", y="mL")
  fig_mv = px.scatter(df, x="time", y="mL")
  fig_co2 = px.scatter(df, x="time", y="mL")
  fig_o2 = px.scatter(df, x="time", y="mL")

  #Create the layout
  app.layout = html.Div([
    html.H2('DAQ-Tool Dashboard'),
    html.H4('Tidal Volume'),
    dcc.Graph(id="tidal-volume", figure=fig_tv),
    html.H4('Breathing Frequency'),
    dcc.Graph(id="breath-frequency", figure=fig_bf),
    html.H4('Minute Ventilation'),
    dcc.Graph(id="minute-ventilation", figure=fig_mv),
    html.H4('CO2 Level'),
    dcc.Graph(id="co2-level", figure=fig_co2),
    html.H4('O2 Level'),
    dcc.Graph(id="o2-level", figure=fig_o2),
    dcc.Interval(id='interval-component')
  ])

  @app.callback(Output('tidal-volume', 'extendData'), [Input('interval-component', 'n_intervals')])
  def get_update(n_intervals):
    y = random.random()
    x = datetime.datetime.now()
    data['time'].append(x)
    data['mL'].append(y)
    df = pd.DataFrame.from_dict(data)
    fig_tv = px.line(df, x="time", y="mL")
    return fig_tv

  app.run(debug=True, threaded=True)