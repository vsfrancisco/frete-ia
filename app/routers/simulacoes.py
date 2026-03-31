from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app import crud, models, schemas
from app.database import get_db
from app.services.calculo_frete import calcular_cotacao_spot

router = APIRouter(prefix="/api/simulacoes", tags=["Simulações"])

@router.get("", response_model=list[schemas.SimulacaoFrete])
def listar_simulacoes(skip: int = 0, limit: int = 50, db: Session = Depends(get_db)):
    return db.query(models.SimulacaoFrete).order_by(models.SimulacaoFrete.id.desc()).offset(skip).limit(limit).all()

@router.post("", response_model=schemas.SimulacaoFrete)
def criar_simulacao(dados: schemas.SimulacaoCreate, db: Session = Depends(get_db)):
    return crud.criar_simulacao(db, dados)

@router.post("/spot", response_model=schemas.SimulacaoSpotResponse)
def criar_cotacao_spot_endpoint(dados: schemas.SimulacaoCreate, db: Session = Depends(get_db)):
    opcoes_spot = calcular_cotacao_spot(dados, db)
    if not opcoes_spot:
        raise HTTPException(status_code=400, detail="Nenhum veículo encontrado que suporte esta carga.")
        
    dados.transportadora_id = db.query(models.Transportadora).filter(models.Transportadora.nome == opcoes_spot[0]["transportadora_nome"]).first().id
    dados.veiculo_id = db.query(models.Veiculo).filter(models.Veiculo.nome.startswith(opcoes_spot[0]["veiculo_nome"].split(" ")[0])).first().id
    
    simulacao_salva = crud.criar_simulacao(db, dados)
    
    return {
        "id_simulacao_principal": simulacao_salva.id,
        "opcoes": opcoes_spot
    }

@router.post("/{simulacao_id}/fechar")
def fechar_frete(simulacao_id: int, db: Session = Depends(get_db)):
    simulacao = db.query(models.SimulacaoFrete).filter(models.SimulacaoFrete.id == simulacao_id).first()
    if simulacao:
        simulacao.frete_fechado = True
        db.commit()
        return {"msg": "Frete fechado com sucesso!"}
    return {"erro": "Não encontrado"}

@router.delete("/{simulacao_id}")
def deletar_simulacao_endpoint(simulacao_id: int, db: Session = Depends(get_db)):
    sucesso = crud.deletar_simulacao(db, simulacao_id)
    if not sucesso:
        raise HTTPException(status_code=404, detail="Cotação não encontrada")
    return {"msg": "Cotação excluída com sucesso"}