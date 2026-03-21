from app.database import SessionLocal, engine
from app.models import Base, TabelaAntt
from sqlalchemy.orm import Session

Base.metadata.create_all(bind=engine)

db: Session = SessionLocal()

# Dados reais Tabela ANTT 2026 - Resolução 6.076 [web:62][web:67]
# Valores aproximados para Carga Geral / 3 eixos (mais comuns para pequenas transportadoras)

dados = [
    # Carga Geral - 3 eixos (típico caminhão toco/truck)
    {"tipo_carga": "Geral", "num_eixos": 3, "faixa_min_km": 0, "faixa_max_km": 99, "coef_deslocamento": 7.49, "coef_carga_descarga": 803.22},
    {"tipo_carga": "Geral", "num_eixos": 3, "faixa_min_km": 100, "faixa_max_km": 199, "coef_deslocamento": 6.82, "coef_carga_descarga": 803.22},
    {"tipo_carga": "Geral", "num_eixos": 3, "faixa_min_km": 200, "faixa_max_km": 499, "coef_deslocamento": 6.35, "coef_carga_descarga": 803.22},
    {"tipo_carga": "Geral", "num_eixos": 3, "faixa_min_km": 500, "faixa_max_km": 999, "coef_deslocamento": 5.94, "coef_carga_descarga": 803.22},
    
    # Carga Geral - 4 eixos (carreta)
    {"tipo_carga": "Geral", "num_eixos": 4, "faixa_min_km": 0, "faixa_max_km": 99, "coef_deslocamento": 9.12, "coef_carga_descarga": 803.22},
    {"tipo_carga": "Geral", "num_eixos": 4, "faixa_min_km": 100, "faixa_max_km": 199, "coef_deslocamento": 8.31, "coef_carga_descarga": 803.22},
    
    # Granel - 3 eixos
    {"tipo_carga": "Granel", "num_eixos": 3, "faixa_min_km": 0, "faixa_max_km": 99, "coef_deslocamento": 7.12, "coef_carga_descarga": 803.22},
    {"tipo_carga": "Granel", "num_eixos": 3, "faixa_min_km": 100, "faixa_max_km": 199, "coef_deslocamento": 6.48, "coef_carga_descarga": 803.22},
]

for d in dados:
    ant = TabelaAntt(**d, vigencia="2026-01")
    db.merge(ant)

db.commit()
print(f"✅ Popularam {len(dados)} linhas da Tabela ANTT 2026")
db.close()
