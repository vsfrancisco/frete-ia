from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from datetime import datetime
from .database import Base

class Veiculo(Base):
    __tablename__ = "veiculo"

    id = Column(Integer, primary_key=True, index=True)
    transportadora_id = Column(Integer, ForeignKey("transportadora.id"), nullable=False)
    nome = Column(String)  # Ex: "Truck Baú", "Carreta LS"
    eixos = Column(Integer) # Ex: 3, 6
    consumo_km_l = Column(Float) # Substitui o consumo genérico da transportadora
    capacidade_kg = Column(Float)
    transportadora = relationship("Transportadora", back_populates="veiculos")

class SimulacaoFrete(Base):
    __tablename__ = "simulacao_frete"

    id = Column(Integer, primary_key=True, index=True)
    transportadora_id = Column(Integer)
    veiculo_id = Column(Integer, nullable=True)
    origem = Column(String, index=True)
    destino = Column(String, index=True)
    distancia_km = Column(Float)
    peso_kg = Column(Float)
    
    # Campos calculados
    custo_diesel = Column(Float)
    custo_manutencao = Column(Float)  
    custo_total = Column(Float)
    piso_anttt = Column(Float, nullable=True)  
    preco_custo_margem = Column(Float, nullable=True)  
    preco_sugerido = Column(Float)
    data_simulacao = Column(DateTime, default=datetime.utcnow)
    margem_ia = Column(Float, nullable=True)
    preco_ia = Column(Float, nullable=True)
    probabilidade_fechamento = Column(String, nullable=True)
    cliente_nome = Column(String(150), nullable=True)
    frete_fechado = Column(Boolean, default=False)
    custo_pedagio = Column(Float, default=0.0)
    custo_seguro = Column(Float, default=0.0)


class Transportadora(Base):
    __tablename__ = "transportadora"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, index=True)
    consumo_km_l = Column(Float)  # consumo médio da frota
    margem_percentual = Column(Float)  # margem padrão
    custo_manutencao_por_km = Column(Float, default=0.15)  # R$/km
    custo_fixo_mensal = Column(Float, default=5000)  # rateado depois
    veiculos = relationship("Veiculo", back_populates="transportadora")

class TabelaAntt(Base):
    __tablename__ = "tabela_antt"
    
    id = Column(Integer, primary_key=True)
    tipo_carga = Column(String)  # "Geral", "Granel", "Frigorificada"
    num_eixos = Column(Integer)
    faixa_min_km = Column(Integer)
    faixa_max_km = Column(Integer)
    coef_deslocamento = Column(Float)  # CCD R$/km
    coef_carga_descarga = Column(Float)  # CC R$
    vigencia = Column(String)  # "2026-01"

class PrecoDiesel(Base):
    __tablename__ = "preco_diesel"

    id = Column(Integer, primary_key=True)
    uf = Column(String(2), unique=True, index=True)
    preco_medio = Column(Float)
    data_atualizacao = Column(DateTime, default=datetime.utcnow)

class ClienteVIP(Base):
    __tablename__ = "cliente_vip"
    
    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String(150), unique=True, index=True, nullable=False)
    desconto_percentual = Column(Float, default=0.0)
    ativo = Column(Boolean, default=True)

class Configuracao(Base):
    __tablename__ = "configuracoes"

    id = Column(Integer, primary_key=True, index=True)
    preco_diesel = Column(Float, default=5.90)
    taxa_seguro = Column(Float, default=0.30)
    margem_padrao = Column(Float, default=20.0)