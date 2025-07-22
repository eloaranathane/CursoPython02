import pandas as pd

# Carregar os dados da planilha
caminho = 'C:/dados/base_inicial.xlsx'

df1 = pd.read_excel(caminho, sheet_name='Relatório de Vendas')
df2 = pd.read_excel(caminho, sheet_name='Relatório de Vendas1')

# Exibir as primeiras linhas para conferir como estão os dados
print('------ Primeiro relatorio ------')
print(df1.head())
print('------ Segundo relatorio ------')
print(df1.head())

# Verificar se há duplicatas nas duas tabelas
print('Duplicatas no relatorio 1')
print(df1.duplicated().sum())
print('Duplicatas no relatorio 1')
print(df2.duplicated().sum())

# Agora vamos consolidar as duas tabelas
print('Dados consolidados')
df_consolidado = pd.concat([df1, df2], ignore_index=True)
print(df_consolidado.head())

# Exibir o numero de clientes por cidade
clientes_por_cidade = df_consolidado.groupby('Cidade')['Cliente'].nunique().sort_values(ascending=False)
print('Clientes por cidade')
print(clientes_por_cidade)

# Numero de vendas por plano
vendas_por_plano = df_consolidado['Plano Vendido'].value_counts()
print('Numero de Vendas por Plano')
print(vendas_por_plano)

# Exibir as 3 primeiras cidades com mais clientes
top_3_cidades = clientes_por_cidade.head(3)
print('Top 3 cidades')
print(top_3_cidades)

# Exibir o total de clientes
total_clientes = df_consolidado['Cliente'].nunique()      #nunique trás um cliente com po mesmo nome como único, se tiver 4 Caios ele trás os 4 separados
print(f'\n Numero total de clientes: {total_clientes}')

# Adicionar uma coluna de Status (exemplo fictício de analise)
# Vamos classificar os planos como premium se for enterprise, caso contrário será padrão
df_consolidado['Status'] = df_consolidado['Plano Vendido'].apply(lambda x: 'Premium' if x == 'Enterprise' else 'Padrão')

    # Exibir a distribuição dos status
status_dist = df_consolidado['Status'].value_counts()
print('\n Distribuição dos status:')
print(status_dist)

# Salvar a tabela em um arquivo
# Primeiro em Excel
df_consolidado.to_excel('dados_consolidados_planilha.xlsx', index=False)
# Depois em CSV
df_consolidado.to_csv('dados_consolidados_texto.csv', index=False) #index=False quer dizer que não precisa do indice numérico que ele determina

# Exibir mensagem final
print('\n Arquivos Gerados com sucesso!')