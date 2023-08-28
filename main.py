from fastapi import FastAPI,Depends
from seguridad.autenticacion_admin import token_auth_admin
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from routers.administrador import router as ra
from routers.empleados import router as re
from routers.productos import router as rp
from seguridad.autenticacion_admin import router as rad
from seguridad.autenticacion_empleado import router as rae
from routers.menu import router as rm
from modelos.modelo_administrador import Administrador

# app
app = FastAPI()

app.mount("/static", StaticFiles(directory="front"), name="static")

# routers
app.include_router(ra)
app.include_router(re)
app.include_router(rp)
app.include_router(rad)
app.include_router(rae)
app.include_router(rm)

@app.get('/login/adm')
async def login_adm_page():
    return FileResponse("front/login/administrador/login_admin.html")

@app.get('/index')
async def index_page():
    return FileResponse("front/index.html")

@app.get('/login/emp')
async def login_emp_page():
    return FileResponse("front/login/empleado/login_empleado.html")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
