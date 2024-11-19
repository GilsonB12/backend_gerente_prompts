from fastapi import FastAPI
from app.routers import auth, prompt
from fastapi.security import OAuth2PasswordBearer

app = FastAPI()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

# Inclui o roteador de autenticação
app.include_router(auth.router, prefix="/auth", tags=["auth"])
app.include_router(prompt.router, prefix="/prompts", tags=["prompts"])