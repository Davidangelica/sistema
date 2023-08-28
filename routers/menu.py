from fastapi import APIRouter,Depends
from seguridad.autenticacion_admin import token_auth_admin, verificar_permisos_admin
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from modelos.modelo_administrador import Administrador

router = APIRouter()

router.mount("/static", StaticFiles(directory="front"), name="static")

@router.get('/menuPrincipal/admin/{nombre}')
async def menu(nombre: str, auth=Depends(verificar_permisos_admin)):
    return FileResponse("front/main/main_administrador/main_a.html")


@router.get('/menuPrincipal/empleado/{nombre}')
async def menu(nombre:str, auth=Depends(verificar_permisos_admin)):
    return FileResponse("front/main/main_empleado/main_e.html")