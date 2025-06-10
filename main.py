from fastapi import FastAPI
from routers import products, users, jwt_auth_users, basic_auth_users, usersdb
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # o ["http://localhost:3000"]
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Routers
app.include_router(products.router)
app.include_router(users.router)
app.include_router(usersdb.router)
app.include_router(jwt_auth_users.router)
app.include_router(basic_auth_users.router)
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/")
async def root():  # root is like the mane of function 
    return "Hola FastAPI! de Cristian"

@app.get("/url")
async def url():
    return {"url": "http://crismachado.com"}