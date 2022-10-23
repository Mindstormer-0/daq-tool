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

    # Supply the data
    x = np.random.sample(100)
    y = np.random.sample(100)
    z = np.random.choice(a=['a', 'b', 'c'], size=100)

    df1 = pd.DataFrame({'x': x, 'y': y, 'z': z}, index=range(100))

    # Configure web elements
    # Single navitem
    nav_item = dbc.NavItem(dbc.NavLink("Link", href="#"))

    # Dropdown menu
    dropdown = dbc.DropdownMenu(
        children=[
            dbc.DropdownMenuItem("Entry 1"),
            dbc.DropdownMenuItem("Entry 2"),
            dbc.DropdownMenuItem(divider=True),
            dbc.DropdownMenuItem("Entry 3"),
        ],
        nav=True,
        in_navbar=True,
        label="Menu",
    )

    # Navbar with logo
    navbar = dbc.Navbar(
        dbc.Container(
            [
                html.A(
                    # Use row and col to control vertical alignment of logo / brand
                    dbc.Row(
                        [
                            dbc.Col(html.Img(src=LOGO, height="35px")),
                            #dbc.Col(dbc.NavbarBrand("Title", className="ms-2")),
                        ],
                        align="center",
                        className="g-0",
                    ),
                    href="https://calebcollar.dev",
                    style={"textDecoration": "none"},
                ),
                dbc.NavbarToggler(id="navbar-toggler2", n_clicks=0),
                dbc.Collapse(
                    dbc.Nav(
                        [nav_item, dropdown],
                        className="ms-auto",
                        navbar=True,
                    ),
                    id="navbar-collapse2",
                    navbar=True,
                ),
            ],
        ),
        color="dark",
        dark=True,
        className="mb-5",
    )

    videobg = html.Div(
        [
            html.Video(id='bgvid', src=BGVID,
                       autoPlay='autoPlay', loop='loop', muted='muted', className='fullscreen-bg__video')
        ]
    )

    # Configure the layout

    app.layout = html.Div(
        [navbar, videobg]
    )

    # Use a callback to toggle the collapse on small screens

    def toggle_navbar_collapse(n, is_open):
        if n:
            return not is_open
        return is_open

    # the same function (toggle_navbar_collapse) is used in all three callbacks
    for i in [2]:
        app.callback(
            Output(f"navbar-collapse{i}", "is_open"),
            [Input(f"navbar-toggler{i}", "n_clicks")],
            [State(f"navbar-collapse{i}", "is_open")],
        )(toggle_navbar_collapse)

    # Start up the web app
    app.run(debug=True, threaded=True)
