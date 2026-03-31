from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func

from app.database import get_db
from app import models, schemas

router = APIRouter(prefix="/api", tags=["Painel Administrativo"])

@router.get("/metricas")
def obter_metricas(db: Session = Depends(get_db)):
    total_fechados = db.query(models.SimulacaoFrete).filter(models.SimulacaoFrete.frete_fechado == True).count()
    
    somas = db.query(
        func.sum(models.SimulacaoFrete.preco_ia).label("faturamento"),
        func.sum(models.SimulacaoFrete.custo_total).label("custo")
    ).filter(models.SimulacaoFrete.frete_fechado == True).first()
    
    faturamento = somas.faturamento or 0.0
    custo = somas.custo or 0.0
    
    return {
        "total_fechados": total_fechados, 
        "faturamento": faturamento, 
        "lucro_estimado": faturamento - custo
    }

@router.get("/clientes-vip", response_model=list[schemas.ClienteVIPResponse])
def listar_clientes_vip(db: Session = Depends(get_db)):
    return db.query(models.ClienteVIP).filter(models.ClienteVIP.ativo == True).all()

@router.post("/clientes-vip", response_model=schemas.ClienteVIPResponse)
def criar_cliente_vip(cliente: schemas.ClienteVIPCreate, db: Session = Depends(get_db)):
    db_cliente = db.query(models.ClienteVIP).filter(models.ClienteVIP.nome.ilike(f"%{cliente.nome}%")).first()
    if db_cliente:
        db_cliente.desconto_percentual = cliente.desconto_percentual
        db_cliente.ativo = True
        db.commit()
        db.refresh(db_cliente)
        return db_cliente
        
    novo_cliente = models.ClienteVIP(**cliente.model_dump())
    db.add(novo_cliente)
    db.commit()
    db.refresh(novo_cliente)
    return novo_cliente