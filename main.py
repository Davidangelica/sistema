from fastapi import FastAPI
from routers.administrador import router as ra
from routers.empleados import router as re
from routers.productos import router as rp
from seguridad.autenticacion_admin import router as rad
from seguridad.autenticacion_empleado import router as rae

# app
app = FastAPI()

# routers
app.include_router(ra)
app.include_router(re)
app.include_router(rp)
app.include_router(rad)
app.include_router(rae)