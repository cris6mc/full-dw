from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

router = APIRouter(prefix="/users", tags=["users"], responses={404: {"description": "Not found"}})


class User(BaseModel):
    id: int
    name: str
    age: int
    url: str
    birthday: str

users_list = [
    User(id=1, name="Juan", age=30, url="https://example.com/juan", birthday="1993-01-01"),
    User(id=2, name="Ana", age=25, url="https://example.com/ana", birthday="1998-02-02"),
    User(id=3, name="Pedro", age=40, url="https://example.com/pedro", birthday="1983-03-03"),
    User(id=4, name="Maria", age=35, url="https://example.com/maria", birthday="1988-04-04"),
    User(id=5, name="Luis", age=28, url="https://example.com/luis", birthday="1995-05-05"),
]

def search_user(user_id: int):
    users = filter(lambda user: user.id == user_id, users_list)
    try:
        return list(users)[0]
    except:
        return {"error": "User not found"}


@router.get("/")
async def users():
    return users_list

@router.get("/{user_id}") #path: /user/1
async def user(user_id: int):
    return search_user(user_id)
    
@router.get("/") # query: /userquery/?user_id=1
async def user(user_id: int):
    return search_user(user_id)
    

@router.post("/", response_model= User, status_code=201) #lo que se supode que devuelve si todo va bien
async def user(user:User):
    if type(search_user(user.id)) == User:
        raise HTTPException(status_code=400, detail="User already exists")
    else:
        users_list.append(user)
        return user
    

@router.put("/")
async def user(user: User):
    for index, saved_user in enumerate(users_list):
        if saved_user.id == user.id:
            users_list[index] = user
            return user
    return {"error": "User not found"}


@router.delete("/{user_id}")
async def user(user_id: int):
    for index, saved_user in enumerate(users_list):
        if saved_user.id == user_id:
            del users_list[index]
            return {"message": "User deleted"}
    return {"error": "User not found"}
