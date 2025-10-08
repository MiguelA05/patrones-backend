from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.v1.endpoints import router as v1_router

app = FastAPI(title="Patrones API")
app.include_router(v1_router, prefix="/api/v1")


@app.get("/")
def root():
    return {"message": "Bienvenido a la API de búsqueda y validación de patrones"}

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:4200"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)