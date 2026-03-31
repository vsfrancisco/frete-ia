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
        'User-Agent': 'FreteIA/1.0 (seuemail@exemplo.com)' 
    }
    
    # Adicionamos o timeout aqui também para garantir!
    response = requests.get(url, headers=headers, timeout=5)
    response.raise_for_status()
    
    dados = response.json()
    if len(dados) > 0:
        # Retorna lon, lat (nesta ordem para o OSRM)
        return float(dados[0]['lon']), float(dados[0]['lat'])
    
    raise ValueError(f"Não foi possível encontrar a cidade: {cidade_estado}")


def calcular_distancia_osrm(origem: str, destino: str) -> float:
    try:
        # Usamos a função auxiliar que já trata os nomes difíceis
        lon1, lat1 = buscar_coordenadas(origem)
        lon2, lat2 = buscar_coordenadas(destino)

        # Calcula a rota no OSRM
        url_rota = f"http://router.project-osrm.org/route/v1/driving/{lon1},{lat1};{lon2},{lat2}?overview=false"
        
        # O timeout salvador de vidas
        resp_rota = requests.get(url_rota, timeout=5)
        resp_rota.raise_for_status()
        dados_rota = resp_rota.json()

        distancia_metros = dados_rota['routes'][0]['distance']
        return distancia_metros / 1000.0

    except Exception as e:
        print(f"❌ Erro ao buscar distância no mapa: {e}")
        # Se a API externa travar ou a internet cair, a gente retorna 500km provisórios 
        # para a tela não travar infinitamente e o usuário poder digitar na mão.
        return 500.0