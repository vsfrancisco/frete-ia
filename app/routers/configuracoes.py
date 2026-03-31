from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from pydantic import BaseModel
from app.database import get_db
from app.models import Configuracao  # Ajuste o import se o seu arquivo de models tiver outro nome

router = APIRouter(prefix="/api/configuracoes", tags=["Configurações"])

# Modelo de dados que vamos receber da tela
class ConfigUpdate(BaseModel):
    preco_diesel: float
    taxa_seguro: float
    margem_padrao: float

@router.get("/")
def ler_configuracoes(db: Session = Depends(get_db)):
    # Busca a primeira (e única) linha de configuração
    config = db.query(Configuracao).first()
    
    # Se não existir ainda, cria uma padrão na hora e salva
    if not config:
        config = Configuracao(preco_diesel=5.90, taxa_seguro=0.30, margem_padrao=20.0)
        db.add(config)
        db.commit()
        db.refresh(config)
        
    return config

@router.put("/")
def atualizar_configuracoes(dados: ConfigUpdate, db: Session = Depends(get_db)):
    config = db.query(Configuracao).first()
    
    # Se por acaso não existir, cria
    if not config:
        config = Configuracao()
        db.add(config)
        
    # Atualiza com os valores novos que vieram da tela
    config.preco_diesel = dados.preco_diesel
    config.taxa_seguro = dados.taxa_seguro
    config.margem_padrao = dados.margem_padrao
    
    db.commit()
    db.refresh(config)
    
    return {"mensagem": "Configurações atualizadas com sucesso!", "config": config}