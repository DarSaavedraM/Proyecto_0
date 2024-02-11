from fastapi import FastAPI
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
import os
from config.database import engine, Base
from middlewares.error_handler import ErrorHandler
from routers.task import task_router
from routers.category import category_router
from routers.usuarios import usuario_router

app = FastAPI()
app.title = "David Saavedra. Proyecto 0."

app.add_middleware(ErrorHandler)
app.include_router(task_router)
app.include_router(category_router)
app.include_router(usuario_router)
app.mount("/static", StaticFiles(directory="static"), name="static")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


Base.metadata.create_all(bind=engine) 

os.makedirs("static/profile_images", exist_ok=True)

@app.get('/')
def message():
    return JSONResponse(content={"message": "Hello world!"})





