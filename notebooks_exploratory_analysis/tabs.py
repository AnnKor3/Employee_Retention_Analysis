app = Dash(__name__, external_stylesheets=external_stylesheets)

def generate_tabs(i):
    return dcc.Tab(label='tab '+str(i), value=str(i))

df = px.data.gapminder()

app.layout = html.Div([
    html.H1('Dash Tabs component demo'),
    dcc.RadioItems(
        options=df.country.unique(),
        value='Canada', 
        inline=True,
        id='ratios'
    ),
    dcc.Tabs(id="tabs-example-graph", value='tab-1-example-graph', children=[
        #dcc.Tab(label='Tab One', value='tab-1-example-graph'),
        #[generate_team_button(i) for i in df_teams['teams']]
        generate_tabs(i) for i in range(5)
        #dcc.Tab(label='Tab Two', value='tab-2-example-graph'),
    ]),
    html.Div(id='tabs-content-example-graph')
])

@callback(Output('tabs-content-example-graph', 'children'),
              Input('tabs-example-graph', 'value'),
          Input('ratios', 'value'),
         allow_duplicate=True)
def render_content(tab,r):
    if tab == '0':
        #fig = px.line(df, x="year", y="lifeExp"),
        a = df[df['country']==r]
        return html.Div([
            html.H3('Tab content 1'),
            
            dcc.Graph(
                
                figure=px.line(a, x="year", y="lifeExp")
                
            )
        ])
    elif tab == '1':
        return html.Div([
            html.H3('Tab content 2'),
            dcc.Graph(
                id='graph-2-tabs-dcc',
                figure={
                    'data': [{
                        'x': [1, 2, 3],
                        'y': [5, 10, 6],
                        'type': 'bar'
                    }]
                }
            )
        ])

if __name__ == '__main__':
    app.run(debug=True, port='8003')