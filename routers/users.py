from fastapi import APIRouter, HTTPException, status
from models.users import (
    User,
    GetUsersResponse,
    CreateUserResponse,
    DeleteUserResponse,
)

router = APIRouter()

usuarios: list[User] = [
    User(id=1, name="juan perez"),
    User(id=2, name="pepe sanchez"),
]


@router.get("/user")
def get_users(is_active: bool | None = None) -> GetUsersResponse:
    # Sin el query param ?is_active, devuelve todos los usuarios
    if is_active is None:
        return GetUsersResponse(users=usuarios)

    # Crea una lista nueva solo con los usuarios del estado pedido
    filtrados = [user for user in usuarios if user.is_active == is_active]
    return GetUsersResponse(users=filtrados)


@router.delete("/user/{id}")
def delete_user(id: int) -> DeleteUserResponse:
    for user in usuarios:
        if user.id == id:
            usuarios.remove(user)
            return DeleteUserResponse(message="usuario borrado")

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Usuario no encontrado"
    )


# status_code: responde 201 (creado) en lugar del 200 por defecto
@router.post("/user", status_code=status.HTTP_201_CREATED)
def create_user(user: User) -> CreateUserResponse:
    # Si el id ya existe, corta con un 409 y no agrega el usuario
    for existing_user in usuarios:
        if existing_user.id == user.id:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Ya existe un usuario con ese id"
            )

    usuarios.append(user)
    return CreateUserResponse(message="usuario creado")
