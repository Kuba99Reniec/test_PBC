import dash
from dash import dash_table
from dash.dependencies import Input, Output, State
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objects as go
import pandas as pd
import numpy as np
dane_cawi_capi = pd.read_csv("https://raw.githubusercontent.com/Kuba99Reniec/wykresy/master/dane_do_dasha_cpw.txt", sep="\t")
options = []
tytuly = pd.read_csv("https://raw.githubusercontent.com/Kuba99Reniec/test_PBC/main/tytuly.txt", sep="\t")
tytuly = tytuly[tytuly['zmienna']!='BUDDOM']
tytuly = tytuly[tytuly['zmienna']!='CZASWNE']
tytuly = tytuly[tytuly['zmienna']!='KROPTV']
tytuly = tytuly[tytuly['zmienna']!='OCZLEK']
tytuly = tytuly[tytuly['zmienna']!='VOGUE']
tytuly = tytuly.reset_index(drop = True)
cpw = pd.DataFrame()
dane_cawi = dane_cawi_capi[dane_cawi_capi['badanie'] == 'cawi']
for i in range(len(tytuly)):
    cpw.loc[tytuly.loc[i, 'tytul'], 'CPW: CAWI + CAPI'] = round(
                np.average(dane_cawi_capi[tytuly.loc[i, 'zmienna'] + '5'], weights=dane_cawi_capi['WAGAOSOB']), 2)
    cpw.loc[tytuly.loc[i, 'tytul'], 'CPW: CAWI'] = round(
                np.average(dane_cawi[tytuly.loc[i, 'zmienna'] + '5'], weights=dane_cawi['WAGAOSOB']), 2)
    cpw.loc[tytuly.loc[i, 'tytul'], 'CPW do raportu czytelnictwa'] = round(
                np.average(dane_cawi_capi[tytuly.loc[i, 'zmienna'] + '5_2C'], weights=dane_cawi_capi['WAGAOSOB']),
                2)
    cpw.loc[tytuly.loc[i, 'tytul'], 'CPW do mediaplanu'] = round(
                np.average(dane_cawi_capi[tytuly.loc[i, 'zmienna'] + '5_24a'], weights=dane_cawi_capi['WAGAOSOB']),
                2)
cpw = cpw.reset_index(drop=False)
cpw = cpw.rename(columns={'index': 'pismo'})
cpw[''] = cpw['pismo']
cpw = cpw.set_index('')
options_2 = sorted(list(set(tytuly['grupa tematyczna'].to_list())))
for col in dane_cawi_capi.columns[:87]:
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
            "Analiza: CAWI vs CAWI + CAPI (IX 2021 - VIII 2022)",
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
        style={'width': '49%', 'align': 'right', 'display': 'inline-block', 'height': '82%'}),
    html.Label("Wybierz grupę tematyczną:"),
    dcc.Dropdown(
            id = 'table_dropdown',
            options=options_2,
            value='kobiece: exclusive'
        ),
    dash_table.DataTable(
        id='dynamic_table',
        columns=[{'name': col, 'id': col} for col in cpw.columns],
        data=cpw.to_dict('records'),
        style_data={
        'color': 'black',
        'backgroundColor': 'white'},
        style_data_conditional=[
        {
            'if': {'row_index': 'odd'},
            'backgroundColor': 'rgb(220, 220, 220)',
        }],
        style_cell_conditional=[
            {'if': {'column_id': ''},
             'width': '16%', 'textAlign': 'left'},
            {'if': {'column_id': 'CPW: CAWI + CAPI'},
             'width': '21%', 'textAlign': 'center'},
            {'if': {'column_id': 'CPW: CAWI'},
             'width': '21%', 'textAlign': 'center'},
            {'if': {'column_id': 'CPW do raportu czytelnictwa'},
             'width': '21%', 'textAlign': 'center'},
            {'if': {'column_id': 'CPW do mediaplanu'},
             'width': '21%', 'textAlign': 'center'}
        ])
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
        marker={"colors": ['#a6cee3', '#1f78b4', '#b2df8a', '#33a02c', '#fb9a99', '#e31a1c', '#fdbf6f', '#ff7f00', '#cab2d6', '#6a3d9a', '#ffff99', '#b15928']},
        title={"position": "top center", "text": "CAWI"}
    )
    fig = go.Figure(trace_1)
    fig.update_traces(title_font_size=20)
    fig.update_traces(title_position='top center')
    fig.update_layout(margin=dict(t=0, b=30, l=0, r=0))
    fig.update_traces(aspectratio=0.5)
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
        title={"position": "top center", "text": "CAWI+CAPI"},
        marker={"colors": ['#a6cee3', '#1f78b4', '#b2df8a', '#33a02c', '#fb9a99', '#e31a1c', '#fdbf6f', '#ff7f00', '#cab2d6', '#6a3d9a', '#ffff99', '#b15928']},
        showlegend=False)
    fig = go.Figure(trace_2)
    fig.update_traces(title_font_size=20)
    fig.update_traces(title_position='top center')
    fig.update_layout(margin=dict(t=0, b=30, l=0, r=0))
    fig.update_traces(aspectratio=0.5)
    return fig
@app.callback(Output('dynamic_table','data'),
             [Input('table_dropdown','value')],)
def get_corresponding_rows(value):
    return cpw.loc[sorted(list(set(tytuly['tytul'][tytuly['grupa tematyczna']==value].to_list()))),].to_dict('records')
if __name__ == '__main__':
    app.run_server(debug=True)
