from pydantic import BaseModel
from typing import Optional

# Transportadora
class TransportadoraBase(BaseModel):
    nome: str
    consumo_km_l: Optional[float] = None
    margem_percentual: float
    custo_manutencao_por_km: float = 0.15
    custo_fixo_mensal: Optional[float] = 5000.0 

class TransportadoraCreate(BaseModel):
    nome: str
    margem_percentual: float
    custo_manutencao_por_km: float

class Transportadora(TransportadoraBase):
    id: int
    class Config:
        from_attributes = True

class VeiculoBase(BaseModel):
    transportadora_id: int
    nome: str
    eixos: int
    consumo_km_l: float
    capacidade_kg: float

class VeiculoCreate(VeiculoBase):
    pass

class Veiculo(VeiculoBase):
    id: int
    class Config:
        from_attributes = True

# Simulação
class SimulacaoCreate(BaseModel):
    transportadora_id: int
    veiculo_id: int
    origem: str
    destino: str
    distancia_km: Optional[float] = None
    peso_kg: float
    tipo_carga: str = "lotacao"
    cliente_nome: Optional[str] = None
    preco_diesel: Optional[float] = None
    valor_carga: Optional[float] = 0.0
    taxa_seguro: Optional[float] = 0.0

class SimulacaoFrete(BaseModel):
    id: int
    transportadora_id: int
    origem: str
    destino: str
    distancia_km: float
    peso_kg: float
    custo_diesel: float
    custo_manutencao: float
    custo_pedagio: float = 0.0
    custo_seguro: float = 0.0
    custo_total: float
    piso_anttt: Optional[float]
    preco_custo_margem: Optional[float]
    preco_sugerido: float
    class Config:
        from_attributes = True
    margem_ia: Optional[float] = None
    preco_ia: Optional[float] = None
    probabilidade_fechamento: Optional[str] = None
    cliente_nome: Optional[str] = None
    frete_fechado: bool = False
    
    class Config:
        from_attributes = True

# ANTT
class TabelaAnttBase(BaseModel):
    tipo_carga: str
    num_eixos: int
    faixa_min_km: int
    faixa_max_km: int
    coef_deslocamento: float
    coef_carga_descarga: float

class TabelaAntt(TabelaAnttBase):
    id: int
    class Config:
        from_attributes = True

# Diesel
class PrecoDieselBase(BaseModel):
    uf: str
    preco_medio: float

class PrecoDiesel(PrecoDieselBase):
    id: int
    class Config:
        from_attributes = True

class OpcaoSpot(BaseModel):
    transportadora_nome: str
    veiculo_nome: str
    custo_total: float
    preco_sugerido: float
    preco_ia: float
    probabilidade_fechamento: float

class SimulacaoSpotResponse(BaseModel):
    id_simulacao_principal: int
    opcoes: list[OpcaoSpot]
