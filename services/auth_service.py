from sqlalchemy.orm import Session
from fastapi import HTTPException, status, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import JWTError, jwt
from models.models import User
from Utils import verify_password, SECRET_KEY, ALGORITHM
from core.database import get_db
 
security = HTTPBearer()
 
def authenticate_user(db: Session, email: str, password: str):
    user = db.query(User).filter(User.email == email).first()
    if not user or not verify_password(password, user.password):
        return False
    return user
 
def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
 
    try:
        # Decodifica o token
        payload = jwt.decode(
            credentials.credentials,
            SECRET_KEY,
            algorithms=[ALGORITHM]
        )
 
        email: str = payload.get("sub")
        user_id: int = payload.get("id")
 
        # Ambos precisam existir
        if email is None or user_id is None:
            raise credentials_exception
 
    except JWTError:
        raise credentials_exception
 
    # Busca pelo ID para evitar conflito e garantir segurança
    user = db.query(User).filter(User.id == user_id).first()
 
    if user is None:
        raise credentials_exception
 
    return user
 
 