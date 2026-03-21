from database import SessionLocal
from models import Transportadora, SimulacaoFrete
from schemas import TransportadoraCreate, SimulacaoFreteCreate
from crud import criar_transportadora, criar_simulacao
from services.calculo_frete import calcular_frete_completo

db = SessionLocal()

# Teste 1
transp = TransportadoraCreate(nome="TESTE", consumo_km_l=2.5, margem_percentual=20, custo_manutencao_por_km=0.15)
t = criar_transportadora(db, transp)
print(f"Transportadora ID: {t.id}")

# Teste 2
dados = SimulacaoFreteCreate(
    transportadora_id=t.id, origem="SP", destino="Campinas", 
    distancia_km=100, peso_kg=5000
)
calc = calcular_frete_completo(dados, db)
print(f"Cálculo: {calc}")

db.close()
