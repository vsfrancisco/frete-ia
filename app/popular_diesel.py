from app.database import SessionLocal, engine
from app.models import Base, PrecoDiesel

Base.metadata.create_all(bind=engine)
db = SessionLocal()

# Preços médios de Diesel S-10 no Brasil (Março 2026) [web:79]
precos_atuais = [
    {"uf": "SP", "preco_medio": 6.10},
    {"uf": "RJ", "preco_medio": 6.15},
    {"uf": "MG", "preco_medio": 6.10},
    {"uf": "PR", "preco_medio": 6.15},
    {"uf": "SC", "preco_medio": 6.12},
    {"uf": "RS", "preco_medio": 6.18},
    {"uf": "BA", "preco_medio": 6.70},
    {"uf": "PE", "preco_medio": 5.89},
    {"uf": "CE", "preco_medio": 6.43},
    {"uf": "GO", "preco_medio": 6.20},
    {"uf": "MT", "preco_medio": 6.30},
    {"uf": "AM", "preco_medio": 7.29},
    {"uf": "AC", "preco_medio": 8.40},  # Diesel mais caro
]

for p in precos_atuais:
    diesel = db.query(PrecoDiesel).filter(PrecoDiesel.uf == p["uf"]).first()
    if diesel:
        diesel.preco_medio = p["preco_medio"]
    else:
        db.add(PrecoDiesel(**p))

db.commit()
print('✅ Preços do Diesel S-10 por UF populados com sucesso!')
db.close()
