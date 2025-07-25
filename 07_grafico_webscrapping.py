# gráfico plotly.py para a pesquisa de webscrapping

import dash
from dash import html
import plotly.express as px
import pandas as pd

# Carregar o CSV
df = pd.read_csv('filmes_adorocinema.csv')

# Ordenar filmes pelas notas
df.sort_values(by = "Nota", ascending = True)

# Criar o grafico com plotly
fig = px.bar(
    df,
    x = 'Nota',
    y = 'Titulo',
    orientation='h',
    labels={'nota':'Nota do Filme','titulo':'Titulo do filme'},
    title='Nota dos filmes'
)
# Inicializando a aplicação Dash
app = dash.Dash()

# Definindo o layout da aplicação
app.layout = html.Div([
    html.H1("Grafico de notas dos filmes", style={'text-align':'center'}),
    html.Div([
        html.Iframe(
            srcDoc=fig.to_html(),
            width="100%",
            height="600px",
            style={'border':'20px'}
        )
    ], style={'padding':'15px'})
])

# Rodar a aplicação
if __name__=='__main__':
    app.run(debug=True)