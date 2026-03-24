from fastapi import FastAPI, Depends, Request, Body
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from .database import Base, engine, SessionLocal
from . import models, crud
from .schemas import Transportadora, TransportadoraCreate, SimulacaoFrete, SimulacaoCreate, TabelaAntt, Veiculo, VeiculoCreate, TransportadoraCreate

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/health")
def health():
    return {"status": "ok"}

@app.get("/transportadoras", response_model=list[Transportadora])
def listar_transportadoras(skip: int = 0, limit: int = 20, db: Session = Depends(get_db)):
    return crud.listar_transportadoras(db, skip=skip, limit=limit)

@app.post("/transportadoras", response_model=Transportadora)
def criar_transportadora(dados: TransportadoraCreate, db: Session = Depends(get_db)):
    return crud.criar_transportadora(db, dados)

@app.get("/simulacoes", response_model=list[SimulacaoFrete])
def listar_simulacoes(skip: int = 0, limit: int = 20, db: Session = Depends(get_db)):
    return crud.listar_simulacoes(db, skip=skip, limit=limit)

@app.post("/simulacoes", response_model=SimulacaoFrete)
def criar_simulacao(dados: SimulacaoCreate, db: Session = Depends(get_db)):
    return crud.criar_simulacao(db, dados)

@app.get("/tabela-antt", response_model=list[TabelaAntt])
def listar_anttt(db: Session = Depends(get_db)):
    return crud.listar_tabela_anttt(db)

@app.post("/veiculos", response_model=Veiculo)
def criar_veiculo(dados: VeiculoCreate, db: Session = Depends(get_db)):
    return crud.criar_veiculo(db, dados)

@app.get("/transportadoras/{transportadora_id}/veiculos", response_model=list[Veiculo])
def listar_veiculos_transp(transportadora_id: int, db: Session = Depends(get_db)):
    return crud.listar_veiculos_por_transportadora(db, transportadora_id)


@app.get("/cadastro-transportadora")
def tela_cadastro(request: Request):
    return templates.TemplateResponse("cadastro.html", {"request": request})

@app.post("/transportadoras/")
def criar_transportadora_endpoint(
    dados: TransportadoraCreate = Body(...), 
    db: Session = Depends(get_db)
):
    return crud.criar_transportadora(db=db, dados=dados)

# Rota para abrir a tela HTML de veículos
@app.get("/cadastro-veiculo")
def tela_cadastro_veiculo(request: Request):
    return templates.TemplateResponse("cadastro_veiculo.html", {"request": request})

# Rota para salvar o veículo no banco de dados
@app.post("/veiculos/")
def criar_veiculo_endpoint(
    dados: VeiculoCreate = Body(...), 
    db: Session = Depends(get_db)
):
    # Chamando exatamente com 'dados=dados' como está no seu crud.py!
    return crud.criar_veiculo(db=db, dados=dados)




