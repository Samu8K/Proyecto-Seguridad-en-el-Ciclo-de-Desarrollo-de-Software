from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.routes import ingestion, metrics, interactive_exercises
from app.api.routes.challenges_new import router as challenges_router
from app.core.config import settings

app = FastAPI(
    title="🛡️ Secure Coding Dojo - Plataforma Educativa Interactiva",
    description="Aprende seguridad en la codificación mediante ejercicios prácticos, desafíos y simulaciones de ataques reales",
    version="2.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # En producción restringir a localhost:3000
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Incluir todas las rutas
app.include_router(challenges_router)
app.include_router(ingestion.router)
app.include_router(metrics.router)
app.include_router(interactive_exercises.router)

@app.get("/health")
async def health():
    return {
        "status": "ok",
        "service": "Secure Coding Dojo",
        "version": "2.0.0",
        "features": [
            "Interactive Exercises",
            "Attack Simulation",
            "Progressive Learning",
            "Real Vulnerabilities",
            "Educational Content"
        ]
    }

@app.get("/")
async def root():
    return {
        "message": "Bienvenido a Secure Coding Dojo",
        "description": "Plataforma educativa para aprender seguridad en la codificación",
        "endpoints": {
            "exercises": "/api/exercises/all",
            "progression": "/api/exercises/progression",
            "health": "/health"
        }
    }

