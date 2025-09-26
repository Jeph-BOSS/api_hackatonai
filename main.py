from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv

# Charger les variables d'environnement dès le début, avant d'importer les routeurs
load_dotenv()

from routers.upload import router as upload_router
from routers.analyze import router as analyze_router
from routers.map import router as map_router
from middleware.rate_limiter import rate_limit_middleware


def create_app() -> FastAPI:
    app = FastAPI(title="Topo Analyzer API", version="0.1.0")

    # Ajouter le rate limiting AVANT CORS
    app.middleware("http")(rate_limit_middleware)
    
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    app.include_router(upload_router)
    app.include_router(analyze_router)
    app.include_router(map_router)

    return app


app = create_app()



