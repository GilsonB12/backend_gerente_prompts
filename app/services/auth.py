from passlib.context import CryptContext
from datetime import datetime, timedelta, timezone
from jose import JWTError, jwt

# Configurações para hashing e JWT
SECRET_KEY = "your_secret_key"  # Troque por uma chave segura
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    return pwd_context.hash(password)

def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    # Certifique-se de que o "sub" é um string ou int válido
    # Certifique-se de que o "sub" é o ID do usuário (um inteiro)
    to_encode["sub"] = str(data.get("user_id"))  # Pegue o user_id corretamente do dicionário data
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
