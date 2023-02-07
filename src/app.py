import dash
from dash_bootstrap_components.themes import BOOTSTRAP
import plotly
import plotly.express as px
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output
import pandas as pd

import psycopg2
from sqlalchemy import create_engine
import dash_bootstrap_components as dbc
import json
from plotly.subplots import make_subplots
import plotly.graph_objects as go
import plotly.subplots as sp

# active the app
app = dash.Dash(
    __name__,
    external_stylesheets=[dbc.themes.CYBORG],
    suppress_callback_exceptions=True,
)
server = app.server

# styling....
SIDEBAR_STYLE = {
    "position": "fixed",
    "top": 0,
    "left": 0,
    "bottom": 0,
    "width": "11rem",
    "padding": "2rem 1rem",
    "background-color": "#c9c8c4",
}

H2_style = {"color": "#31364c", "font-size": "20px"}

P_style = {"color": "#31364c", "font-size": "14px"}

footer = {
    "bottom": 0,
    "position": "fixed",
    "width": "100%",
    "height": 50,
    "background-color": "#31364c",
    "margin-left": 160,
}

CONTENT_STYLE = {
    "margin-left": "0rem",
    "margin-right": "2rem",
    "padding": "1rem 1rem",
    "background": "#F4F4F1",
    "width": "100%",
    "height": "100%",
    "font-color": "white",
}
# pages
links = [
    {"id": "page-home-link", "href": "/", "link-text": "Germany"},
    {"id": "page-1-link", "href": "/plz1", "link-text": "Example single Data Centre"},
    {"id": "page-3-link", "href": "/plz5", "link-text": "Confidential"},
    {"id": "page-3-link", "href": "/plz2", "link-text": "Impressum"}

]
# sidebar
sidebar = html.Div(
    [
        html.H4(
            "Energyefficiency Register for Data Centres",
            className="display-4",
            style=H2_style,
        ),
        html.Hr(),
        html.P("", className="lead", style=P_style),
        # the nach component has nav links, active it was makes it looks active
        dbc.Nav(
            [
                dbc.NavItem(
                    dbc.NavLink(
                        link["link-text"],
                        href=link["href"],
                        id=link["id"],
                        active="exact",
                    )
                )
                for link in links
            ],
            vertical=True,
            pills=True,
        ),
    ],
    style=SIDEBAR_STYLE,
)

content = html.Div(id="page-content", children=[], style=CONTENT_STYLE)

# app layout
app.layout = html.Div(
    [
        dcc.Location(id="url"),
        sidebar,
        content,
    ]
)

# db connection
mydb = psycopg2.connect(
    database="dc_register_ukaa",
    user="dc_register_ukaa_user",
    password="5T1EESdCVAxqGwNmMrYP3ealUoVPFbsb",
    host="dpg-cfh56ehgp3jqehpsocmg-a.oregon-postgres.render.com",
    port="5432",
)

# using json_build_object query to create a FeatureCollection
# geodata = pd.read_sql(
#   """SELECT jsonb_build_object('type','FeatureCollection','features', jsonb_agg(features.feature))FROM (SELECT jsonb_build_object('type','Feature',
# 'id', plz1,'geometry',ST_AsGeoJSON(geom)::jsonb,'properties', to_jsonb(inputs) - 'geom') AS feature FROM (SELECT * FROM plz1) inputs) features;""",
#    mydb,
# )

# geodata = pd.read_sql(
#    """SELECT jsonb_build_object('type','FeatureCollection','features', jsonb_agg(features.feature))FROM (SELECT jsonb_build_object('type','Feature',
# 'id_0', plz1,id,plz2,id_1,plz3,'geometry',ST_AsGeoJSON(geom)::jsonb,'properties', to_jsonb(inputs) - 'geom') AS feature FROM (SELECT * FROM plz123) inputs) features;""",
#   mydb,
# )

# saving the feature collection in a dict
# geodata_dict = geodata.iloc[0]["jsonb_build_object"]

# write dict to json
# with open("test.json", "w") as outfile:
#   json.dump(geodata_dict, outfile)

# read json
with open("test.json") as f:
    data = json.load(f)

# using view kpi
df = pd.read_sql("""SELECT * from kpi_v2""", mydb)

#
# plz11=pd.read_sql("""SELECT * from kpi_v2 where plz1='1'""",mydb)
plz11 = pd.read_sql("""SELECT * from kpi_v2 where plz2='13'""", mydb)
plz12 = pd.read_sql("""SELECT * from kpi_v2 where plz1='2'""", mydb)
plz13 = pd.read_sql("""SELECT * from kpi_v2 where plz1='3'""", mydb)
plz14 = pd.read_sql("""SELECT * from kpi_v2 where plz1='4'""", mydb)
plz15 = pd.read_sql("""SELECT * from kpi_v2 where plz1='5'""", mydb)
plz16 = pd.read_sql("""SELECT * from kpi_v2 where plz1='6'""", mydb)
plz17 = pd.read_sql("""SELECT * from kpi_v2 where plz1='7'""", mydb)
plz18 = pd.read_sql("""SELECT * from kpi_v2 where plz1='8'""", mydb)
plz19 = pd.read_sql("""SELECT * from kpi_v2 where plz1='9'""", mydb)
plz10 = pd.read_sql("""SELECT * from kpi_v2 where plz1='0'""", mydb)

dfs = [df, plz11, plz12, plz13, plz14, plz15, plz16, plz17, plz18, plz19, plz10]

for i in dfs:
    i = i.rename(
        columns={
            "pue": "Power Usage Effectiveness",
            "erf": "Energy Reuse Factor",
            "wue": "Water Usage Effectiveness",
            "cer": "Cooling Efficiency Ratio",
            "ref": "Renewable Energy Factor",
        }, inplace=True
    )

OPTIONS = [
    "Power Usage Effectiveness",
    "Energy Reuse Factor",
    "Water Usage Effectiveness",
    "Cooling Efficiency Ratio",
    "Renewable Energy Factor",
]

all_options = {
    'default': ['d', 'd', 'd'],
    '1': ['12', '13', '14', '15', '16', '17', '18', '10'],
    '2': [u'21', '23', '24', '25', '26', '27', '28', '29', '19'],
    '3': [u'31', '32', '34', '35', '36', '37', '38', '39', '30'],
    '4': [u'41', '42', '43', '45', '46', '47', '48', '49', '40'],
    '5': [u'51', '52', '53', '54', '56', '57', '58', '59', '50'],
    '6': [u'61', '62', '63', '64', '65', '67', '68', '69', '60'],
    '7': [u'71', '72', '73', '74', '75', '76', '78', '79', '70'],
    '8': [u'81', '82', '83', '84', '85', '86', '87', '89', '80'],
    '9': [u'91', '92', '93', '94', '95', '96', '97', '98', '90'],
    '0': [u'01', '02', '03', '04', '05', '06', '07', '08', '09'],
}


@app.callback(
    Output('zweistellig', 'options'),
    Input('var_data', 'value'))
def set_cities_options(selected_country):
    return [{'label': i, 'value': i} for i in all_options[selected_country]]


# choropleth map
@app.callback(Output(component_id="my-graph", component_property="figure"),
              [Input(component_id="var_choice", component_property="value"),
               Input(component_id="var_data", component_property="value"),
               Input('zweistellig', 'value'),
               ])
def update_figure(var_choice, var_data, zweistellig):
    def genereatecolorscale(text):
        if text == "Power Usage Effectiveness":
            return (1, 3)
        if text == "Energy Reuse Factor":
            return (0, 8)
        if text == "Water Usage Effectiveness":
            return (0, 10)
        if text == "Cooling Efficiency Ratio":
            return (0, 12)
        if text == "Renewable Energy Factor":
            return (0, 1)
        else:
            return (1, 6)

    def generatedata(text, text2):
        if text == "1":
            if text2 == "13":
                return plz11
            else:
                return plz11
        if text == "2":
            return plz12
        if text == "3":
            return plz13
        if text == "4":
            return plz14
        if text == "5":
            return plz15
        if text == "6":
            return plz16
        if text == "7":
            return plz17
        if text == "8":
            return plz18
        if text == "9":
            return plz19
        if text == "0":
            return plz10
        else:
            return df

    def generateloc(text, text2):
        if text2 == "13":
            return "plz3"
        else:
            if text == "default":
                return "plz1"
            if text == "1":
                return "plz2"
            else:
                return "plz1"

    def generateid(text, text2):
        if text2 == "13":
            return "properties.plz3"
        else:
            if text == "default":
                return "properties.plz1"
            if text == "1":
                return "properties.plz2"
            else:
                return "properties.plz1"

    def generatezoom(text, text2):
        if text2 == "13":
            return 10
        if text == "1":
            return 8
        else:
            return 4

    def generatelatlong(text, text2):
        if text2 == "13":
            return {"lat": 52.520008, "lon": 13.404954}
        if text == "1":
            return {"lat": 52.520008, "lon": 13.404954}
        else:
            return {"lat": 50.1109, "lon": 13.404954}

    depp = generatedata(var_data, zweistellig)
    loc = generateloc(var_data, zweistellig)
    idd = generateid(var_data, zweistellig)
    range = genereatecolorscale(var_choice)
    zoom = generatezoom(var_data, zweistellig)
    coord = generatelatlong(var_data, zweistellig)

    fig = px.choropleth_mapbox(
        data_frame=depp,
        geojson=data,
        locations=loc,
        color=var_choice,
        featureidkey=idd,
        color_continuous_scale="balance",
        opacity=0.5,
        hover_data=['dc_id'],
        range_color=range,
        mapbox_style="open-street-map",
        zoom=zoom,
        center=coord,
    )

    fig.update_geos(fitbounds="locations")

    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        width=600,
        margin=dict(l=0, r=30, t=10, b=10),
        legend_font_color="#31364c",
        font_color="#31364c",
        coloraxis_colorbar=dict(title=""),
    )
    return fig


with open("vaihingen.json") as f:
    vai = json.load(f)

vai_data = pd.read_csv("kpi.csv")

vai_data.rename(
    columns={
        "pue": "Power Usage Effectiveness",
        "erf": "Energy Reuse Factor",
        "wue": "Water Usage Effectiveness",
        "cer": "Cooling Efficiency Ratio",
        "ref": "Renewable Energy Factor",
    }, inplace=True)

print(vai_data)

OPTIONS = [
    "Power Usage Effectiveness",
    "Energy Reuse Factor",
    "Water Usage Effectiveness",
    "Cooling Efficiency Ratio",
    "Renewable Energy Factor",
]


# choropleth map 5 stellig
@app.callback(Output(component_id="my-graph2", component_property="figure"),
              Input(component_id="var_choice", component_property="value"), )
def update_figure(var_choice):
    def genereatecolorscale(text):
        if text == "Power Usage Effectiveness":
            return (1, 3)
        if text == "Energy Reuse Factor":
            return (0, 8)
        if text == "Water Usage Effectiveness":
            return (0, 10)
        if text == "Cooling Efficiency Ratio":
            return (0, 12)
        if text == "Renewable Energy Factor":
            return (0, 1)
        else:
            return (1, 6)

    range = genereatecolorscale(var_choice)

    fig = px.choropleth_mapbox(
        data_frame=vai_data,
        geojson=vai,
        locations="plz5",
        color=var_choice,
        featureidkey="properties.plz5",
        color_continuous_scale="balance",
        opacity=0.5,
        range_color=range,
        mapbox_style="open-street-map",
        zoom=8,
        center={"lat": 48.745837, "lon": 9.105398},
    )

    fig.update_geos(fitbounds="locations")

    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        width=600,
        margin=dict(l=0, r=30, t=10, b=10),
        legend_font_color="#31364c",
        font_color="#31364c",
        coloraxis_colorbar=dict(title=""),
    )
    return fig


el_share_1 = pd.read_sql(
    """select avg(electricity_supply.el_share_renewables) as reneweables,avg(electricity_supply.el_share_nuclear) as nuclear,avg(electricity_supply.el_share_fossil) as fossil
from electricity_supply""",
    mydb,
)

values = [40.4, 56.6, 6.0]
labels = ['Renewable energy', 'Nuclear energy', 'Fossil energy']
print(values)

fig_share = px.pie(el_share_1, values=values, names=labels, color_discrete_sequence=px.colors.sequential.ice,
                   opacity=0.6)
fig_share.update_layout(margin=dict(l=50, r=50, t=19, b=19),
                        font=dict(size=10, color="#31364c"), width=350,
                        height=259, title="Data Centre Electricity Mix",
                        plot_bgcolor="rgba(0,0,0,0)",
                        paper_bgcolor="rgba(0,0,0,0)",
                        legend=dict(
                            yanchor="top",
                            xanchor="left",
                        ),
                        )

# gaucharts
gau = make_subplots(rows=1, cols=5, horizontal_spacing=0.25)
gau = go.Figure()

gau.add_trace(
    go.Indicator(
        value=1.2,
        title={"text": "PUE", "font": {"size": 14}, },
        name="wssss",
        gauge={
            "bgcolor": "red",
            "axis": {"range": [1, 3]},
            "steps": [
                {"range": [1, 1.3], "color": "green"},
                {"range": [1.3, 1.8], "color": "yellow"},
                {"range": [1.8, 2.2], "color": "orange"},
                {"range": [2.2, 3], "color": "red"},
            ],
        },
        domain={"row": 0, "column": 0},
    )
)

gau.add_trace(
    go.Indicator(
        value=0.08,
        title={"text": "ERF", "font": {"size": 14}},
        gauge={
            "axis": {"range": [1, 0]},
            "bar": {"color": "blue", "thickness": 0.0},
            "steps": [
                {"range": [0, 0.1], "color": "darkred"},
                {"range": [0.1, 0.3], "color": "red"},
                {"range": [0.3, 0.6], "color": "darkorange"},
                {"range": [0.6, 0.8], "color": "orange"},
                {"range": [0.8, 1], "color": "green"},
            ],
        },
        domain={"row": 1, "column": 0},
    )
)

gau.add_trace(
    go.Indicator(
        value=10,
        title={"text": "CER", "font": {"size": 14}},
        gauge={
            "axis": {"range": [12, 1]},
            "bar": {"color": "blue", "thickness": 0.0},
            "steps": [
                {"range": [1, 3], "color": "darkred"},
                {"range": [3, 4], "color": "red"},
                {"range": [4, 6], "color": "darkorange"},
                {"range": [6, 8], "color": "orange"},
                {"range": [8, 10], "color": "darkgreen"},
                {"range": [10, 12], "color": "green"},
            ],
        },
        domain={"row": 0, "column": 1},
    )
)

gau.add_trace(
    go.Indicator(
        value=0.5,
        title={"text": "REF", "font": {"size": 14}},
        gauge={
            "axis": {"range": [1, 0]},
            "bar": {"color": "blue", "thickness": 0.0},
            "steps": [
                {"range": [0, 0.1], "color": "darkred"},
                {"range": [0.1, 0.3], "color": "red"},
                {"range": [0.3, 0.6], "color": "darkorange"},
                {"range": [0.6, 0.8], "color": "orange"},
                {"range": [0.8, 1], "color": "green"},
            ],
        },
        domain={"row": 1, "column": 1},
    )
)

gau.add_trace(
    go.Indicator(
        value=0.002,
        title={"text": "WUE", "font": {"size": 14}},
        gauge={
            "axis": {"range": [1, 0]},
            "bar": {"color": "blue", "thickness": 0.0},
            "steps": [
                {"range": [0, 0.1], "color": "darkred"},
                {"range": [0.1, 0.3], "color": "red"},
                {"range": [0.3, 0.6], "color": "darkorange"},
                {"range": [0.6, 0.8], "color": "orange"},
                {"range": [0.8, 1], "color": "green"},
            ],
        },
        domain={"row": 1, "column": 2},
    )
)

gau.update_layout(
    plot_bgcolor="rgba(0,0,0,0)",
    paper_bgcolor="rgba(0,0,0,0)",
    height=260,
    width=500,
    margin=dict(l=22, r=30, t=50, b=10),
    font_color="#31364c",
    grid={"rows": 2, "columns": 3, "pattern": "independent"},
    template={
        "data": {
            "indicator": [
                {'title': {'text': "Speed"},
                 "mode": "number+gauge",
                 "number": {"font": {"size": 30}},
                 }
            ]
        }
    },
)

# size_class=pd.read_sql('''select count(dc_it_nominal_power_kw) as anzahl, class
# from size_class group by class''',mydb)

classes = ["<100kW", "<500kW", "<1MW", "<5MW", "<10MWW", "<100MW", ">=100MW"]
anzahl = [100, 90, 19, 0, 0, 0, 1]

it_conn = px.bar(

    x=classes,
    y=anzahl,
    labels={
        "classes": "Size class according to IT connected load",
    },

)
it_conn.update_layout(margin=dict(l=60, r=50, t=21, b=19),
                      font=dict(size=10, color="#31364c"), width=300,
                      height=250, title="Number of Data Centres by Size",
                      plot_bgcolor="rgba(0,0,0,0)",
                      paper_bgcolor="rgba(0,0,0,0)",
                      xaxis_title="",

                      legend=dict(
                          yanchor="top",
                          xanchor="left",

                      ), yaxis_title=None, )

it_conn.update_yaxes(visible=True, showticklabels=True)

it_conn.update_xaxes(type='category')

# sql following....
connect_power_kw = pd.read_sql(
    """select sum(dc.dc_connection_power_kw)/1000 as sum, 
"left"(dc.dc_zipcode, 1) AS plz1
from dc
group by plz1
order by plz1""",
    mydb,
)

connect_power_kw2 = pd.read_sql(
    """select sum(dc.dc_connection_power_kw)/1000 as sum, 
"left"(dc.dc_zipcode, 2) AS plz2
from dc
where dc.dc_zipcode like '1%'
group by plz2
order by plz2""",
    mydb,
)

el_consumption_kw = pd.read_sql(
    """select "left"(dc.dc_zipcode, 1) AS plz1,sum(electricity_consumption.el_total_dc_kwh),electricity_consumption.el_consumption_year as year
from dc, electricity_consumption
where dc.dc_id = electricity_consumption.dc_id
group by plz1,year""",
    mydb,
)

el_consumption_kw2 = pd.read_sql(
    """select "left"(dc.dc_zipcode, 2) AS plz2,sum(electricity_consumption.el_total_dc_kwh),electricity_consumption.el_consumption_year as year
from dc, electricity_consumption
where dc.dc_id = electricity_consumption.dc_id and dc.dc_zipcode like '1%'
group by plz2,year""",
    mydb,
)

emission_co2 = pd.read_sql(
    """select  "left"(dc.dc_zipcode, 1) AS plz1,sum(((coolant_consumption.coolant_refilled_kg - coolant_consumption.coolant_disposed_kg) * coolant_type.emission_f) /10 ) as emission,coolant_consumption_year as year
from coolant_consumption,coolant_type,dc,chiller
WHERE coolant_consumption.coolant_type_id = coolant_type.coolant_type_id AND chiller.dc_id = dc.dc_id AND coolant_consumption.chiller_id = chiller.chiller_id
GROUP BY plz1,year""",
    mydb,
)

emission_co22 = pd.read_sql(
    """select  "left"(dc.dc_zipcode, 2) AS plz2,sum(((coolant_consumption.coolant_refilled_kg - coolant_consumption.coolant_disposed_kg) * coolant_type.emission_f) /10 ) AS emission,coolant_consumption_year as year
from coolant_consumption,coolant_type,dc,chiller
WHERE coolant_consumption.coolant_type_id = coolant_type.coolant_type_id AND chiller.dc_id = dc.dc_id AND coolant_consumption.chiller_id = chiller.chiller_id
GROUP BY plz2,year""",
    mydb,
)
# sql done
new_df = pd.merge(
    el_consumption_kw, emission_co2, how="left", left_on=["plz1"], right_on=["plz1"]
)
new_df2 = pd.merge(
    el_consumption_kw2, emission_co22, how="left", left_on=["plz2"], right_on=["plz2"]
)
print(new_df)
emisssion_randmon = [250000, 76000, 30000, 70000]


@app.callback(
    Output(component_id="the_graph", component_property="figure"),
    [Input(component_id="yaxis_raditem", component_property="value"),
     Input('var_data', 'value')],
)
def update_graph(y_axis, text2):
    if text2 == '1':
        dff2 = new_df2
        barchart = px.bar(
            data_frame=dff2,
            x="plz2",
            y=y_axis,
            color="year_x",
            color_discrete_map={
                "2020": "rgba(141, 29, 37,0.9)",
                "2021": "rgba(101,142,177,0.6)",
            },
            barmode="group",
            labels={
                "plz2": "Postcode Regions 2-digits Germany",
                "sum": "[kWh/year]",
                "emission": "[t CO2 eq]",
                "year_x": "Year",
            },

        )

        barchart.add_traces(
            go.Scatter(x=new_df2["plz2"], y=new_df["emission"], mode='markers', yaxis="y2", name="[t CO2 eq]",
                       marker=dict(
                           color='darkblue',
                           size=12,
                           line=dict(
                               color='darkblue',
                               width=2
                           )))),

        barchart.update_layout(
            {"plot_bgcolor": "rgba(0, 0, 0, 0)", "paper_bgcolor": "rgba(0, 0, 0, 0)"},
            barmode="group",
            title={
                "xanchor": "center",
                "yanchor": "top",
                "y": 0.9,
                "x": 0.5,
            },

            margin=dict(l=10, r=10, t=10, b=10),
            font=dict(size=10, color="#31364c"),
            yaxis=dict(
                titlefont=dict(color="#31364c"),
                tickfont=dict(color="#31364c")),

            # create 2nd y axis      
            yaxis2=dict(overlaying="y", side="right", titlefont=dict(color="#31364c"),
                        tickfont=dict(color="#31364c"), title_text="[t CO2 eq]"), )
        barchart.update_yaxes(tickformat=".2s")
        barchart.update_layout(legend=dict(
            orientation="h",

            y=1.2

        ))
        return barchart
    else:
        dff = new_df
        barchart = px.bar(
            data_frame=dff,
            x="plz1",
            y=y_axis,
            color="year_x",
            color_discrete_map={
                "2020": "rgba(141, 29, 37,0.9)",
                "2021": "rgba(101,142,177,0.6)",
            },
            barmode="group",
            labels={
                "plz1": "Postcode Regions 1-digit Germany",
                "sum": "[kWh/year]",
                "emission": "[t CO2 eq]",
                "year_x": "Year",
            },
            category_orders={"plz1": ["1", "2", "3", "4", "5", "6", "7", "8", "9"]},
        )

        barchart.add_traces(
            go.Scatter(x=new_df["plz1"], y=new_df["emission"], mode='markers', yaxis="y2", name="CO2 emissions",
                       marker=dict(
                           color='darkblue',
                           size=12,
                           line=dict(
                               color='darkblue',
                               width=2
                           )))),

        barchart.update_layout(
            {"plot_bgcolor": "rgba(0, 0, 0, 0)", "paper_bgcolor": "rgba(0, 0, 0, 0)"},
            barmode="group",
            title={
                "xanchor": "center",
                "yanchor": "top",
                "y": 0.9,
                "x": 0.5,
            },

            margin=dict(l=10, r=10, t=10, b=10),
            font=dict(size=10, color="#31364c"),
            yaxis=dict(
                titlefont=dict(color="#31364c"),
                tickfont=dict(color="#31364c")),

            # create 2nd y axis      
            yaxis2=dict(overlaying="y", side="right", titlefont=dict(color="#31364c"),
                        tickfont=dict(color="#31364c"), title_text="[t CO2 eq]"), )
        barchart.update_yaxes(tickformat=".2s", )

        barchart.update_layout(legend=dict(
            orientation="h",

            y=1.2

        ))
        return barchart


colo = [130, 130, 230, 30, 30, 30, 30, 130, 130, ]
enter = [140, 40, 140, 40, 140, 240, 40, 40, 40, ]
hosting = [55, 60, 19, 19, 44, 100, 70, 80, 33]
network = [100, 60, 19, 19, 44, 100, 70, 80, 33]


@app.callback(
    Output(component_id="the_graph_2", component_property="figure"),
    Input('var_data', 'value'),
)
def update_graph(text2):
    if text2 == '1':

        trace1 = go.Figure(go.Bar(
            x=connect_power_kw2["plz2"],
            y=colo, name='Colocation',
            hovertemplate=("<i>Connection Power</i>: %{y:}<i>MW</i><extra></extra>"),
            marker_color="#6688BD",
            marker_line_color="#6d94b0",
            marker_line_width=1.5,
        ))

        trace1.add_trace(go.Bar(x=connect_power_kw2["plz2"],
                                y=enter, name='Enterprise',
                                hovertemplate=("<i>Connection Power</i>: %{y:}<i>MW</i><extra></extra>"),
                                marker_color="#9EBAC6",
                                marker_line_color="#6d94b0",
                                marker_line_width=1.5, ))

        trace1.add_trace(go.Bar(x=connect_power_kw2["plz2"],
                                y=hosting, name='Hosting',
                                hovertemplate=("<i>Connection Power</i>: %{y:}<i>MW</i><extra></extra>"),
                                marker_color="#A15258",
                                marker_line_color="#A15258",
                                marker_line_width=1.5, ))

        trace1.add_trace(go.Bar(x=connect_power_kw2["plz2"],
                                y=network, name='Network',
                                hovertemplate=("<i>Connection Power</i>: %{y:}<i>MW</i><extra></extra>"),
                                marker_color="#1D2351",
                                marker_line_color="#1D2351",
                                marker_line_width=1.5, ))

        trace1.update_layout(
            width=460,
            height=230,
            margin=dict(l=10, r=10, t=50, b=10),
            plot_bgcolor="rgba(0,0,0,0)",
            paper_bgcolor="rgba(0,0,0,0)",
            barmode='stack',
            font=dict(size=10, color="#31364c"),
            title="Non-redundant power supply of Data Centres"
        )

        trace1.update_yaxes(title='[MW]')
        trace1.update_xaxes(title='Postcode Regions 2-digits Germany')
        return trace1
    else:
        trace1 = go.Figure(go.Bar(
            x=connect_power_kw["plz1"],
            y=colo, name='Colocation',
            hovertemplate=("<i>Connection Power</i>: %{y:}<i>MW</i><extra></extra>"),
            marker_color="#6688BD",
            marker_line_color="#6d94b0",
            marker_line_width=1.5,
        ))
        trace1.add_trace(go.Bar(x=connect_power_kw["plz1"],
                                y=enter, name='Enterprise',
                                hovertemplate=("<i>Connection Power</i>: %{y:}<i>MW</i><extra></extra>"),
                                marker_color="#9EBAC6",
                                marker_line_color="#6d94b0",
                                marker_line_width=1.5, ))
        trace1.add_trace(go.Bar(x=connect_power_kw["plz1"],
                                y=hosting, name='Hosting',
                                hovertemplate=("<i>Connection Power</i>: %{y:}<i>MW</i><extra></extra>"),
                                marker_color="#A15258",
                                marker_line_color="#A15258",
                                marker_line_width=1.5, ))

        trace1.add_trace(go.Bar(x=connect_power_kw["plz1"],
                                y=network, name='Network',
                                hovertemplate=("<i>Connection Power</i>: %{y:}<i>MW</i><extra></extra>"),
                                marker_color="#1D2351",
                                marker_line_color="#1D2351",
                                marker_line_width=1.5, ))

        trace1.update_layout(
            width=460,
            height=230,
            margin=dict(l=10, r=10, t=50, b=10),
            plot_bgcolor="rgba(0,0,0,0)",
            paper_bgcolor="rgba(0,0,0,0)",
            barmode='stack',
            font=dict(size=10, color="#31364c"),
            title="Non-redundant power supply of Data Centres",
        )

        trace1.update_yaxes(title='[MW]')
        trace1.update_xaxes(title='Postcode Regions 1-digit Germany')
        return trace1


table_data = pd.read_csv("hlrs.csv")

table = go.Figure(data=[go.Table(header=dict(values=['HLRS Stuttgart']),
                                 cells=dict(values=[
                                     ["Art der baulichen Nutzung des Umfelds", "Verfügbarkeitsklasse", "Zertifikate",
                                      "Anschlussleistung", "Grundstücksfläche", "Gebäudefläche", "Whitespace"], []]))
                        ])

table.update_layout(width=500, height=300, margin=dict(l=50, r=50, t=40, b=19), plot_bgcolor="rgba(0,0,0,0)",
                    paper_bgcolor="rgba(0,0,0,0)", )

# sql
heat = pd.read_sql(
    """select "left"(dc.dc_zipcode, 1) AS plz1, sum(heat_use.heat_reuse_kwh) as used,sum(heat_use.heat_unuse_kwh) as unused
from heat_use,dc
where dc.dc_id = heat_use.dc_id
group by plz1
order by plz1""",
    mydb,
)

heat2 = pd.read_sql("""select "left"(dc.dc_zipcode, 2) AS plz2, sum(heat_use.heat_reuse_kwh) as used,sum(heat_use.heat_unuse_kwh) as unused
from heat_use,dc
where dc.dc_id = heat_use.dc_id and dc.dc_zipcode like '1%'
group by plz2
order by plz2""", mydb)

demand = [10000, 100000, 10000, 100000, 100000, 100000, 100000, 10000, 10000, 10000]

used = heat["used"].to_numpy()
unused = heat["used"].to_numpy()
plz1 = heat["plz1"].to_numpy()

used2 = heat2["used"].to_numpy()
unused2 = heat2["used"].to_numpy()
plz2 = heat2["plz2"].to_numpy()


@app.callback(
    Output(component_id="heat_graph", component_property="figure"),
    Input('var_data', 'value'),
)
def update_graph(text2):
    if text2 == '1':
        fig = go.Figure()
        fig.add_trace(
            go.Barpolar(
                r=used2,
                name="Used",
                marker_color="rgba(141, 29, 37,0.9)",
            )
        )
        fig.add_trace(
            go.Barpolar(
                r=unused2,
                name="Unused",
                marker_color="#262a6c",
            )
        )
        fig.add_trace(
            go.Barpolar(r=demand, name="Heat Demand", marker_color="rgba(18, 91, 177,0.6)")
        )
        fig.update_traces(theta=plz2)
        fig.update_layout(
            title={
                'text': "Potential Waste heat availability from Data Centres <br>(Postcode Area 2-digit Germany)",
                'y': 0.95,
                'x': 0.5,
                'xanchor': 'center',
                'yanchor': 'top'},
            width=800,
            height=300,
            margin=dict(l=0, r=0, t=50, b=0),
            # title="Waste Heat for each Postcode Region 1-digit Germany",
            plot_bgcolor="rgba(0,0,0,0)",
            paper_bgcolor="rgba(0,0,0,0)",
            legend=dict(yanchor="top", y=0.9, xanchor="right", x=0.8),
            font=dict(size=10, color="#31364c"),
            polar=dict(radialaxis=dict(showticklabels=False)),
        )
        return fig
    else:
        fig = go.Figure()
        fig.add_trace(
            go.Barpolar(
                r=used,
                name="Used",
                marker_color="rgba(141, 29, 37,0.9)",
            )
        )
        fig.add_trace(
            go.Barpolar(
                r=unused,
                name="Unused",
                marker_color="#262a6c",
            )
        )
        fig.add_trace(
            go.Barpolar(r=demand, name="Heat Demand", marker_color="rgba(18, 91, 177,0.6)")
        )
        fig.update_traces(theta=plz1)
        fig.update_layout(
            title={
                'text': "Potential Waste heat availability from Data Centres <br>(Postcode Area 1-digit Germany)",
                'y': 0.95,
                'x': 0.5,
                'xanchor': 'center',
                'yanchor': 'top'},
            width=800,
            height=300,
            margin=dict(l=0, r=0, t=50, b=20),
            # title="Waste Heat for each Postcode Region 1-digit Germany",
            plot_bgcolor="rgba(0,0,0,0)",
            paper_bgcolor="rgba(0,0,0,0)",
            legend=dict(yanchor="top", y=0.9, xanchor="right", x=0.8),
            font=dict(size=10, color="#31364c"),
            polar=dict(radialaxis=dict(showticklabels=False)),
        )
        return fig


# creates content based on the link
@app.callback(Output("page-content", "children"), [Input("url", "pathname")])
def render_page_content(
        pathname,
):  # pathname is just the / after the port thats why its loading...http://127.0.0.1:8050/
    if pathname == "/":
        return [
            html.Div(
                [
                    html.Div(
                        [
                            html.Div(
                                [
                                    html.Label(
                                        "The map section shows KPIs (Key Performance Indicators) for evaluating the energy efficiency of data centers in a choropleth map. The map is divided into postal code areas. The coarsest resolution shows the areas at the single-digit postal code level. The small resolution shows the desired areas of the 5-digit postal code range. ",
                                        style={"width": "880px", "font-size": "12px", "color": "#31364c"}

                                    ),
                                    html.Label(
                                        "Select the KPI and the Postcode Region from the drop-down menu.",
                                        style={
                                            "margin-top": "10px",
                                            "color": "#31364c",
                                            "font-weight": "bold",
                                        },
                                    ),

                                    dcc.Dropdown(
                                        id="var_choice",
                                        value="Power Usage Effectiveness",
                                        options=[
                                            {"label": i, "value": i} for i in OPTIONS
                                        ],
                                        # optionHeight=19,
                                        style={
                                            "background-color": "#121212",
                                            "color": "black",
                                            "font-size": "12px",
                                            "height": "30px",
                                            # "margin-top":"50px"
                                        },
                                    ),

                                    dcc.Dropdown(id="var_data", value="default", optionHeight=19,

                                                 options=[{"label": i, "value": i} for i in
                                                          ['1', '2', '3', '4', '5', '6', '7', '8', '9']],
                                                 style={"font-size": "12px",
                                                        "height": "30px"}
                                                 ),

                                    dcc.Dropdown(id="zweistellig", style={"font-size": "12px",
                                                                          "height": "30px"}),
                                    dcc.Graph(id="my-graph"),

                                ],
                                className="six columns",
                                style={
                                    "position": "absolute",
                                    "width": 400,
                                    "margin-top": 0,
                                    "margin-left": 180,
                                    "display": "inline-block",
                                    "height": "auto",
                                    "background-color": "#F4F4F1",
                                },
                            ),
                            dbc.Button("Info", href="/",
                                       style={"margin-left": "580px", "width": "100px", "margin-top": "114px",
                                              "height": "35px", "font-size": "12px"}),

                            html.Div(
                                [
                                    html.Br(),
                                    dcc.RadioItems(
                                        id="yaxis_raditem",
                                        options=[
                                            {
                                                "label": html.Div(
                                                    ["Electricity Production Data Centres"],
                                                    style={
                                                        "display": "flex",
                                                        "align-items": "center",
                                                        "justify-content": "center",
                                                        "margin-top": "-20px",
                                                        "margin-left": "20px",
                                                        "padding-right": "20px",
                                                    },
                                                ),
                                                "value": "emission",
                                            },
                                            {
                                                "label": html.Div(
                                                    [
                                                        "Electricity Consumption Data Centres",
                                                    ],
                                                    style={
                                                        "display": "flex",
                                                        "align-items": "center",
                                                        "justify-content": "center",
                                                        "margin-left": "20px",
                                                        "margin-top": "-20px",
                                                    },
                                                ),
                                                "value": "sum",
                                            },
                                        ],
                                        inline=True,
                                        value="sum",
                                        style={
                                            "font-size": "13px",
                                            "width": "800px",
                                            "margin-top": "-100px",
                                            "margin-left": "750px",
                                            # "position": "relative",
                                            "font-family": "Helvetica",
                                            "color": "#31364c",
                                        },
                                    ),
                                ],
                                className="six columns",
                            ),
                            html.Div(
                                dcc.Graph(
                                    id="the_graph",
                                    className="six columns",
                                    style={
                                        # "padding-top": "0px",
                                        "margin-left": "760px",
                                        "width": 450,
                                        "margin-top": "-50px",
                                        "height": 200,
                                        "background-color": "#F4F4F1",
                                        "font-size": "14px"
                                    },
                                ),
                                className="six columns",
                            ),
                            html.Div(dcc.Graph(id="the_graph_2",
                                               style={"width": 400, "height": 200, "margin-left": "780px"})),
                            html.Div(
                                dcc.Graph(
                                    id="heat_graph",

                                    style={
                                        "margin-left": "580px",
                                        "margin-top": "80px",

                                    },
                                )
                            ),
                            html.Div(dcc.Graph(id="share", figure=fig_share),
                                     style={"width": 390, "height": 200, "margin-left": "160px",
                                            "margin-top": "-200px"}, ),
                            html.Div(dcc.Graph(id="class", figure=it_conn),
                                     style={"width": 300, "height": 150, "margin-top": "-200px",
                                            "margin-left": "-100px"}),
                        ],
                        className="row",
                        style={"font-color": "red"},
                    )
                ]
            ),
        ]
    elif pathname == "/plz1":
        return [
            html.Div(
                [
                    html.Div(
                        [
                            html.Div(
                                [
                                    html.Label(
                                        "HLRS Universität Stuttgart", style=H2_style),
                                    dcc.Dropdown(
                                        id="var_choice",
                                        value="Power Usage Effectiveness",
                                        options=[
                                            {"label": i, "value": i} for i in OPTIONS
                                        ],
                                        # optionHeight=19,
                                        style={
                                            "background-color": "#121212",
                                            "color": "black",
                                        },
                                    ),
                                    dcc.Dropdown(
                                        id="var_data",
                                        value="default",
                                        optionHeight=19,
                                        options=[
                                            {"label": i, "value": i}
                                            for i in [
                                                "1",
                                                "2",
                                                "3",
                                                "4",
                                                "5",
                                                "6",
                                                "7",
                                                "8",
                                                "9",
                                            ]
                                        ],
                                    ),
                                    dcc.Graph(id="my-graph2"),

                                ],
                                className="six columns",
                                style={
                                    "position": "absolute",
                                    "width": 400,
                                    "margin-top": 0,
                                    "margin-left": 180,
                                    "display": "inline-block",
                                    "height": "auto",
                                    "background-color": "#F4F4F1",
                                },
                            ),

                            html.Div(
                                dcc.Graph(id="tik2", figure=gau),
                                className="six columns",
                                style={
                                    "width": 200,
                                    "margin-left": 580,
                                    "display": "inline-block",
                                    "height": 500,
                                },
                            ),
                            html.Div(
                                [

                                ],
                                className="six columns",
                            ),
                            html.Div(
                                dcc.Graph(
                                    id="test", figure=table,
                                    className="six columns",
                                    style={
                                        "padding-top": "0px",
                                        "margin-left": "500px",
                                        "width": 550,
                                        "margin-top": "-250px",
                                        "height": 250,
                                        "background-color": "#F4F4F1",
                                    },
                                ),
                                className="six columns",
                            ),

                        ],
                        className="row",
                        style={"font-color": "red"},
                    )
                ]
            ),
        ]
    elif pathname == "/plz5":
        return [
            html.Div(
                [
                    html.Div(
                        [
                            html.Div(
                                [
                                    html.Label(
                                        "Confidential Energyefficiency Register for Data",
                                        style={"width": "880px", "font-size": "20px", "color": "red"}

                                    ),
                                    html.Label(
                                        "Select the KPI and the Postcode Region from the drop-down menu.",
                                        style={
                                            "margin-top": "10px",
                                            "color": "#31364c",
                                            "font-weight": "bold",
                                        },
                                    ),

                                    dcc.Dropdown(
                                        id="var_choice",
                                        value="Power Usage Effectiveness",
                                        options=[
                                            {"label": i, "value": i} for i in OPTIONS
                                        ],
                                        # optionHeight=19,
                                        style={
                                            "background-color": "#f5ae51",
                                            "color": "black",
                                            "font-size": "12px",
                                            "height": "30px",
                                            # "margin-top":"50px"
                                        },
                                    ),

                                    dcc.Dropdown(id="var_data", value="default", optionHeight=19,

                                                 options=[{"label": i, "value": i} for i in
                                                          ['1', '2', '3', '4', '5', '6', '7', '8', '9']],
                                                 style={"font-size": "12px",
                                                        "height": "30px"}
                                                 ),

                                    dcc.Dropdown(id="zweistellig", style={"font-size": "12px",
                                                                          "height": "30px"}),
                                    dcc.Graph(id="my-graph"),

                                ],
                                className="six columns",
                                style={
                                    "position": "absolute",
                                    "width": 400,
                                    "margin-top": 0,
                                    "margin-left": 180,
                                    "display": "inline-block",
                                    "height": "auto",
                                    "background-color": "#f5ae51",
                                },
                            ),
                            dbc.Button("Info", href="/",
                                       style={"margin-left": "580px", "width": "100px", "margin-top": "114px",
                                              "height": "35px", "font-size": "12px"}),

                            html.Div(
                                [
                                    html.Br(),
                                    dcc.RadioItems(
                                        id="yaxis_raditem",
                                        options=[
                                            {
                                                "label": html.Div(
                                                    ["Electricity Production Data Centres"],
                                                    style={
                                                        "display": "flex",
                                                        "align-items": "center",
                                                        "justify-content": "center",
                                                        "margin-top": "-20px",
                                                        "margin-left": "20px",
                                                        "padding-right": "20px",
                                                    },
                                                ),
                                                "value": "emission",
                                            },
                                            {
                                                "label": html.Div(
                                                    [
                                                        "Electricity Consumption Data Centres",
                                                    ],
                                                    style={
                                                        "display": "flex",
                                                        "align-items": "center",
                                                        "justify-content": "center",
                                                        "margin-left": "20px",
                                                        "margin-top": "-20px",
                                                    },
                                                ),
                                                "value": "sum",
                                            },
                                        ],
                                        inline=True,
                                        value="sum",
                                        style={
                                            "font-size": "13px",
                                            "width": "800px",
                                            "margin-top": "-100px",
                                            "margin-left": "750px",
                                            # "position": "relative",
                                            "font-family": "Helvetica",
                                            "color": "black",
                                        },
                                    ),
                                ],
                                className="six columns",
                            ),
                            html.Div(
                                dcc.Graph(
                                    id="the_graph",
                                    className="six columns",
                                    style={
                                        # "padding-top": "0px",
                                        "margin-left": "760px",
                                        "width": 450,
                                        "margin-top": "-50px",
                                        "height": 200,
                                        "background-color": "#f5ae51",
                                        "font-size": "14px"
                                    },
                                ),
                                className="six columns",
                            ),
                            html.Div(dcc.Graph(id="the_graph_2",
                                               style={"width": 400, "height": 200, "margin-left": "780px"})),
                            html.Div(
                                dcc.Graph(
                                    id="heat_graph",

                                    style={
                                        "margin-left": "580px",
                                        "margin-top": "80px",

                                    },
                                )
                            ),
                            html.Div(dcc.Graph(id="share", figure=fig_share),
                                     style={"width": 390, "height": 200, "margin-left": "160px",
                                            "margin-top": "-200px"}, ),
                            html.Div(dcc.Graph(id="class", figure=it_conn),
                                     style={"width": 300, "height": 150, "margin-top": "-200px",
                                            "margin-left": "-100px"}),
                        ],
                        className="row",
                        style={"font-color": "red", "background-color": "#f5ae51"},
                    )
                ]
            ),
        ]

    # If the user tries to reach a different page, return a 404 message


# return dbc.Jumbotron(
#    [
#       html.H1("404: Not found", className="text-danger"),
#      html.Hr(),
#     html.P(f"The pathname {pathname} was not recognised..."),
# ]
# )
if __name__ == "__main__":
    app.run_server(debug=True)
