import dash
from dash.dependencies import Input,Output,State
import dash_core_components as dcc 
import dash_html_components as html
import pandas as pd
import plotly.express as px


df=pd.read_csv('CSV Files for Dash/covid_19_india.csv')
df['Date']=pd.to_datetime(df['Date'])
df['Month']=df['Date'].dt.month
df['Year']=df['Date'].dt.year
print(df['Year'].dtype)

external_stylesheets=['https://codepen.io/chriddyp/pen/bWLwgp.css']
app=dash.Dash(__name__, external_stylesheets=external_stylesheets)

app.layout=html.Div([
    html.H1("Covid-19 Analysis Dashboard:India 2021", style={'textAlign':'center','color':'#316395',
    'font-family':'sans-serif'}),
    html.Hr(),
    html.H3("Choose State:", style={'font-family':'sans-serif','color':'#316395'}),
    html.Div(html.Div([
        dcc.Dropdown(id='state-type',clearable=False,
                     value='Kerala',
                     options=[{'label':x, 'value':x} for x in 
                              df['State/UnionTerritory'].unique()]),
    ], className="two columns"), className="row"),
    
    html.Div(id='output-div', children=[]),

])

@app.callback(Output('output-div', 'children'),
             [Input('state-type','value')])
    
def make_graphs(state):

    #histogram
    df_hist=df[df['State/UnionTerritory']==state]
    fig_1=px.bar(
        df_hist,
        x='Month',
        y='Cured',
    )
    fig_1.update_traces(marker_color='#4C78A8')
    

    fig_2=px.bar(
        df_hist,
        x='Month',
        y='Deaths',
    )
    fig_2.update_traces(marker_color='#4C78A8')

    fig_3=px.pie(
        data_frame=df_hist,
        names='Month',
        values='Confirmed',
        hover_data=['Year'],
        color_discrete_sequence=px.colors.sequential.haline,
    )
    fig_3.update_layout(title_text='Total Confirmed Cases per Month')

    fig_4=px.scatter(
        x='Cured',
        y='Deaths',
        data_frame=df_hist,
    )
    fig_4.update_layout(title_text='Total Patients Cured vs No. of Deaths per State')

    fig_5=px.line(
        x='ConfirmedIndianNational',
        y='ConfirmedForeignNational',
        data_frame=df_hist,
        color='Month',
        hover_data=['Year']
    )

    

    return [
        html.Div([
            html.Div([dcc.Graph(figure=fig_1)], style={'display':'inline-block'}),
            html.Div([dcc.Graph(figure=fig_2)], style={'display':'inline-block'}),
        ], className="row"),
        html.Div([
            html.Div([dcc.Graph(figure=fig_3)],style={'display':'inline-block'}),
            html.Div([dcc.Graph(figure=fig_4)],style={'display':'inline-block'}),
        ]),
        html.Div([
            html.Div([dcc.Graph(figure=fig_5)]),
        ])
    
    ]


        
    
if __name__ == '__main__':
    app.run_server(debug=True)