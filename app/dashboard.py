# This function is used to configure the dashboard and then launch it locally.
def run_dash():
    # Imports
    from dash import Dash, dcc, html, Input, Output, State
    from dash_bootstrap_templates import load_figure_template
    from dash_bootstrap_components._components.Container import Container
    import time, datetime
    import plotly.graph_objs as go
    import plotly.express as px
    import dash_bootstrap_components as dbc
    import pandas as pd
    import numpy as np

    # Select the Bootstrap stylesheet and figure template for the theme
    template_theme = "solar"
    url_theme = dbc.themes.SOLAR

    # Configure the app
    app = Dash(__name__, external_stylesheets=[
               url_theme], update_title=None)  # type: ignore
    load_figure_template(template_theme)

    # Fetch static Resources
    LOGO = app.get_asset_url('logo.png')
    BGVID = app.get_asset_url('bg.mp4')
    BGPOSTER = app.get_asset_url('poster.png')

    # Supply the data TODO: dummy data for now
    df = pd.read_csv(
    "https://raw.githubusercontent.com/plotly/datasets/master/finance-charts-apple.csv")
    df.columns = [col.replace("AAPL.", "") for col in df.columns]

    # Individual dataframes
    df_tv = df
    df_bf = df
    df_mv = df
    df_co2 = df
    df_o2 = df

    # Instantiate the graphs
    fig_tv = go.Figure()
    fig_bf = go.Figure()
    fig_mv = go.Figure()
    fig_co2 = go.Figure()
    fig_o2 = go.Figure()
    figures = [fig_tv, fig_bf, fig_mv, fig_co2, fig_o2]

    # Add range sliders
    for fig in figures:
        fig.add_trace(go.Scatter(x=list(df.Date), y=list(df.High)))
        fig.update_layout(autosize=True, margin=dict(l=20, r=40, t=20, b=10))
        fig.update_layout(
            xaxis=dict(
                rangeselector=dict(
                    bgcolor="#839496",
                    font=dict(
                        color="white"),
                    buttons=list([
                        dict(count=1,
                            label="1m",
                            step="month",
                            stepmode="backward"),
                        dict(count=6,
                            label="6m",
                            step="month",
                            stepmode="backward"),
                        dict(count=1,
                            label="YTD",
                            step="year",
                            stepmode="todate"),
                        dict(count=1,
                            label="1y",
                            step="year",
                            stepmode="backward"),
                        dict(step="all")
                    ])
                ),
                rangeslider=dict(
                    visible=True
                ),
                type="date"
            )
        )

    # Configure web elements
    # Video background element
    videobg = html.Div(
        [
            html.Video(id='bgvid', src=BGVID, poster=BGPOSTER,
                       autoPlay='autoPlay', loop='loop', muted='muted', className='fullscreen-bg__video')
        ]
    )

    # Single navitem
    nav_item = dbc.NavItem(dbc.NavLink("Github", href='https://github.com/Mindstormer-0/daquery-tool'))

    # Dropdown menu
    dropdown = dbc.DropdownMenu(
        children=[
            dbc.DropdownMenuItem("Vertical"),
            dbc.DropdownMenuItem("Grid"),
            dbc.DropdownMenuItem(divider=True),
            dbc.DropdownMenuItem("Reset"),
        ],
        nav=True,
        in_navbar=True,
        label="View",
    )

    # Navbar with logo
    navbar = dbc.Navbar(
        dbc.Container(
            [
                html.A(
                    # Use row and col to control vertical alignment of logo / brand
                    dbc.Row(
                        [
                            dbc.Col(html.Img(src=LOGO, height='35px')),
                            #dbc.Col(dbc.NavbarBrand("Title", className="ms-2")),
                        ],
                        align='center',
                        className='g-0',
                    ),
                    href='#',
                    style={'textDecoration': 'none'},
                ),
                dbc.NavbarToggler(id='navbar-toggler2', n_clicks=0),
                dbc.Collapse(
                    dbc.Nav(
                        [nav_item, dropdown],
                        className='ms-auto',
                        navbar=True,
                    ),
                    id='navbar-collapse2',
                    navbar=True,
                ),
            ],
        ),
        id='navbar',
        color='dark',
        dark=True,
        className='mb-5',
    )

    # Cards with graphs
    tidal_volume = dbc.Container(
        [
            dbc.Card(
                [
                    dbc.CardHeader("Tidal Volume:"),
                    dcc.Graph(figure=fig_tv),
                ],
                className='card mb-3 g-0 d-flex')
        ]
    )

    breathing_frequency = dbc.Container(
        [
            dbc.Card(
                [
                    dbc.CardHeader("Breathing Frequency:"),
                    dcc.Graph(figure=fig_bf),
                ],
                className='card mb-3 g-0 d-flex')
        ]
    )

    minute_ventilation = dbc.Container(
        [
            dbc.Card(
                [
                    dbc.CardHeader("Minute Ventilation:"),
                    dcc.Graph(figure=fig_mv),
                ],
                className='card mb-3 g-0 d-flex')
        ]
    )

    CO2 = dbc.Container(
        [
            dbc.Card(
                [
                    dbc.CardHeader("CO2 Level:"),
                    dcc.Graph(figure=fig_co2),
                ],
                className='card mb-3 g-0 d-flex')
        ]
    )

    O2 = dbc.Container(
        [
            dbc.Card(
                [
                    dbc.CardHeader("O2 Level:"),
                    dcc.Graph(figure=fig_o2),
                ],
                className='card mb-3 g-0 d-flex')
        ]
    )

    # Spacer
    spacer = dbc.Container(className='spacer')

    # Footer
    footer = dbc.Container(className='footer')

    # Configure the layout order
    app.layout = dbc.Container(
        [
            dcc.Loading(
                [
                    html.Div(
                        [
                            navbar,
                            videobg,
                        ]
                    ),
                ],
                id="loading-1",
                type="dot",
                fullscreen=True,
                color='#268bd2',
                style={'backgroundColor': '#002b36'}
            ),
            dbc.Container(
                [
                    dcc.Loading(tidal_volume, color='#268bd2'),
                    dcc.Loading(breathing_frequency, color='#268bd2'),
                    dcc.Loading(minute_ventilation, color='#268bd2'),
                    dcc.Loading(CO2, color='#268bd2'),
                    dcc.Loading(O2, color='#268bd2')
                ]
            )
        ], fluid=True, style={'padding': '0'}
    )

    # Use a callback to toggle the collapse on small screens
    def toggle_navbar_collapse(n, is_open):
        if n:
            return not is_open
        return is_open

    # The same function can be used in all callbacks
    for i in [2]:
        app.callback(
            Output(f"navbar-collapse{i}", "is_open"),
            [Input(f"navbar-toggler{i}", "n_clicks")],
            [State(f"navbar-collapse{i}", "is_open")],
        )(toggle_navbar_collapse)

    # Start up the web app
    app.run(debug=True, threaded=True)
