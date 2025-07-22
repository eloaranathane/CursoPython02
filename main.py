import config 
import pandas as pd
import sqlite3
import os 
from flask import Flask, request, jsonify, render_template_string

app = Flask(__name__)

DB_PATH = config.DB_PATH

# Função para inicializar o banco de dados SQL
def init_db():
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS inadimplencia(
                mes TEXT PRIMARY KEY,
                inadimplencia REAL               
                )
        ''')
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS selic(
                mes TEXT PRIMARY KEY,
                selic_diaria REAL               
                )
        ''')
        conn.commit()

# EM BREVE =)
vazio = 0

@app.route('/')
def index():
    return render_template_string('''
        <h1>Upload de Dados Econômicos</h1>
        <form action='/upload' method='POST' enctype='multipart/form-data'> 
            <label for='campo_inadimplencia'>Arquivo de Inadimplencia</label>
            <input name='campo_inadimplencia' type='file' required><br><br>

            <label for='campo_selic'>Arquivo de Taxa Selic</label>
            <input name='campo_selic' type='file' required><br><br>
            <input type='submit' value='Fazer Upload'>                                  
        </form>
        <br><br><hr>
        <a href='/consultar'> Consultar Dados <br>                         
        <a href='/graficos'> Visualizar Graficos <br>     
        <a href='/editar_inadimplencia'> Editar dados de Inadimplencia <br>     
        <a href='/correlacao'> Analisar a Correlação <br>                                    
    ''')

@app.route('/upload', methods=['POST','GET'])
def upload():
    inad_file = request.files.get('campo_inadimplencia')
    selic_file = request.files.get('campo_selic')
    # Verificar se os arquivos de fato foram enviados
    if not inad_file or not selic_file:
        return jsonify({'Erro':'Ambos os arquivos devem ser enviados'})
    
    inad_df = pd.read_csv(
        inad_file,
        sep = ';',
        names = ['data','inadimplencia'],
        header = 0
    )

    selic_df = pd.read_csv(
        selic_file,
        sep = ';',
        names = ['data','selic'],
        header = 0
    )       
# Formata o campo de data como datahora padrão
    inad_df['data'] = pd.to_datetime(inad_df['data'], format="%d/%m/%Y")    
    selic_df['data'] = pd.to_datetime(selic_df['data'], format="%d/%m/%Y")

# Gera uma coluna nova mes e preenche de acordo com a data
    inad_df['mes'] = inad_df['data'].dt.to_period('M').astype(str)
    selic_df['mes'] = selic_df['data'].dt.to_period('M').astype(str)

# Limpa as duplicatas e agupa conjuntos                            
    inad_mensal = inad_df[['mes','inadimplencia']].drop_duplicates()
    selic_mensal = selic_df.groupby('mes')['selic'].mean().reset_index()

# Agora com tudo limpo e ordenado vamos armazenar no banco de dados
    with sqlite3.connect(DB_PATH) as conn:
        inad_mensal.to_sql('inadimplencia', conn, if_exists='replace', index=False)
        selic_mensal.to_sql('selic', conn, if_exists='replace', index=False)
    return jsonify({'Mensagem':'Dados inseridos com sucesso!'})

@app.route('/consultar', methods=['POST','GET'])
def consultar():
    # Resultado se a página for carregada recebendo POST
    if request.method == 'POST':
        tabela = request.form.get('campo_tabela')
        if tabela not in ['inadimplencia','selic']:
            return jsonify({'Erro;','Tabela é invalida'})
        with sqlite3.connect(DB_PATH) as conn:
            df = pd.read_sql_query(f'SELECT * FROM {tabela}', conn)
        return df.to_html(index=False)
    # Resultado sem receber um POST, ou seja, primeiro carregamento da pagina de consulta
    return render_template_string('''
        <h1> Consultar Tabelas </h1>
        <form action='/consultar' method='POST'>
            <label for='campo tabela'> Escolha a tabela: </label>
            <select name='campo_tabela'>
                <option value='inadimplencia'>Inadimplencia</option>
                <option value-'selic'>Selic</option>
            </select>
            <input type='submit' value='Consultar'>
        </form>
        <br>
        <a href='/'>Voltar</a>
    ''')

if __name__ == '__main__':
    # init_db()
    app.run(debug=True)
