# Importa o algoritmo de cluestering do KMeans da biblioteca scikit-learn
from sklearn.cluster import KMeans
# Importa o escalador StandrtScaler para padronizar os dados
from sklearn.preprocessing import StandardScaler

# Definir os dados de exemplo 
# Será uma lista de listas
x = [[1,2],[1,4],[1,0],[10,2],[10,4],[10,0]]

# Vamos instanciar o standard para padronizar os dados
scaler = StandardScaler()

# Aplicar o escalador nos dados para que tenham média 0 e desvio-padrão 1
X_scaled = scaler.fit_transform(x)

# Cria a instancia do algoritmo KMeans com 2 clusters
kmeans = KMeans(n_clusters=2, random_state=42)

# Aplicar o algoritmo do kmeans aos dados padronizados
kmeans.fit(X_scaled)

# Exibir os rotulos (clusters) atribuídos a cada ponto
print(kmeans.labels_)