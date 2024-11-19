from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from app.models.user import User
from app.database import SessionLocal
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

# Configuração do OAuth2
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

# Chave secreta e algoritmo usados para assinar o JWT
SECRET_KEY = "your_secret_key"
ALGORITHM = "HS256"

# Dependência para obter o banco de dados
async def get_db():
    async with SessionLocal() as session:
        yield session

# Função para obter o usuário atual
async def get_current_user(
    token: str = Depends(oauth2_scheme), db: AsyncSession = Depends(get_db)
) -> User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        print("Decoded payload:", payload)  # Debug
        user_id = payload.get("sub")
        print("User ID from token:", user_id)  # Debug
        if user_id is None:
            raise credentials_exception
        user_id = int(user_id)
    except JWTError as e:
        print("JWTError:", str(e))  # Debug
        raise credentials_exception

    # Busca o usuário no banco de dados
    result = await db.execute(select(User).where(User.id == user_id))
    user = result.scalars().first()
    if user is None:
        raise credentials_exception
    return user
