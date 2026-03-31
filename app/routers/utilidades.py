from fastapi import APIRouter, Response
from app.services.gerar_pdf import gerar_relatorio_frete

router = APIRouter(tags=["Ferramentas Extra"])

@router.post("/gerar-pdf/")
def gerar_pdf(dados: dict):
    try:
        pdf_buffer = gerar_relatorio_frete(
            dados_frete=dados,
            transportadora_nome=dados.get("transportadora_nome", "N/A"),
            veiculo_nome=dados.get("veiculo_nome", "N/A")
        )
        pdf_bytes = pdf_buffer.getvalue()
        pdf_buffer.close()
        
        return Response(
            content=pdf_bytes,
            media_type="application/pdf",
            headers={"Content-Disposition": "attachment; filename=cotacao_frete.pdf"}
        )
    except Exception as e:
        print(f"Erro ao gerar PDF: {e}")
        return {"erro": str(e)}