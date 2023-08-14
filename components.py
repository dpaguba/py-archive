import data
from dash import dcc
from dash import html
import dash_bootstrap_components as dbc
import plotly.graph_objects as go

""" Slider """
rplanet_selector = dcc.RangeSlider(
    # slider id
    id="range-slider",

    # the minimum and maximum values will be taken from the data rplanet
    min=min(data.df["RPLANET"]),
    max=max(data.df["RPLANET"]),

    # marks
    marks={5: "5", 10: "10", 25: "25", 50: "50"},
    step=1,

    # default value
    value=[min(data.df["RPLANET"]), max(data.df["RPLANET"])]
)

""" Dropdown menu"""
star_size_selector = dcc.Dropdown(
    id="star-size-dropdown",
    options=data.options,
    value=["small", "similar", "bigger"],
    multi=True
)

""" Tabs """
tab1_content = [
    dbc.Row([
        dbc.Col([
            html.Div(id="responsive-graph")], md=6),
        dbc.Col([
            html.Div(id="celestial-graph")], md=6)], className="tabs"),
    dbc.Row([
        dbc.Col([
            html.Div(id="relative-dist-graph")
        ], md=6),
        dbc.Col([
            html.Div(id="mstar-tstar-graph")
        ], md=6)
    ])
]

tab2_content = [
    dbc.Row([
        html.Div(id="data-table")
    ])
]

table_header = [
    html.Thead(
        html.Tr([
            html.Th("Field Name"),
            html.Th("Details")
        ])
    )
]

""" Data Table """
expl = {
    "KOI": "Object of Interest number",
    "A": "Semi-major axis (AU)",
    "RPLANET": "Planetary radius (Earth radii)",
    "RSTAR": "Stellar radius (Sol radii)",
    "TSTAR": "Effective temperature of host star as reported in KIC (k)",
    "KMAG": "Kepler magnitude (kmag)",
    "TPLANET": "Equilibrium temperature of planet, per Borucki et al. (k)",
    "T0": "Time of transit center (BJD-2454900)",
    "UT0": "Uncertainty in time of transit center (+-jd)",
    "UT0": "Uncertainty in time of transit center (+-jd)",
    "PER": "Period (days)",
    "UPER": "Uncertainty in period (+-days)",
    "DEC": "Declination (@J200)",
    "RA": "Right ascension (@J200)",
    "MSTAR": "Derived stellar mass (msol)",
}

tbl_rows = []
for i in expl:
    tbl_rows.append(html.Tr([html.Td(i), html.Td(expl[i])]))

table_body = [html.Tbody(tbl_rows)]

table = dbc.Table(table_header + table_body, bordered=True)

text = "Data are sourced from Kepler API via asterank.com"
tab3_content = [
    dbc.Row([
        html.A(text, href="https://www.asterank.com/kepler")
    ], className="tabs"),
    dbc.Row(html.Div(children=table), className="tabs"),

]

""" Global design settings """
CHARTS_TEMPLATE = go.layout.Template(
    layout=dict(
        font=dict(family="Century Gothic",
                  size=14),
        legend=dict(orientation="h",
                    title_text="",
                    x=0, y=1.1)

    )
)

COLORS_STATUS_VALUES = ["lightgray", "#1f85de", "#22D744"]