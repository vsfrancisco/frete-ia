from fastapi import APIRouter, Request, Depends
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

# Precisamos importar a segurança do arquivo principal, que ajustaremos no Passo 5
from app.core.security import verificar_credenciais 

router = APIRouter()
templates = Jinja2Templates(directory="templates")

@router.get("/", response_class=HTMLResponse)
async def home(request: Request, username: str = Depends(verificar_credenciais)):
    return templates.TemplateResponse("index.html", {"request": request})

@router.get("/historico", response_class=HTMLResponse)
def tela_historico(request: Request, username: str = Depends(verificar_credenciais)):
    return templates.TemplateResponse("historico.html", {"request": request})

@router.get("/cadastro-transportadora", response_class=HTMLResponse)
def tela_cadastro(request: Request, username: str = Depends(verificar_credenciais)):
    return templates.TemplateResponse("cadastro.html", {"request": request})

@router.get("/cadastro-veiculo", response_class=HTMLResponse)
def tela_cadastro_veiculo(request: Request, username: str = Depends(verificar_credenciais)):
    return templates.TemplateResponse("cadastro_veiculo.html", {"request": request})