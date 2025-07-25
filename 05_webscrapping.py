import requests
from bs4 import BeautifulSoup
import pandas as pd
import time

# Headers para simular um navegador real
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0 Safari/537.36'
}
base_url = "https://www.adorocinema.com/filmes/melhores/"
filmes = []

# Limita para as 5 primeiras paginas
for pagina in range(1,6):
    url = f"{base_url}?page={pagina}"
    print(f"Coletando dados da pagina {pagina}:{url}")

    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")
    
# Cada filme está em uma div com classe nomeada
    cards = soup.find_all("div", class_='card entity-card entity-card-list cf')
    
    for card in cards:
        titulo_tag = card.find("a", class_="meta-title-link")
        titulo = titulo_tag.text.strip() if titulo_tag else "N/A"
        link = "https://www.adorocinema.com" + titulo_tag['href'] if titulo_tag else None
        
        nota_tag = card.find("span", class_="stareval-note")
        nota = nota_tag.text.strip().replace(",", ".") if nota_tag else "N/A"

        # Visitar a pagina do filme e pegar as informações (director e elenco)
        if link:
            filme_response = requests.get(link, headers=headers)
            filme_soup = BeautifulSoup(filme_response.text,"html.parser")

        # Director
            director_container = filme_soup.find("div", class_="meta_body-direction")
            if director_container:
                director_tag = director_container.find("a")
                director = director_tag.text.strip() if director_tag else "N/A"
            else:
                director = "N/A"

        # Elenco
            elenco_tags = filme_soup.find_all("div", class_="meta-body-actor")
            elenco = []
            for tag in elenco_tags:
                atores = tag.find_all("a")
                elenco.extend([a.text.strip() for a in atores])
            elenco_str = ", ".join(elenco[:4]) # limita aos primeiros 5 atores
        else:
            director = "N/A"
            elenco_str = "N/A"

        filmes.append({
            "Título": titulo, 
            "Direção": director,
            "Elenco": elenco_str,
            "Nota": nota,
            "Link": link
        })
        time.sleep(1)
    time.sleep(3)

df = pd.DataFrame(filmes)
print(df.head())
df.to_csv("filmes_adorocinema.csv", index=False, encoding="utf-8-sig")