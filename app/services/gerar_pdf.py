from reportlab.lib.pagesizes import letter, A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib import colors
from io import BytesIO
from datetime import datetime

def to_float(valor, padrao=0.0):
    if valor is None:
        return padrao
    if isinstance(valor, str):
        # Remove símbolos de porcentagem e converte vírgula pra ponto
        valor = valor.replace("%", "").strip().replace(",", ".")
    try:
        return float(valor)
    except ValueError:
        return padrao

def gerar_relatorio_frete(dados_frete: dict, transportadora_nome: str, veiculo_nome: str) -> BytesIO:
    """
    Gera um PDF profissional com o relatório da cotação de frete.
    Retorna um BytesIO que pode ser downloadado.
    """
    
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4, topMargin=0.5*inch, bottomMargin=0.5*inch)
    elements = []
    styles = getSampleStyleSheet()
    
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=24,
        textColor=colors.HexColor('#4F46E5'),
        spaceAfter=6,
        alignment=1
    )
    
    subtitle_style = ParagraphStyle(
        'CustomSubtitle',
        parent=styles['Normal'],
        fontSize=10,
        textColor=colors.HexColor('#6B7280'),
        spaceAfter=20,
        alignment=1
    )
    
    elements.append(Paragraph("📋 COTAÇÃO DE FRETE", title_style))
    elements.append(Paragraph(f"Gerado em {datetime.now().strftime('%d/%m/%Y às %H:%M:%S')}", subtitle_style))
    elements.append(Spacer(1, 0.3*inch))
    
    # --- CONVERSÃO SEGURA DE TODOS OS NÚMEROS ---
    distancia_km = to_float(dados_frete.get('distancia_km', 0))
    peso_kg = to_float(dados_frete.get('peso_kg', 0))
    custo_diesel = to_float(dados_frete.get('custo_diesel', 0))
    custo_manutencao = to_float(dados_frete.get('custo_manutencao', 0))
    custo_total = to_float(dados_frete.get('custo_total', 0))
    piso_anttt = to_float(dados_frete.get('piso_anttt', 0))
    preco_sugerido = to_float(dados_frete.get('preco_sugerido', 0))
    preco_ia = to_float(dados_frete.get('preco_ia', 0))
    margem_ia = to_float(dados_frete.get('margem_ia', 0))
    prob_fechamento = to_float(dados_frete.get('probabilidade_fechamento', 0))

    # ====== SEÇÃO 1: INFORMAÇÕES GERAIS ======
    info_data = [
        ['TRANSPORTADORA', transportadora_nome],
        ['VEÍCULO', veiculo_nome],
        ['ORIGEM', dados_frete.get('origem', 'N/A')],
        ['DESTINO', dados_frete.get('destino', 'N/A')],
        ['DISTÂNCIA', f"{distancia_km:.2f} km"],
        ['PESO', f"{peso_kg:.0f} kg"],
    ]
    
    info_table = Table(info_data, colWidths=[2*inch, 3*inch])
    info_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#E0E7FF')),
        ('TEXTCOLOR', (0, 0), (0, -1), colors.HexColor('#312E81')),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
        ('TOPPADDING', (0, 0), (-1, -1), 8),
        ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#D1D5DB')),
    ]))
    
    elements.append(info_table)
    elements.append(Spacer(1, 0.3*inch))
    
    # ====== SEÇÃO 2: BREAKDOWN DE CUSTOS ======
    elements.append(Paragraph("Análise de Custos", styles['Heading2']))
    elements.append(Spacer(1, 0.1*inch))
    
    costs_data = [
        ['Descrição', 'Valor (R$)'],
        ['Diesel + Transporte', f"R$ {custo_diesel + custo_manutencao:.2f}"],
        ['Custo Total Técnico', f"R$ {custo_total:.2f}"],
        ['Piso Mínimo ANTT', f"R$ {piso_anttt:.2f}"],
        ['Preço Base (Com Margem)', f"R$ {preco_sugerido:.2f}"],
    ]
    
    costs_table = Table(costs_data, colWidths=[3.5*inch, 1.5*inch])
    costs_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#FCA5A5')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 10),
        ('TOPPADDING', (0, 0), (-1, -1), 10),
        ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#D1D5DB')),
    ]))
    
    elements.append(costs_table)
    elements.append(Spacer(1, 0.3*inch))
    
    # ====== SEÇÃO 3: RECOMENDAÇÃO DA IA ======
    elements.append(Paragraph("⚡ Recomendação de Preço (IA)", styles['Heading2']))
    elements.append(Spacer(1, 0.1*inch))
    
    ia_data = [
        ['Preço Sugerido pela IA', f"R$ {preco_ia:.2f}"],
        ['Margem de Lucro', f"{margem_ia:.1f}%"],
        ['Probabilidade de Fechamento', f"{prob_fechamento:.1f}%"],
    ]
    
    ia_table = Table(ia_data, colWidths=[3.5*inch, 1.5*inch])
    ia_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#E9D5FF')),
        ('TEXTCOLOR', (0, 0), (-1, -1), colors.HexColor('#581C87')),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, -1), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 11),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 12),
        ('TOPPADDING', (0, 0), (-1, -1), 12),
        ('GRID', (0, 0), (-1, -1), 2, colors.HexColor('#9333EA')),
    ]))
    
    elements.append(ia_table)
    elements.append(Spacer(1, 0.5*inch))
    
    # ====== RODAPÉ ======
    footer_style = ParagraphStyle(
        'Footer',
        parent=styles['Normal'],
        fontSize=8,
        textColor=colors.HexColor('#9CA3AF'),
        alignment=1
    )
    elements.append(Paragraph("🚚 Frete IA Pro - Sistema de Inteligência Artificial para Logística", footer_style))
    elements.append(Paragraph("Este relatório foi gerado automaticamente pelo sistema.", footer_style))
    
    doc.build(elements)
    buffer.seek(0)
    return buffer
