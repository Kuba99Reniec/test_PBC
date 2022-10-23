import dash
from dash.dependencies import Input, Output, State
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objects as go
import pandas as pd
dane_cawi_capi = pd.read_csv("https://raw.githubusercontent.com/Kuba99Reniec/wykresy/master/dane_do_dasha.txt", sep="\t")
options = []
for col in dane_cawi_capi.columns[:-1]:
    options.append({'label':'{}'.format(col, col), 'value':col})
value = 'Wielkość gospodarstwa domowego (6 kategorii)'
zmienne = pd.read_csv("https://raw.githubusercontent.com/Kuba99Reniec/wykresy/master/5_opis_zmiennych_20220819_podwojny_konwerter_opinie.txt", sep="\t")
wartosci = pd.read_csv("https://raw.githubusercontent.com/Kuba99Reniec/wykresy/master/6.txt", sep="\t", decimal =",")
wartosci = wartosci.merge(zmienne, on = "Nazwa zmiennej")
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash('CAWI vs CAWI + CAPI', external_stylesheets=external_stylesheets)
server = app.server
app.layout = html.Div([
    html.Div(
        className="header",
        style={"backgroundColor": "#3c6382"},
        children=[html.H3(
            "Porównanie rozkładów zmiennych: CAWI vs CAWI + CAPI (IX 2021 - VIII 2022)",
            style={
                "color": "white",
                "padding": "20px 0 20px 0",
                "textAlign": "center"}
        )],
    ),
    html.Label("Wybierz zmienną:"),
    dcc.Dropdown(
            id = 'my_dropdown',
            options= options,
            value='RS: Płeć'
        ),
    dcc.Graph(
        id='graph',
        style={'width': '49%', 'display': 'inline-block', 'height': '82%'}),
    dcc.Graph(
        id='graph_2',
        style={'width': '49%', 'align': 'right', 'display': 'inline-block', 'height': '82%'})
])
@app.callback(
    Output('graph', 'figure'),
    Input('my_dropdown', 'value'),
    State('graph', 'figure')
)
def update_figure(value, fig):
    zmienna = value
    df_pom = pd.DataFrame(dane_cawi_capi[dane_cawi_capi['badanie'] == 'cawi'][zmienna].value_counts())
    names_cawi_pom = df_pom.index.to_list()
    values_cawi = df_pom[zmienna].to_list()
    values_cawi_capi = []
    names_cawi = []
    for i in names_cawi_pom:
        values_cawi_capi.append(len(dane_cawi_capi[dane_cawi_capi[zmienna] == i]))
        if zmienna in wartosci['Etykieta zmiennej'].to_list():
            names_cawi.append(
                wartosci[(wartosci['Etykieta zmiennej'] == zmienna) & (wartosci['wartość'] == i)]['Etykieta'].to_list()[
                    0])
        else:
            names_cawi = names_cawi_pom
    trace_1 = go.Funnelarea(
        name="CAWI",
        text=names_cawi,
        values=values_cawi,
        showlegend=False,
        marker={"colors": ["#1f77b4", "#ff7f0e", "#2ca02c", "#d62728", "#9467bd", "#8c564b", "#e377c2", "#7f7f7f", "#bcbd22", "#17becf"]},
        title={"position": "top center", "text": "CAWI"}
    )
    fig = go.Figure(trace_1)
    fig.update_traces(title_font_size=20)
    fig.update_traces(title_position='top center')
    fig.update_layout(margin=dict(t=0, b=0, l=0, r=0))
    fig.update_traces(aspectratio=0.6)
    return fig
@app.callback(
    Output('graph_2', 'figure'),
    Input('my_dropdown', 'value'),
    State('graph_2', 'figure')
)
def update_figure(value, fig):
    zmienna = value
    df_pom = pd.DataFrame(dane_cawi_capi[dane_cawi_capi['badanie'] == 'cawi'][zmienna].value_counts())
    names_cawi_pom = df_pom.index.to_list()
    values_cawi = df_pom[zmienna].to_list()
    values_cawi_capi = []
    names_cawi = []
    for i in names_cawi_pom:
        values_cawi_capi.append(len(dane_cawi_capi[dane_cawi_capi[zmienna] == i]))
        if zmienna in wartosci['Etykieta zmiennej'].to_list():
            names_cawi.append(
                wartosci[(wartosci['Etykieta zmiennej'] == zmienna) & (wartosci['wartość'] == i)]['Etykieta'].to_list()[
                    0])
        else:
            names_cawi = names_cawi_pom
    trace_2 = go.Funnelarea(
        name="CAWI + CAPI",
        text=names_cawi,
        values=values_cawi_capi,
        textinfo="percent",
        title={"position": "top center", "text": "CAWI+CAPI"},
        marker={"colors": ["#1f77b4", "#ff7f0e", "#2ca02c", "#d62728", "#9467bd", "#8c564b", "#e377c2", "#7f7f7f", "#bcbd22", "#17becf"]},
        showlegend=False)
    fig = go.Figure(trace_2)
    fig.update_traces(title_font_size=20)
    fig.update_traces(title_position='top center')
    fig.update_layout(margin=dict(t=0, b=0, l=0, r=0))
    fig.update_traces(aspectratio=0.6)
    return fig
if __name__ == '__main__':
    app.run_server(debug=True)
