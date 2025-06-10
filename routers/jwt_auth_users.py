from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
import jwt, jwt.exceptions
from passlib.context import CryptContext
from datetime import datetime, timedelta
from db.client import db_client


ALGORITHM = "HS256"
TIME_EXPIRE = 40  # segundos
SECRET_KEY = "78eab2372ec19b57f179832653848303b0deef170322ac02ba3c36d2a3fdfce3"

router = APIRouter(prefix="/jwt_auth", tags=["jwt_auth"], responses={404: {"description": "Not found"}})

oauth2 = OAuth2PasswordBearer(tokenUrl="login")



crypt = CryptContext(schemes=["bcrypt"])

class User(BaseModel):
    username: str
    email: str
    full_name: str
    disabled: bool

class UserDB(User):
    password: str


@router.get("/hola")
async def hola():
    return "Holaaaa"


@router.post("/login")
async def login(form: OAuth2PasswordRequestForm = Depends()):
    user_db = db_client.users.find_one({"username": form.username})
    if not user_db:
        raise HTTPException(status_code=400, detail="Incorrect username")
    
    if not crypt.verify(form.password, user_db["password"]):
        raise HTTPException(status_code=400, detail="Incorrect password")
    
    expire = datetime.utcnow() + timedelta(seconds=TIME_EXPIRE)

    access_token = {
        "sub": form.username,
        "exp": expire,
    }
    
    return {
        "access_token": jwt.encode(access_token, SECRET_KEY, algorithm=ALGORITHM),
        "token_type": "bearer",
    }

def search_user(username: str):
    user_db = db_client.users.find_one({"username": username})
    if not user_db:
        return None
    
    return User(
        username=user_db["username"],
        email=user_db["email"],
        full_name=user_db.get("full_name", ""),
        disabled=user_db.get("disabled", False)
    )
    

async def auth_user(token:str = Depends(oauth2)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise HTTPException(status_code=401, detail="Token no valido")
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expirado")
    
    user = search_user(username)
    if not user:
        raise HTTPException(status_code=401, detail="Token no valido")
    
    return user


async def current_user(user: User = Depends(auth_user)):
    
    if user.disabled:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail="Usuario inactivo", 
            headers={"WWW-Authenticate": "Bearer"})
    return user

@router.get("/me")
async def me(user: User = Depends(current_user)):
    return user