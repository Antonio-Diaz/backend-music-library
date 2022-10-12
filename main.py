from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from config.Environment import get_environment_variables
from metadata.Tags import Tags
from models.BaseModel import init

from routers.v1.AuthRouter import AuthRouter
from routers.v1.InformationRouter import InformationRouter
from routers.v1.MusicRouter import MusicRouter
# Application Environment Configuration
env = get_environment_variables()

# Core Application Instance
app = FastAPI(
    title=env.APP_NAME,
    version=env.API_VERSION,
    description=env.APP_DESCRIPTION,
    openapi_tags=Tags,
)

# CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Add Routers
app.include_router(InformationRouter, prefix="/api/v1", tags=["Usuarios"])
app.include_router(MusicRouter, prefix="/api/v1", tags=["Mis Gustos"])
app.include_router(AuthRouter, prefix="/api/v1", tags=["Autenticación"])
# Initialise Data Model Attributes
init()
