from fastapi import FastAPI, HTTPException
from datetime import datetime, time
try:
    from .models import UserProfile, AccessRequest, AccessResponse
except ImportError:
    from models import UserProfile, AccessRequest, AccessResponse

app = FastAPI(title="Aurora Kids Alfa API", description="Protocolo de Segurança Digital Infantil")

# Simulação de Banco de Dados
users_db = {
    "user123": UserProfile(
        id="user123",
        name="João Silva",
        cpf="123.456.789-00",
        birth_date=datetime(2012, 5, 20),
        is_minor=True
    )
}

def is_curfew_active() -> bool:
    """Verifica se o Toque de Recolher Digital (00:00 - 06:00) está ativo."""
    now = datetime.now().time()
    start = time(0, 0)
    end = time(6, 0)
    return start <= now <= end

@app.post("/validate-access", response_model=AccessResponse)
async def validate_access(request: AccessRequest):
    user = users_db.get(request.user_id)
    if not user:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")
    
    # Regra de Ouro: Se for menor de 16 e estiver no horário de toque de recolher
    if user.age < 16 and is_curfew_active():
        return AccessResponse(
            allowed=False,
            reason="Toque de Recolher Digital Ativo (00:00 - 06:00). Proteção Aurora Kids Alfa."
        )
    
    return AccessResponse(allowed=True, reason="Acesso permitido.")

@app.get("/health")
async def health_check():
    return {"status": "online", "timestamp": datetime.now()}
