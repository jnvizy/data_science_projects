
import pandas as pd
import dash
import dash_html_components as html
import dash_core_components as dcc
import plotly.graph_objs as go
from textwrap import dedent
import numpy as np

############################### Chargement de la base issue ds queries mongo car le cluster mongosur aws n'existe plus ################
url_file="/home/user/TelecomParistech/TP_NOSQL/Projet_NoSQL/data_dash/df3_result.csv"
data_r3=pd.read_csv(url_file, names=['nneg','npos','FIPS','acteur','langue','mois','SHORT_NAME','tot_art'],skiprows=1)
acteur='SPY'


##les sujets (acteurs) qui ont eu le plus d’articles positifs/negatifs (mois, pays, langue de l’article).

############################## des couleurs pour l'histogramme #############################
colorVal = ["#F4EC15", "#DAF017", "#BBEC19", "#9DE81B", "#80E41D", "#66E01F",
                "#4CDC20", "#34D822", "#24D249", "#25D042", "#26CC58", "#28C86D",
                "#29C481", "#2AC093", "#2BBCA4", "#2BB5B8", "#2C99B4", "#2D7EB0",
                "#2D65AC", "#2E4EA4", "#2E38A4", "#3B2FA0", "#4E2F9C", "#603099"]
colorVal2 = ['#ff0000','#fc0a0a' , '#ef0404' , '#e50202' , '#d30a0a' ,'#d10606', '#c10303','#ff3030']






########## fonction pemettant de générer une table
def generate_table(dataframe, max_rows=10):
    return html.Table(
        # Header
        [html.Tr([html.Th(col) for col in dataframe.columns])] +

        # Body
        [html.Tr([
            html.Td(dataframe.iloc[i][col]) for col in dataframe.columns
        ]) for i in range(min(len(dataframe), max_rows))]
    )



########### des test intermédiaire############
#mois=2
#pays='IT'
#langue='sqi'
#res_df=data_r3[(data_r3.mois==mois) & (data_r3.FIPS==pays) & (data_r3.langue == langue)]
#res1=res_df.groupby(by=['acteur']).agg({'nneg':'sum'}).sort_values(by=['nneg'],ascending=False)
#res2=res_df.groupby(by=['acteur']).agg({'npos':'sum'}).sort_values(by=['npos'],ascending=False)[1:5]



########### initialiser l'appliation Dash 
app = dash.Dash()

########### import du fchier css
app.css.append_css({
    'external_url': 'https://codepen.io/chriddyp/pen/bWLwgP.css'
})




########### custom layout 
app.layout = html.Div([
    
  html.Div([
                html.Div([
                    html.H2("GDELT Flask APP ", style={'font-family': 'Dosis','color':'rgb(217, 217, 217)'})
                    
    ])
     ],style={'background-image': 'url(https://raw.githubusercontent.com/kasamoh/NoSQL/master/global-knowledge-graph-netvis.jpg)','background-color': '#111111' ,'background-size': ' contain, cover'}),
      html.P("Selectionner le mois"),
    dcc.Dropdown(
        id='mois-dropdown',
        options=[{'label': i, 'value': i} for i in data_r3.mois.unique()],
        placeholder="Selectionner le mois",
        multi=False,
        value=[1]
    ), html.P("Selectionner la langue"),
      dcc.Dropdown(
        id='langue-dropdown',
        options=[{'label': i, 'value': i} for i in data_r3.langue.unique()],
        placeholder="Selectionner la langue",
        multi=False,
        value=[1]
    ),
     html.P("Selectionner le pays"),
    dcc.Dropdown(
        id='pays-dropdown',
        placeholder="Selectionner le pays",
        options=[{'label': i, 'value': i} for i in data_r3.FIPS.unique()],
        multi=False,
        value=[1]
    ),
     html.Div( #small block upper most
   dcc.Graph(id='timeseries-graph')
    ,style={'width': '50%', 'display': 'inline-block' ,'backgroundColor':'#323130'  }),
  html.Div(  dcc.Graph(id='timeseries-graph2'),style={'width': '50%', 'display': 'inline-block','backgroundColor':'#323130'  }),


                html.Div(
                    [

                 generate_table(data_r3.sample(5)) ],
                    className='ten columns',
                    style={'margin-top': '10'}
                ),         html.P("Selectionner un acteur"),

                dcc.Dropdown(
        id='artist_slider',

        options=[{'label': i, 'value': i} for i in data_r3.acteur.unique()],
        multi=False,
        value=[acteur]
    ),
    

    dcc.Graph(id='graph-with-slider')

])


########### mise à jour du graphe à partir des donnees sur le mois , langue et pays 

@app.callback(dash.dependencies.Output('timeseries-graph', 'figure'),
    [dash.dependencies.Input('mois-dropdown', 'value'),
    dash.dependencies.Input('langue-dropdown', 'value'),
    dash.dependencies.Input('pays-dropdown', 'value')])
def update_graph(mois,langue,pays):
    print(mois)
    res_df=data_r3[(data_r3.mois==mois) & (data_r3.FIPS==pays) & (data_r3.langue == langue)]
    data_rank_2018=res_df.groupby(by=['acteur']).agg({'npos':'sum'}).sort_values(by=['npos'],ascending=False)[1:8]
    return {
        'data': [go.Bar(
             x=data_rank_2018.index,
            y=data_rank_2018.npos,
            marker=dict(
                        color=colorVal
                    )
        ) ],
        'layout': go.Layout(
            title="Top acteur par nombe d'articles positifs",
            font=dict(family='Courier New, monospace', size=15, color='rgb(217, 217, 217)'),

            xaxis=dict(
               title='Acteur',
                  titlefont=dict(
                 size=16,
                  color='rgb(217, 217, 217)'
                  ),
               tickfont=dict(
                   size=14,
            color='rgb(217, 217, 217)'
                   )
                ),
             yaxis=dict(
               title='Nmbre de mentions positifs',
                  titlefont=dict(
                 size=16,
                  color='rgb(217, 217, 217)'
                  ),
               tickfont=dict(
                   size=14,
            color='rgb(217, 217, 217)'
                   )
                ),
            margin={'l': 60, 'b': 50, 't': 80, 'r': 0},
            hovermode='closest',
            bargap=0.5,
             bargroupgap=0,
             barmode='group',
             #margin=Margin(l=10, r=0, t=0, b=30),
             showlegend=True,
             plot_bgcolor='#323130',
             paper_bgcolor='rgb(66, 134, 244, 0)',
            legend=dict(
              x=0,
               y=1.0,
             bgcolor='rgba(255, 255, 255, 0)',
            bordercolor='rgba(255, 255, 255, 0)'
             ),
             height=450,
             dragmode="select"
         )
    }




########### mise à jour du deuxième graphe à partir des donnees sur le mois , langue et pays 

@app.callback(dash.dependencies.Output('timeseries-graph2', 'figure'),
    [dash.dependencies.Input('mois-dropdown', 'value'),
    dash.dependencies.Input('langue-dropdown', 'value'),
    dash.dependencies.Input('pays-dropdown', 'value')])
def update_graph(mois,langue,pays):
    print(mois)
    res_df=data_r3[(data_r3.mois==mois) & (data_r3.FIPS==pays) & (data_r3.langue == langue)]
    data_rank_2018=res_df.groupby(by=['acteur']).agg({'nneg':'sum'}).sort_values(by=['nneg'],ascending=False)[1:5]
    print("ddddddddddddddddddd")
    return {
        'data': [go.Bar(
             x=data_rank_2018.index,
            y=data_rank_2018.nneg,
           # name=country,
               marker=dict(
                        color=colorVal2
                    )
            #mode="lines+marker"
           # name=country,
 
        ) ],
        'layout': go.Layout(
       title="Top acteur par nombre d'articles négatifs",
            font=dict(family='Courier New, monospace', size=15, color='rgb(217, 217, 217)'),

            xaxis=dict(
               title='Acteur',
                  titlefont=dict(
                 size=16,
                  color='rgb(217, 217, 217)'
                  ),
               tickfont=dict(
                   size=14,
            color='rgb(217, 217, 217)'
                   )
                ),
             yaxis=dict(
               title='Nmbre de mentions négatifs',
                  titlefont=dict(
                 size=16,
                  color='rgb(217, 217, 217)'
                  ),
               tickfont=dict(
                   size=14,
            color='rgb(217, 217, 217)'
                   )
                ),

           # yaxis={'title': 'Nombre de mentions positifs'},
            margin={'l': 60, 'b': 50, 't': 80, 'r': 0},
            hovermode='closest',
            bargap=0.5,
             bargroupgap=0,
             barmode='group',
             #margin=Margin(l=10, r=0, t=0, b=30),
             showlegend=True,
             plot_bgcolor='#323130',
             paper_bgcolor='rgb(66, 134, 244, 0)',
            legend=dict(
              x=0,
               y=1.0,
             bgcolor='rgba(255, 255, 255, 0)',
            bordercolor='rgba(255, 255, 255, 0)'
             ),
             height=450,
             dragmode="select"
         #   paper_bgcolor='#111111',
        #    plot_bgcolor= '#111111',
          #  font= { 'color': '#7FDBFF'}
             
        )
    }


############# préparation d'un layout pour une carte , à la fin on l'a pas garder  ....
mapbox_access_token = 'pk.eyJ1IjoiamFja2x1byIsImEiOiJjajNlcnh3MzEwMHZtMzNueGw3NWw5ZXF5In0.fk8k06T96Ml9CLGgKmk81w'  # noqa: E501

layout = dict(
    autosize=True,
    height=500,
    font=dict(color='#CCCCCC'),
    titlefont=dict(color='#CCCCCC', size='14'),
    margin=dict(
        l=35,
        r=35,
        b=35,
        t=45
    ),
    hovermode="closest",
    plot_bgcolor="#191A1A",
    paper_bgcolor="#020202",
    legend=dict(font=dict(size=10), orientation='h'),
    title='Satellite Overview',
    mapbox=dict(
        accesstoken=mapbox_access_token,
        style="dark",
        center=dict(
            lon=-78.05,
            lat=42.54
        ),
        zoom=7,
    )
)


########## mise à jour du grphe des tendenances+ et - pour chaque acteur
@app.callback(
    dash.dependencies.Output('graph-with-slider', 'figure'),
    [dash.dependencies.Input('artist_slider', 'value')])
def update_figure(selected_artist):
    #selected_artist=selected_artist[0]
    
    print("######")
    print(selected_artist)
    acteur=selected_artist

    tsn=data_r3[data_r3.acteur==acteur].groupby(by=['mois']).agg({'nneg':'sum'}).sort_values(by=['mois'],ascending=True).nneg
    tsp=data_r3[data_r3.acteur==acteur].groupby(by=['mois']).agg({'npos':'sum'}).sort_values(by=['mois'],ascending=True).npos

    traces = []

 
    print("######")
    listatt=['Mentions_Pos','Mentions_Neg']
    for i,ts in enumerate([tsn,tsp]):

        traces.append(go.Scatter(
            x=ts.index,
            y=ts,
            text= listatt[i],
            mode='lines+markers',
            opacity=0.7,
            marker={
                'size': 15,
                'line': {'width': 0.5, 'color': 'white'}
            },
            name=  listatt[i]
        ))

    return {
        'data': traces,
        'layout': go.Layout(
            title="Evolution des mentions ",
                        font=dict(family='Courier New, monospace', size=15, color='rgb(217, 217, 217)'),

            #hovermode='closest',

            xaxis=dict(
               title='Acteur',
                  titlefont=dict(
                 size=16,
                  color='rgb(255,255,255,255)',
                  )
                ),
            plot_bgcolor='#323130',
             paper_bgcolor='rgb(255,255,255,255)',
                 legend=dict(
              x=0,
               y=1.0,
             bgcolor='rgba(255, 255, 255, 0)',
            bordercolor='rgba(255, 255, 255, 0)'
             ),
                   height=450,
             dragmode="select"
        )
    }



if __name__ == "__main__":
    app.run_server(debug=True,port=8059)
