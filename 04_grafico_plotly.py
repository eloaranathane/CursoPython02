# 04_grafico_plotly.py

from flask import Flask, render_template_string
import plotly.express as px
import pandas as pd

# Iniciar o Flask
app = Flask(__name__)

# Gerar o Dataframe
df_consolidado = pd.DataFrame({
    'Status':[
        'Ativo',
        'Inativo',
        'Cancelado',
        'Ativo',
        'Inativo',
        'Ativo',
        'Inativo',
        'Cancelado',
        'Ativo',
        'Inativo'
    ]
})

# Rota inicial do gráfico de pizza usando o plotly
@app.route('/')
def grafico_pizza():
    # Contar quantas ocorrências de cada status
    status_dist = df_consolidado['Status'].value_counts().reset_index()
    status_dist.columns = ['Status','Quantidade']

    # Criar o gráfico plotly
    fig = px.pie(
        status_dist,
        values = 'Quantidade',
        names = 'Status',
        title = 'Distribuição de Status'
    )
    # Converter o gráfico para HTML (isso já gera um html pronto com <DIV>, <STYLE., e {} )

    grafico_html = fig.to_html(full_html=False)

    html = '''
            <html>
                <head>
                    <meta charset='UTF-8'>
                    <title>04 Grafico </title>
                </head>
                <body>]
                    <h2>Grafico com Plotly</h2>
                    {{grafico_html | safe }}
                </body>
            </html>    
            '''
    return render_template_string(html, grafico_html=grafico_html)

if __name__ == '__main__' :
    app.run(debug=True)     