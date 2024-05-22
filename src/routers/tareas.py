from fastapi import APIRouter, Body, status, Query, Path
from typing import List
from datetime import date
from fastapi.responses import JSONResponse
from src.schemas.tareas import Tarea, TareaCreate
from src.models.tareas import Tarea as TareaModel
from src.repositories.tareas import TareaRepository
from src.config.database import SessionLocal
from fastapi.encoders import jsonable_encoder
from src.auth import auth_handler
from typing import Annotated
from fastapi.security import HTTPAuthorizationCredentials
from src.auth.has_access import security
from fastapi import Depends

tareas_router = APIRouter()

@tareas_router.get(
    "/no_completadas",
    tags=["tareas"],
    response_model=List[Tarea],
    description="Returns all tareas that are not completed",
)
def get_tareas_no_completadas(
    credentials: Annotated[HTTPAuthorizationCredentials, Depends(security)]
) -> List[Tarea]:
    if auth_handler.verify_jwt(credentials):
        db = SessionLocal()
        credential = credentials.credentials
        owner_id = auth_handler.decode_token(credential)["user.id"]
        result = TareaRepository(db).get_tareas_no_completadas(owner_id)
        return JSONResponse(
            content=jsonable_encoder(result), status_code=status.HTTP_200_OK
        )
    else:
        return JSONResponse(
            content={"message": "Invalid credentials"},
            status_code=status.HTTP_401_UNAUTHORIZED,
        )
@tareas_router.delete(
    "/completadas",
    tags=["tareas"],
    response_model=dict,
    description="Removes all completed tareas",
)
def remove_tareas_completadas(
    credentials: Annotated[HTTPAuthorizationCredentials, Depends(security)],
) -> dict:
    if auth_handler.verify_jwt(credentials):
        db = SessionLocal()
        credential = credentials.credentials
        owner_id = auth_handler.decode_token(credential)["user.id"]
        TareaRepository(db).delete_tareas_completadas(owner_id)
        return JSONResponse(
            content={"message": "All completed tareas were removed successfully", "data": None},
            status_code=status.HTTP_200_OK,
        )
    else:
        return JSONResponse(
            content={"message": "Invalid credentials"},
            status_code=status.HTTP_401_UNAUTHORIZED,
        )
@tareas_router.get(
    "/",
    tags=["tareas"],
    response_model=List[Tarea],
    description="Returns all tareas stored",
)
def get_all_tareas(
    credentials: Annotated[HTTPAuthorizationCredentials, Depends(security)],
    min_valor: float = Query(default=None, min=10, max=5000000),
    max_valor: float = Query(default=None, min=10, max=5000000),
    offset: int = Query(default=None, min=0),
    limit: int = Query(default=None, min=1),
) -> List[Tarea]:
    if auth_handler.verify_jwt(credentials):
        db = SessionLocal()
        credential = credentials.credentials
        owner_id = auth_handler.decode_token(credential)["user.id"]
        result = TareaRepository(db).get_tareas(
            min_valor, max_valor, offset, limit, owner_id
        )
        return JSONResponse(
            content=jsonable_encoder(result), status_code=status.HTTP_200_OK
        )
    else:
        return JSONResponse(
            content={"message": "Invalid credentials"},
            status_code=status.HTTP_401_UNAUTHORIZED,
        )
    
@tareas_router.get(
    "/{id}",
    tags=["tareas"],
    response_model=Tarea,
    description="Returns data of one specific tarea",
)
def get_tarea(
    credentials: Annotated[HTTPAuthorizationCredentials, Depends(security)],
    id: int = Path(ge=1, le=5000),
) -> Tarea:
    if auth_handler.verify_jwt(credentials):
        db = SessionLocal()
        element = TareaRepository(db).get_tarea(id)
        if not element:
            return JSONResponse(
                content={
                    "message": "The requested tarea was not found",
                    "data": None,
                },
                status_code=status.HTTP_404_NOT_FOUND,
            )
        return JSONResponse(
            content=jsonable_encoder(element), status_code=status.HTTP_200_OK
        )
    else:
        return JSONResponse(
            content={"message": "Invalid credentials"},
            status_code=status.HTTP_401_UNAUTHORIZED,
        )
    
@tareas_router.post(
    "/", tags=["tareas"], response_model=dict, description="Creates a new tarea"
)
def create_tarea(
    credentials: Annotated[HTTPAuthorizationCredentials, Depends(security)],
    tarea: TareaCreate = Body(),
) -> dict:
    if auth_handler.verify_jwt(credentials):
        db = SessionLocal()
        credential = credentials.credentials
        owner_id = auth_handler.decode_token(credential)["user.id"]
        new_tarea = TareaRepository(db).create_tarea(tarea, owner_id)
        return JSONResponse(
            content={
                "message": "The tarea was successfully created",
                "data": jsonable_encoder(new_tarea),
            },
            status_code=status.HTTP_201_CREATED,
        )
    else:
        return JSONResponse(
            content={"message": "Invalid credentials"},
            status_code=status.HTTP_401_UNAUTHORIZED,
        )
@tareas_router.put(
    "/{id}",
    tags=["tareas"],
    response_model=dict,
    description="Updates the data of specific tarea",
)
def update_tarea(
    credentials: Annotated[HTTPAuthorizationCredentials, Depends(security)],
    id: int = Path(ge=1),
    tarea: TareaCreate = Body(),
) -> dict:
    if auth_handler.verify_jwt(credentials):
        db = SessionLocal()
        element = TareaRepository(db).update_tarea(id, tarea)
        return JSONResponse(
            content={
                "message": "The tarea was successfully updated",
                "data": jsonable_encoder(element),
            },
            status_code=status.HTTP_200_OK,
        )
    else:
        return JSONResponse(
            content={"message": "Invalid credentials"},
            status_code=status.HTTP_401_UNAUTHORIZED,
        )


@tareas_router.delete(
    "/{id}",
    tags=["tareas"],
    response_model=dict,
    description="Removes specific tarea",
)
def remove_tarea(
    credentials: Annotated[HTTPAuthorizationCredentials, Depends(security)],
    id: int = Path(ge=1),
) -> dict:
    if auth_handler.verify_jwt(credentials):
        db = SessionLocal()
        TareaRepository(db).delete_tarea(id)
        return JSONResponse(
            content={"message": "The tarea was removed successfully", "data": None},
            status_code=status.HTTP_200_OK,
        )
    else:
        return JSONResponse(
            content={"message": "Invalid credentials"},
            status_code=status.HTTP_401_UNAUTHORIZED,
        )
###
@tareas_router.get(
    "/fecha_limite/{fecha_limite}",
    tags=["tareas"],
    response_model=List[Tarea],
    description="Returns all tareas with a specific fecha_limite",
)
def get_tareas_by_fecha_limite(
    credentials: Annotated[HTTPAuthorizationCredentials, Depends(security)],
    fecha_limite: date = Path(...),
) -> List[Tarea]:
    if auth_handler.verify_jwt(credentials):
        db = SessionLocal()
        credential = credentials.credentials
        owner_id = auth_handler.decode_token(credential)["user.id"]
        result = TareaRepository(db).get_tareas_by_fecha_limite(
            fecha_limite, owner_id
        )
        return JSONResponse(
            content=jsonable_encoder(result), status_code=status.HTTP_200_OK
        )
    else:
        return JSONResponse(
            content={"message": "Invalid credentials"},
            status_code=status.HTTP_401_UNAUTHORIZED,
        )

@tareas_router.get(
    "/prioridad/{prioridad}",
    tags=["tareas"],
    response_model=List[Tarea],
    description="Returns all tareas with a specific prioridad",
)
def get_tareas_by_prioridad(
    credentials: Annotated[HTTPAuthorizationCredentials, Depends(security)],
    prioridad: int = Path(..., ge=1, le=3),
) -> List[Tarea]:
    if auth_handler.verify_jwt(credentials):
        db = SessionLocal()
        credential = credentials.credentials
        owner_id = auth_handler.decode_token(credential)["user.id"]
        result = TareaRepository(db).get_tareas_by_prioridad(
            prioridad, owner_id
        )
        return JSONResponse(
            content=jsonable_encoder(result), status_code=status.HTTP_200_OK
        )
    else:
        return JSONResponse(
            content={"message": "Invalid credentials"},
            status_code=status.HTTP_401_UNAUTHORIZED,
        )

@tareas_router.get(
    "/categoria/{categoria}",
    tags=["tareas"],
    response_model=List[Tarea],
    description="Returns all tareas with a specific categoria",
)
def get_tareas_by_categoria(
    credentials: Annotated[HTTPAuthorizationCredentials, Depends(security)],
    categoria: str = Path(...),
) -> List[Tarea]:
    if auth_handler.verify_jwt(credentials):
        db = SessionLocal()
        credential = credentials.credentials
        owner_id = auth_handler.decode_token(credential)["user.id"]
        result = TareaRepository(db).get_tareas_by_categoria(
            categoria, owner_id
        )
        return JSONResponse(
            content=jsonable_encoder(result), status_code=status.HTTP_200_OK
        )
    else:
        return JSONResponse(
            content={"message": "Invalid credentials"},
            status_code=status.HTTP_401_UNAUTHORIZED,
        )

@tareas_router.put(
    "/completar/{id}",
    tags=["tareas"],
    response_model=Tarea,
    description="Marks a tarea as completed",
)
def marcar_tarea_completa(
    credentials: Annotated[HTTPAuthorizationCredentials, Depends(security)],
    id: int = Path(..., ge=1),
) -> Tarea:
    if auth_handler.verify_jwt(credentials):
        db = SessionLocal()
        result = TareaRepository(db).marcar_tarea_completa(id)
        return JSONResponse(
            content=jsonable_encoder(result), status_code=status.HTTP_200_OK
        )
    else:
        return JSONResponse(
            content={"message": "Invalid credentials"},
            status_code=status.HTTP_401_UNAUTHORIZED,
        )

