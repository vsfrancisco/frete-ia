from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from app.database import Base, engine
# Importando nossos novos módulos organizados:
from app.routers import views, simulacoes, admin, cadastros, utilidades, configuracoes

# Criação do Banco de Dados
Base.metadata.create_all(bind=engine)

# Instância Mestre do FastAPI
app = FastAPI(title="Frete IA Pro", description="SaaS de precificação de fretes com Inteligência Artificial")

# Servindo os arquivos estáticos (CSS/Imagens)
app.mount("/static", StaticFiles(directory="static"), name="static")

# Registrando todas as gavetas (Routers) na cômoda principal
app.include_router(views.router)
app.include_router(simulacoes.router)
app.include_router(admin.router)
app.include_router(cadastros.router)
app.include_router(utilidades.router)
app.include_router(configuracoes.router)

@app.get("/health")
def health():
    return {"status": "O Frete IA está respirando forte na Nuvem!"}