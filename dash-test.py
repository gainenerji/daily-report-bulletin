import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from dash import Dash, html, dash_table,dcc
import dash_bootstrap_components as dbc
from functions import *
from dash import Input, Output, html

today = "2023-09-15"
yesterday = "2023-09-14"
tomorrow = "2023-09-16"

""" today = datetime.today().strftime('%Y-%m-%d')
yesterday = (datetime.today() - timedelta(days=1)).strftime('%Y-%m-%d')
tomorrow = (datetime.today() + timedelta(days=1)).strftime('%Y-%m-%d') """

price_yesterday = ptf_smf(yesterday, yesterday)
price_today = ptf_smf(today, today)
price_tomorrow = ptf_smf(tomorrow, tomorrow)

price_yesterday["Tarih"] = pd.to_datetime(price_yesterday["Tarih"])

max_fiyat = price_yesterday.apply(fiyat_max, axis=1)
min_fiyat = price_yesterday.apply(fiyat_min, axis=1)
price_yesterday["+EDF"] = round((min_fiyat * 0.97),2)
price_yesterday["-EDF"] = round((max_fiyat * 1.03),2)
price_yesterday= saat_sutunu_ekle(price_yesterday)

price_today_usd = change_currency("USD",price_today)
price_today_eur = change_currency("EUR",price_today)

price_tomorrow_usd = change_currency("USD",price_tomorrow)
price_tomorrow_eur = change_currency("EUR",price_tomorrow)

price_yesterday_usd = change_currency("USD",price_yesterday)
price_yesterday_eur = change_currency("EUR",price_yesterday)



df = pd.DataFrame(columns=['Saat', 'PTF (D+1)',"PTF (D)","PTF (D-1)","SMF (D-1)","+EDF (D-1)","-EDF (D-1)"])
df["Saat"] = price_yesterday["Saat"]
df["PTF (D+1)"] = price_tomorrow["PTF"]
df["PTF (D)"] = price_today["PTF"]
df["PTF (D-1)"] = price_yesterday["PTF"]
df["SMF (D-1)"] = price_yesterday["SMF"]
df["+EDF (D-1)"] = price_yesterday["+EDF"]
df["-EDF (D-1)"] = price_yesterday["-EDF"]
df_avg = df.mean().to_frame().T
df_avg = df_avg.rename(columns={"Saat": 'AOF'})
df_avg["AOF"] = ""
df_avg = df_avg.round(2)

df_usd = pd.DataFrame(columns=['Saat', 'PTF (D+1)',"PTF (D)","PTF (D-1)","SMF (D-1)","+EDF (D-1)","-EDF (D-1)"])
df_usd["Saat"] = price_yesterday_usd["Saat"]
df_usd["PTF (D+1)"] = price_tomorrow_usd["PTF"]
df_usd["PTF (D)"] = price_today_usd["PTF"]
df_usd["PTF (D-1)"] = price_yesterday_usd["PTF"]
df_usd["SMF (D-1)"] = price_yesterday_usd["SMF"]
df_usd["+EDF (D-1)"] = price_yesterday_usd["+EDF"]
df_usd["-EDF (D-1)"] = price_yesterday_usd["-EDF"]
df_avg_usd = df_usd.mean().to_frame().T
df_avg_usd = df_avg_usd.rename(columns={"Saat": 'AOF'})
df_avg_usd["AOF"] = ""
df_avg_usd = df_avg_usd.round(2)

df_eur = pd.DataFrame(columns=['Saat', 'PTF (D+1)',"PTF (D)","PTF (D-1)","SMF (D-1)","+EDF (D-1)","-EDF (D-1)"])
df_eur["Saat"] = price_yesterday_eur["Saat"]
df_eur["PTF (D+1)"] = price_tomorrow_eur["PTF"]
df_eur["PTF (D)"] = price_today_eur["PTF"]
df_eur["PTF (D-1)"] = price_yesterday_eur["PTF"]
df_eur["SMF (D-1)"] = price_yesterday_eur["SMF"]
df_eur["+EDF (D-1)"] = price_yesterday_eur["+EDF"]
df_eur["-EDF (D-1)"] = price_yesterday_eur["-EDF"]
df_avg_eur = df_eur.mean().to_frame().T
df_avg_eur = df_avg_eur.rename(columns={"Saat": 'AOF'})
df_avg_eur["AOF"] = ""
df_avg_eur = df_avg_eur.round(2)


table = dbc.Table.from_dataframe(df, 
                             striped=True, 
                             bordered=True, 
                             hover=True,
                             responsive=True,
                             size = 'sm')

table_avg = dbc.Table.from_dataframe(df_avg,
                                    striped=True, 
                                    bordered=True, 
                                    hover=True,
                                    responsive=True,
                                    size = 'sm')

table_usd = dbc.Table.from_dataframe(df_usd,
                                    striped=True, 
                                    bordered=True, 
                                    hover=True,
                                    responsive=True,
                                    size = 'sm')

table_avg_usd = dbc.Table.from_dataframe(df_avg_usd,
                                    striped=True, 
                                    bordered=True, 
                                    hover=True,
                                    responsive=True,
                                    size = 'sm')

table_eur = dbc.Table.from_dataframe(df_eur,
                                    striped=True, 
                                    bordered=True, 
                                    hover=True,
                                    responsive=True,
                                    size = 'sm')

table_avg_eur = dbc.Table.from_dataframe(df_avg_eur,
                                    striped=True, 
                                    bordered=True, 
                                    hover=True,
                                    responsive=True,
                                    size = 'sm',
                                    style = {"color":"red"})



#######################################################
ptf_fig = px.line(df, x="Saat", y=["PTF (D+1)","PTF (D)","PTF (D-1)"], 
                  title='PTF Karşılaştırması',
                  labels={"value": "PTF", "variable":"Veri"},
                  template="plotly_white")
ptf_smf_fig = px.line(df, x="Saat", y=["PTF (D-1)","SMF (D-1)"], 
                      title='PTF SMF Karşılaştırması (D-1)',
                      labels={"value": "PTF", "variable":"Veri"},
                      template="plotly_white",
                      )
#######################################################
nav_contents = [
    dbc.NavItem(dbc.NavLink("Fiyat Analizi", href="#", active=True)),
    dbc.NavItem(dbc.NavLink("GİP Analizi", href="#",style={"color":"#285A84"})),
    dbc.NavItem(dbc.NavLink("Yük Analizi", href="#",style={"color":"#285A84"})),
    dbc.NavItem(dbc.NavLink("Diğer Analizler", href="#",style={"color":"#285A84"})),
]

app = Dash(external_stylesheets=[dbc.themes.FLATLY])
server = app.server

app.layout = dbc.Container(
    html.Div([
        dbc.Row(
            [   dbc.Col(html.Div(html.A(href="url(https://www.gainenerji.com)")),
                        width=2,
                        style = {"background-image" : "url(https://www.gainenerji.com/wp-content/uploads/2022/10/gain-20-web.png)",
                                 "background-repeat": "no-repeat",
                                 "background-position": "start",
                                 "background-size": "contain",
                                 }),
                dbc.Col(html.Div(dbc.Nav(nav_contents, pills=True, fill=True),
                                 style={"margin-bottom":"10px","text-color":"black"}),
                                 width=6,
                                 ),
            ],
            justify="between",
            style={"margin-bottom":"10px", "margin-top":"30px"}
        ),
        dbc.Row(
            [
                html.Hr(),
                dbc.Col(html.Div(
                [
                    dbc.Tabs(
                        [
                            dbc.Tab(label="TL", tab_id="tl",label_style={"color":"#285A84"},active_label_style={"color":"#E13915"}),
                            dbc.Tab(label="USD", tab_id="usd",label_style={"color":"#285A84"},active_label_style={"color":"#E13915"}),
                            dbc.Tab(label="EUR", tab_id="eur",label_style={"color":"#285A84"},active_label_style={"color":"#E13915"}),
                        ],
                        id="tabs",
                        active_tab="tl",
                    ),
                    html.Div(id="content"),
                ]
            )),

            dbc.Col([dcc.Graph(figure = ptf_fig),dcc.Graph(figure = ptf_smf_fig)],width=6),
            html.Hr(),
            ]
        )
    ])

)

@app.callback(Output("content", "children"), [Input("tabs", "active_tab")])
def switch_tab(at):
    if at == "tl":
        return table, table_avg
    elif at == "usd":
        return table_usd, table_avg_usd
    elif at == "eur":
        return table_eur, table_avg_eur

if __name__ == '__main__':
    app.run(debug=True)