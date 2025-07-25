from flask import Flask, request, render_template_string
import pandas as pd
import sqlite3
import plotly.express as px
import plotly.io as pio
import random

# Configura o plotly para abrir os arquivos no navegador por padrão
pio.renderers.deafult = "browser"

# Carregar o drinks.csv
df = pd.read_csv("drinks.csv")

# Cria o banco de dados em sql e popular com os dados do arquivo csv
conn = sqlite3.connect("consumo_alcool.db")
df.to_sql("drinks", conn, if_exists="replace", index=False)
conn.commit()
conn.close()




