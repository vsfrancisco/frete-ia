from sqlalchemy.orm import Session
from . import models
from .schemas import TransportadoraCreate, SimulacaoCreate

# Transportadora
def criar_transportadora(db: Session, dados: TransportadoraCreate):
    db_obj = models.Transportadora(**dados.model_dump())
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj

def listar_transportadoras(db: Session, skip: int = 0, limit: int = 20):
    return db.query(models.Transportadora).offset(skip).limit(limit).all()

# --- VEÍCULOS ---
def criar_veiculo(db: Session, dados: schemas.VeiculoCreate):
    db_obj = models.Veiculo(**dados.model_dump())
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj

def listar_veiculos_por_transportadora(db: Session, transportadora_id: int):
    return db.query(models.Veiculo).filter(models.Veiculo.transportadora_id == transportadora_id).all()

# Simulações
def criar_simulacao(db: Session, dados: schemas.SimulacaoCreate):
    from .services.calculo_frete import calcular_frete_completo
    
    calculo = calcular_frete_completo(dados, db)
    
    # Removemos o tipo_carga do dicionário para não quebrar o banco atual
    dados_dict = dados.model_dump(exclude={"tipo_carga"})
    
    db_obj = models.SimulacaoFrete(
        **dados_dict,
        # Adicionados os campos que estavam faltando!
        custo_diesel=calculo.get("custo_diesel"),
        custo_manutencao=calculo.get("custo_manutencao"),
        custo_total=calculo.get("custo_total"),
        piso_anttt=calculo.get("piso_anttt"),
        preco_custo_margem=calculo.get("preco_custo_margem"),
        preco_sugerido=calculo.get("preco_sugerido"),
        margem_ia=calculo.get("margem_ia"),
        preco_ia=calculo.get("preco_ia"),
        probabilidade_fechamento=calculo.get("probabilidade_fechamento")
    )
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj

def listar_simulacoes(db: Session, skip: int = 0, limit: int = 20):
    return db.query(models.SimulacaoFrete).offset(skip).limit(limit).all()

# ANTT
def listar_tabela_anttt(db: Session):
    return db.query(models.TabelaAntt).all()
