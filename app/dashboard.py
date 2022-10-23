# This function is used to configure the dashboard and then launch it locally.
def run_dash():
    # Imports
    from dash import Dash, dcc, html, Input, Output, State
    from dash_bootstrap_templates import load_figure_template
    from dash_bootstrap_components._components.Container import Container
    import datetime
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

    # Supply the data
    x = np.random.sample(100)
    y = np.random.sample(100)
    z = np.random.choice(a=['a', 'b', 'c'], size=100)

    # Dataframes
    df_tv = pd.DataFrame({'x': x, 'y': y, 'z': z}, index=range(100))
    df_bf = pd.DataFrame({'x': x, 'y': y, 'z': z}, index=range(100))
    df_mv = pd.DataFrame({'x': x, 'y': y, 'z': z}, index=range(100))
    df_co2 = pd.DataFrame({'x': x, 'y': y, 'z': z}, index=range(100))
    df_o2 = pd.DataFrame({'x': x, 'y': y, 'z': z}, index=range(100))

    # Configure the graphs
    fig_tv = px.scatter(df_tv, x="x", y="y", height=300,)
    fig_tv.update_layout(autosize=True, margin=dict(l=20, r=40, t=10, b=0))

    fig_bf = px.scatter(df_bf, x="x", y="y", height=300,)
    fig_bf.update_layout(autosize=True, margin=dict(l=20, r=40, t=10, b=0))

    fig_mv = px.scatter(df_mv, x="x", y="y", height=300,)
    fig_mv.update_layout(autosize=True, margin=dict(l=20, r=40, t=10, b=0))

    fig_co2 = px.scatter(df_co2, x="x", y="y", height=300,)
    fig_co2.update_layout(autosize=True, margin=dict(l=20, r=40, t=10, b=0))

    fig_o2 = px.scatter(df_o2, x="x", y="y", height=300,)
    fig_o2.update_layout(autosize=True, margin=dict(l=20, r=40, t=10, b=0))

    # Configure web elements
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
    app.layout = html.Div(
        [
            navbar,
            videobg,
            tidal_volume,
            breathing_frequency,
            minute_ventilation,
            CO2,
            O2,
            footer
        ]
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
