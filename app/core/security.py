import secrets
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from app.core.config import settings

security = HTTPBasic()

def verificar_credenciais(credentials: HTTPBasicCredentials = Depends(security)):
    usuario_digitado = credentials.username.encode("utf-8")
    senha_digitada = credentials.password.encode("utf-8")
    
    usuario_correto = settings.admin_user.encode("utf-8")
    senha_correta = settings.admin_password.encode("utf-8")
    
    usuario_valido = secrets.compare_digest(usuario_digitado, usuario_correto)
    senha_valida = secrets.compare_digest(senha_digitada, senha_correta)
    
    if not (usuario_valido and senha_valida):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Usuário ou senha incorretos",
            headers={"WWW-Authenticate": "Basic"},
        )
    return credentials.username