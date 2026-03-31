from fastapi import APIRouter, Depends, Body
from sqlalchemy.orm import Session

from app.database import get_db
from app import crud, schemas

router = APIRouter(tags=["Cadastros Base"])

@router.get("/transportadoras", response_model=list[schemas.Transportadora])
def listar_transportadoras(skip: int = 0, limit: int = 20, db: Session = Depends(get_db)):
    return crud.listar_transportadoras(db, skip=skip, limit=limit)

@router.post("/transportadoras", response_model=schemas.Transportadora)
def criar_transportadora_endpoint(dados: schemas.TransportadoraCreate = Body(...), db: Session = Depends(get_db)):
    return crud.criar_transportadora(db=db, dados=dados)

@router.get("/transportadoras/{transportadora_id}/veiculos", response_model=list[schemas.Veiculo])
def listar_veiculos_transp(transportadora_id: int, db: Session = Depends(get_db)):
    return crud.listar_veiculos_por_transportadora(db, transportadora_id)

@router.post("/veiculos", response_model=schemas.Veiculo)
def criar_veiculo_endpoint(dados: schemas.VeiculoCreate = Body(...), db: Session = Depends(get_db)):
    return crud.criar_veiculo(db=db, dados=dados)