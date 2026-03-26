from sqlalchemy.orm import Session
from ..schemas import SimulacaoCreate
from ..models import Transportadora, TabelaAntt, PrecoDiesel, Veiculo
from .mapas import calcular_distancia_osrm
from .ia_frete import sugerir_preco_ia

def calcular_frete_completo(dados: SimulacaoCreate, db: Session):
    transportadora = db.query(Transportadora).filter(Transportadora.id == dados.transportadora_id).first()
    veiculo = db.query(Veiculo).filter(Veiculo.id == dados.veiculo_id).first()
    
    if not transportadora or not veiculo:
        raise ValueError("Transportadora ou Veículo não encontrado")
        
    if not dados.distancia_km or dados.distancia_km <= 0:
        dados.distancia_km = calcular_distancia_osrm(dados.origem, dados.destino)

    uf_origem = "SP"
    if "/" in dados.origem:
        uf_origem = dados.origem.split("/")[-1].strip().upper()

        # Se o usuário digitou o diesel na tela, usa ele. Senão, busca do banco.
    if hasattr(dados, 'preco_diesel') and dados.preco_diesel and dados.preco_diesel > 0:
        preco_litro_diesel = dados.preco_diesel
    else:
        diesel_db = db.query(PrecoDiesel).filter(PrecoDiesel.uf == uf_origem).first()
        preco_litro_diesel = diesel_db.preco_medio if diesel_db else 6.50

    
    # 1. CUSTOS DA VIAGEM COMPLETA (CAMINHÃO CHEIO)
    if veiculo.consumo_km_l and veiculo.consumo_km_l > 0:
        custo_diesel_full = (dados.distancia_km / veiculo.consumo_km_l) * preco_litro_diesel
    else:
        custo_diesel_full = (dados.distancia_km / 2.5) * preco_litro_diesel
        
    custo_manutencao_full = dados.distancia_km * transportadora.custo_manutencao_por_km
    custo_total_full = custo_diesel_full + custo_manutencao_full
    
    # 2. PISO ANTT (CAMINHÃO CHEIO)
    piso_row = db.query(TabelaAntt).filter(
        TabelaAntt.faixa_min_km <= dados.distancia_km,
        TabelaAntt.faixa_max_km >= dados.distancia_km,
        TabelaAntt.num_eixos == veiculo.eixos
    ).first()
    
    if piso_row:
        piso_anttt_full = (piso_row.coef_deslocamento * dados.distancia_km) + piso_row.coef_carga_descarga
    else:
        # PLANO B: Se não achar os eixos ou a distância no banco, aplica uma fórmula média nacional
        coef_deslocamento_medio = 1.15 * veiculo.eixos
        coef_carga_descarga_medio = 45.00 * veiculo.eixos
        piso_anttt_full = (coef_deslocamento_medio * dados.distancia_km) + coef_carga_descarga_medio

    # 3. LÓGICA DE FRACIONAMENTO
    tipo = getattr(dados, "tipo_carga", "lotacao")
    
    if tipo == "fracionada":
        # Descobre a porcentagem que a carga ocupa no veículo (máximo 100%)
        proporcao = min(dados.peso_kg / veiculo.capacidade_kg, 1.0)
        
        # Adicionamos uma taxa fixa para cobrir custos de coleta/entrega/manuseio
        taxa_operacional_fracionado = 50.00 
        
        custo_diesel = custo_diesel_full * proporcao
        custo_manutencao = custo_manutencao_full * proporcao
        custo_total = (custo_total_full * proporcao) + taxa_operacional_fracionado
        piso_anttt = piso_anttt_full * proporcao
    else:
        # Lotação padrão
        custo_diesel = custo_diesel_full
        custo_manutencao = custo_manutencao_full
        custo_total = custo_total_full
        piso_anttt = piso_anttt_full
        
    # 4. PREÇO FINAL E IA
    preco_custo_margem = custo_total * (1 + transportadora.margem_percentual / 100.0)
    preco_sugerido = max(preco_custo_margem, piso_anttt) if piso_anttt > 0 else preco_custo_margem
    
    dica_ia = sugerir_preco_ia(dados.distancia_km, dados.peso_kg, custo_total, piso_anttt)
    
    return {
        "custo_diesel": custo_diesel,
        "custo_manutencao": custo_manutencao,
        "custo_total": custo_total,
        "piso_anttt": piso_anttt,
        "preco_custo_margem": preco_custo_margem,
        "preco_sugerido": preco_sugerido,
        "margem_ia": dica_ia["margem_ia"],
        "preco_ia": dica_ia["preco_ia"],
        "probabilidade_fechamento": dica_ia["probabilidade_fechamento"]
    }