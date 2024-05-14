from fastapi import FastAPI
from fastapi.responses import JSONResponse, RedirectResponse
from routers.Router_Proyecto import router as proyecto_router
from routers.Router_Empleado import router as empleado_router
from routers.Router_AgregarEP import router as proyectoempleado_router
from config.db import engine
from models import Modelos_Empleado_Proyecto

Modelos_Empleado_Proyecto.Base.metadata.create_all(bind=engine)
app = FastAPI(swagger_ui_parameters={"syntaxHighlight": False})

app.include_router(empleado_router, prefix="/api/v1/empleados", tags=["Empleados"])
app.include_router(proyecto_router, prefix="/api/v1/proyectos", tags=["Proyectos"])
app.include_router(proyectoempleado_router, prefix="/api/v1/Asignacion_Proyecto_Empleado", tags=["Proyecto_Empleado"])

@app.exception_handler(Exception)
async def error_handler(request, exc):
    return JSONResponse(status_code=500, content={"message": "Error interno del servidor"})

@app.get("/")
async def root():
    return RedirectResponse(url="/docs")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
