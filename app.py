from typing import Union, Any

import dash
from dash import dcc
from dash import html
from dash import dash_table
from dash.dependencies import Input, Output, State
import dash_bootstrap_components as dbc

import data
import components

import pandas as pd
import plotly.express as px
from pandas import Series, DataFrame
from pandas.core.generic import NDFrame

from dash_iconify import DashIconify

# init
app = dash.Dash(__name__,
                # add bootstrap
                external_stylesheets=[dbc.themes.BOOTSTRAP])

""" LAYOUT """
app.layout = html.Div([

    # Header
    html.Header(
        dbc.Row([
            dbc.Col(
                html.Img(src=app.get_asset_url("images/satellite.png"),
                         style={"width": "200px"}), width={"size": 2, "offset": 0}
            ),
            dbc.Col([
                html.H1("Exoplanet Data Visualization"),
                html.A("Read about exoplanets", href="https://spaceplace.nasa.gov/all-about-exoplanets/en/")
            ], width={"size": 7, "offset": 0})
        ], className="app-header"), className="app-sticky"),

    dcc.Store(id="filtered-data", storage_type="session"),

    # Body
    html.Main(
        html.Div([
            dbc.Row(
                [dbc.Col([
                    html.Div("Select planet main semi-axis range", className="selector", ),
                    html.Div(components.rplanet_selector)
                ], width={"size": 3, "offset": 0}),
                    dbc.Col([
                        html.Div("Select Star size", className="selector", ),
                        html.Div(components.star_size_selector)
                    ], width={"size": 3, "offset": 1}),
                    dbc.Col(dbc.Button("Apply all changes", id="btn-submit", outline=True, color="secondary",
                                       className="me-1", n_clicks=0), className="btn")
                ],
                className="main-selectors",
            ),
            dbc.Tabs([
                dbc.Tab(components.tab1_content, label="Charts"),
                dbc.Tab(components.tab2_content, label="Data"),
                dbc.Tab(components.tab3_content, label="About")
            ])
        ])
    ),

    # Footer
    html.Footer(
        dbc.Col([
            html.A(DashIconify(icon="ion:logo-github", width=30, ), href="https://github.com/dpaguba"),
            html.A("dpaguba", href="https://github.com/dpaguba")
        ], className="app-footer")
    )
])

""" CALLBACKS """


@app.callback(
    Output(component_id="filtered-data", component_property="data"),
    [Input(component_id="btn-submit", component_property="n_clicks")],
    [State(component_id="range-slider", component_property="value"),
     State(component_id="star-size-dropdown", component_property="value")]
)
def update_graph(radius_range, star_size):
    """
    The function is responsible for filtering the data.
    Filtered data is saved as json file and then used to apply changes to charts

    :param radius_range: selected radius range
    :param star_size: selected stars size
    :return:
    """

    graph_data: Union[Union[Series, DataFrame, None, NDFrame, data.ndarray], Any] = \
        data.df[(data.df["RPLANET"] > radius_range[0]) & (data.df["RPLANET"] < radius_range[1]) &
                (data.df["StarSize"].isin(star_size))]

    return graph_data.to_json(date_format="iso", orient="split", default_handler=str)


@app.callback(
    [Output(component_id="responsive-graph", component_property="children"),
     Output(component_id="celestial-graph", component_property="children"),
     Output(component_id="relative-dist-graph", component_property="children"),
     Output(component_id="mstar-tstar-graph", component_property="children"),
     Output(component_id="data-table", component_property="children")],
    Input(component_id="filtered-data", component_property="data")
)
def update_graph(chart_data):
    """
    the function builds graphs based on the data received
    from the function that filters (update_graph(radius_range, star_size)).

    also builds a table in tab "Data" with all raw data that was used to build the graphs

    :param chart_data: data about all charts
    :return:
    """

    graph_data = pd.read_json(chart_data, orient="split")

    if len(graph_data) == 0:
        return html.Div("Please select more data!",
                        style={"font-size": "250%", "margin-top": "40px"}), html.Div(), html.Div(), html.Div()

    fig1 = px.scatter(graph_data, x="TPLANET", y="A", color="StarSize")
    fig1.update_layout(template=components.CHARTS_TEMPLATE)
    html1 = [html.H5("Planet Temperature ~ Distance to the Star"), dcc.Graph(figure=fig1)]

    fig2 = px.scatter(graph_data, x="RA", y="DEC", size="RPLANET",
                      color="status", color_discrete_sequence=components.COLORS_STATUS_VALUES)
    fig2.update_layout(template=components.CHARTS_TEMPLATE)
    html2 = [html.H5("Position on the Celestial Sphere"), dcc.Graph(figure=fig2)]

    fig3 = px.histogram(graph_data, x="Relative_dist", color="status", barmode="overlay", marginal="violin")
    fig3.update_layout(template=components.CHARTS_TEMPLATE)
    fig3.add_vline(x=1, annotation_text="Earth", line_dash="dot")
    html3 = [html.H5("Relative Distance (AU/Sol radii)"), dcc.Graph(figure=fig3)]

    fig4 = px.scatter(graph_data, x="MSTAR", y="TSTAR", size="RPLANET",
                      color="status", color_discrete_sequence=components.COLORS_STATUS_VALUES)
    fig4.update_layout(template=components.CHARTS_TEMPLATE)
    html4 = [
        html.H5("Star Mass ~ Star Temperature"),
        dcc.Graph(figure=fig4)
    ]

    # Raw data table
    # delete added columns
    raw_data = graph_data.drop(["Relative_dist", "StarSize", "Gravity", "status", "Temp", "ROW"], axis=1)
    # build table, we change format of the graph data into a dictionary and then write the data into the table columns
    tbl = dash_table.DataTable(data=graph_data.to_dict("records"),
                               columns=[{"name": i, "id": i} for i in raw_data.columns],
                               style_data={"width": "93px", "maxWidth": "93px", "minWidth": "93px"},
                               style_header={"textAlign": "center"},
                               page_size=40
                               )

    html5 = [html.P("Raw Data"), tbl]

    return html1, html2, html3, html4, html5


if __name__ == "__main__":
    app.run_server(debug=True)
