from fastapi import FastAPI
from src.middlewares.error_handler import ErrorHandler
from src.routers.tareas import tareas_router  # Importa el enrutador de tareas
from src.config.database import Base, engine
from src.models.tareas import Tarea  # Importa el modelo de tareas
from src.routers.auth import auth_router
app = FastAPI()

app.title = "Control gastos API"
app.summary = "Control gastos REST API with FastAPI and Python"
app.description = "This is a demostration of API REST using Python"
app.version = "0.1.0"

app.openapi_tags = [
    {
        "name": "web",
        "description": "Endpoints of example",
    },
    {
        "name": "Tareas",
    },
    {
        "name": "auth",
        "description": "User's authentication",
    },
]


app.add_middleware(ErrorHandler)
app.include_router(prefix="/api/v1/tareas", router=tareas_router)  
app.include_router(prefix="", router=auth_router)
Base.metadata.create_all(bind=engine)


tareas = []
@app.get("/")
def great():
    return {"Hello": "World"}