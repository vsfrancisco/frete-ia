import requests
import urllib.parse

def buscar_coordenadas(cidade_estado: str):
    """
    Usa o Nominatim (OpenStreetMap) para transformar 'Campinas/SP' em Lat e Lng.
    """
    # Formata o texto para a URL (ex: "Campinas/SP" -> "Campinas%2FSP")
    query = urllib.parse.quote(cidade_estado + ", Brazil")
    url = f"https://nominatim.openstreetmap.org/search?q={query}&format=json&limit=1"
    
    headers = {
        'User-Agent': 'FreteIA/1.0 (seuemail@exemplo.com)' # O Nominatim exige um User-Agent
    }
    
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200 and len(response.json()) > 0:
        dados = response.json()[0]
        # Retorna lon, lat (nesta ordem para o OSRM)
        return float(dados['lon']), float(dados['lat'])
    
    raise ValueError(f"Não foi possível encontrar a cidade: {cidade_estado}")

def calcular_distancia_osrm(origem: str, destino: str) -> float:
    """
    Conecta Origem e Destino, pega as coordenadas, bate no OSRM e retorna a distância em KM.
    """
    lon_origem, lat_origem = buscar_coordenadas(origem)
    lon_destino, lat_destino = buscar_coordenadas(destino)
    
    # URL da API de roteamento OSRM (pública)
    url = f"http://router.project-osrm.org/route/v1/driving/{lon_origem},{lat_origem};{lon_destino},{lat_destino}?overview=false"
    
    response = requests.get(url)
    if response.status_code == 200:
        dados = response.json()
        if dados.get("code") == "Ok":
            distancia_metros = dados["routes"][0]["distance"]
            distancia_km = distancia_metros / 1000.0
            return round(distancia_km, 2)
            
    raise ValueError("Não foi possível traçar a rota entre as cidades.")
