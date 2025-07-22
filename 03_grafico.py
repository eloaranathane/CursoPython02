import dash 
from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.graph_objs as go            # "go" é um nome que determinamos para os graph_objs importados no plotly

# Dicionário com as Informações da Caixa Dropdown
dados_conceitos = {
    'java':{'Variaveis':8, 'Condicionais':10, 'Loops':4, 'poo':3, 'funções':4},

    'python':{'Variaveis':9, 'Condicionais':7, 'Loops':8, 'poo':7, 'funções':2},

    'sql':{'Variaveis':10, 'Condicionais':9, 'Loops':1, 'poo':6, 'funções':8},

    'golang':{'Variaveis':7, 'Condicionais':5, 'Loops':3, 'poo':5, 'funções':3},

    'javascript':{'Variaveis':6, 'Condicionais':2, 'Loops':2, 'poo':4, 'funções':6}
}

cores_map = dict(
    java='red',
    python='green',
    sql='yellow',
    golang='blue',
    javascript='pink'
)
# "app" seria um gráfico de linguagens (Informações do Gráfico) (App - aplicação)
app = dash.Dash(__name__)            # Dois underline pois é uma convenção para utilização da biblioteca
                                     # Para conseguir processar Dash.dependencies essa estrutura tem que estar desenhada no programa
app.layout = html.Div([              # Div é uma caixa que depois eu determino o que ela vai ser, o que vai compor nela
    html.H4('Cursos de TI', style={'textAlign':'center'}),
    html.Div(
        dcc.Dropdown(
            id = 'dropdown_linguagens',
            options = [
                {'label':'Java','value':'java'},
                {'label':'Python','value':'python'},
                {'label':'SQL','value':'sql'},
                {'label':'GoLang','value':'goland'},
                {'label':'Javascript','value':'javascript'}
            ],
            value=['python'],   # Vem como padrão logo quando abre o site aparece no Dropdown
            multi=True,         # Permite que a gente selecione mais de uma opção para plotar no grafico
            style={'width':'50%','margin':'0 auto'}
        )
    ),
    dcc.Graph(id='grafico_linguagem')
], style={'width':'80%','margin':'0 auto'}
)

# Uma função que vai ser chamada através do evento (Interação do Gráfico)
@app.callback(
    Output('grafico_linguagem','figure'),
    [Input('dropdown_linguagens','value')]
)

def scarter_linguagens(linguagens_selecionadas):
    scarter_trace=[]

    for linguagem in linguagens_selecionadas:
        dados_linguagem = dados_conceitos[linguagem] 
        for conceito, conhecimento in dados_linguagem.items():
            scarter_trace.append(
                go.Scatter(
                    x=[conceito],
                    y=[conhecimento],
                    mode = 'markers',
                    name=linguagem.title(),
                    marker={'size':15,'color':cores_map[linguagem]},
                    showlegend=False
                )
            )
    scarter_layout = go.Layout(
        title="Meus conhecimentos em Linguagens",
        xaxis=dict(title = 'Conceitos', showgrid=False),
        yaxis=dict(title = 'Niveis de Conhecimento', showgrid=False),
    )
    return {'data':scarter_trace, 'layout':scarter_layout}

if __name__ == '__main__':
    app.run(debug=True)           # Para executar a programação
# Para conseguir processar Dash.dependencies essa estrutura tem que estar desenhada no programa