import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split

# Variável global para armazenar o modelo treinado em memória
_modelo_ia = None

def treinar_modelo_ia():
    """
    Treina um modelo Random Forest com dados simulados de mercado.
    Na vida real, esses dados viriam das simulações "ganhas" do banco de dados.
    """
    global _modelo_ia
    print("🤖 Treinando IA de precificação de frete...")

    # Gerando 1000 linhas de histórico falso de fretes do mercado
    np.random.seed(42)
    n_samples = 1000
    
    # Features (o que a IA olha)
    distancia = np.random.uniform(50, 1500, n_samples)
    peso = np.random.uniform(1000, 30000, n_samples)
    custo_total = (distancia * 1.5) + (peso * 0.05) # Cálculo genérico de custo
    piso_anttt = distancia * 2.5 # Piso genérico
    
    # Target (o que a IA quer prever: Margem Aceita pelo Cliente em %)
    # Lógica que a IA vai descobrir sozinha:
    # Se a distância é muito longa, a margem cobrada costuma ser menor
    # Se o custo for muito menor que o piso, dá pra colocar mais margem
    margem_aceita = 35.0 - (distancia * 0.01) + ((piso_anttt - custo_total) * 0.005)
    
    # Adicionando um ruído (pois o mercado não é exato)
    margem_aceita += np.random.normal(0, 3, n_samples)
    
    # Garante que a margem nunca seja menor que 5% ou maior que 60%
    margem_aceita = np.clip(margem_aceita, 5.0, 60.0)

    # Montando o DataFrame
    df = pd.DataFrame({
        'distancia': distancia,
        'peso': peso,
        'custo_total': custo_total,
        'piso_anttt': piso_anttt,
        'margem_aceita': margem_aceita
    })

    X = df[['distancia', 'peso', 'custo_total', 'piso_anttt']]
    y = df['margem_aceita']

    # Treinando o modelo (Random Forest é ótimo para isso) [web:99][web:102]
    _modelo_ia = RandomForestRegressor(n_estimators=50, random_state=42)
    _modelo_ia.fit(X, y)
    
    print("✅ IA Treinada com sucesso!")

def sugerir_preco_ia(distancia: float, peso: float, custo_total: float, piso_anttt: float) -> dict:
    """
    Usa o modelo treinado para sugerir a margem e o preço competitivo.
    """
    global _modelo_ia
    
    # Se o modelo não estiver treinado, treina agora
    if _modelo_ia is None:
        treinar_modelo_ia()
        
        # Prepara os dados do frete atual para a IA avaliar
    X_novo = pd.DataFrame({
        'distancia': [distancia],
        'peso': [peso],
        'custo_total': [custo_total],
        'piso_anttt': [piso_anttt]
    })
    
    # IA faz a previsão da margem ideal E JÁ CONVERTE PARA FLOAT DO PYTHON
    margem_sugerida = float(_modelo_ia.predict(X_novo)[0])
    
    # Arredondando para ficar bonito (ex: 18.5%)
    margem_sugerida = round(margem_sugerida, 2)
    
    # Calcula o preço usando a margem da IA (convertendo pra float por garantia)
    preco_ia = float(custo_total * (1 + margem_sugerida / 100.0))
    preco_ia = max(preco_ia, float(piso_anttt)) if piso_anttt > 0 else preco_ia
    
    return {
        "margem_ia": margem_sugerida,
        "preco_ia": round(preco_ia, 2),
        # Mandando como número (85.0) para o PostgreSQL aceitar de boa
        "probabilidade_fechamento": 85.0 if margem_sugerida < 30 else 60.0 
    }
