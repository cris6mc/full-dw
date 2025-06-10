from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

router = APIRouter()

oauth2 = OAuth2PasswordBearer(tokenUrl="login")

class User(BaseModel):
    username: str
    email: str
    full_name: str
    disabled: bool

class UserDB(User):
    password: str

users_db = {
    "johndoe": {
        "username": "johndoe",
        "full_name": "John Doe",
        "email": "jhondoe@gmail.com",
        "disabled": False,
        "password": "123456",
    },
    "alice": {
        "username": "alice",
        "full_name": "Alice",
        "email": "fggfs@gmail.com",
        "disabled": False,
        "password": "654123",
    },
    "johndoe2": {
        "username": "johndoe2",
        "full_name": "John Doe",
        "email": "jhondoe2@gmail.com",
        "disabled": True,
        "password": "987456",
    },
}

def search_user(username: str):
    if username in users_db:
        return User(**users_db[username])
    
async def current_user(token: str = Depends(oauth2)):
    user = search_user(token)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail="Credenciales invalidas", 
            headers={"WWW-Authenticate": "Bearer"})
    if user.disabled:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail="Usuario inactivo", 
            headers={"WWW-Authenticate": "Bearer"})
    return user
    
@router.post("/login")
async def login(form: OAuth2PasswordRequestForm = Depends()):
    user_db = users_db.get(form.username)
    if not user_db:
        raise HTTPException(status_code=400, detail="Incorrect username")
    
    if not form.password == user_db["password"]:
        raise HTTPException(status_code=400, detail="Incorrect password")
    
    return {
        "access_token": form.username,
        "token_type": "bearer",
    }

@router.get("/users/me_basic")
async def me(user: User = Depends(current_user)):
    return user