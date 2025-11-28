from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from api.routes.system_routes import router as system_router
from api.routes.task_routes import router as task_router
from api.routes.event_routes import router as event_router
from api.routes.blueprint_routes import router as blueprint_router
from api.routes.income_routes import router as income_router
from api.routes.worker_routes import router as worker_router

app = FastAPI(
    title="Nomad Engine v1.5 API",
    version="1.5",
    description="Autonomous income generation engine API layer"
)

# CORS for dashboards / extensions
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_credentials=True,
    allow_headers=["*"],
)

# ROUTES
app.include_router(system_router)
app.include_router(task_router)
app.include_router(event_router)
app.include_router(blueprint_router)
app.include_router(income_router)
app.include_router(worker_router)


@app.get("/")
def root():
    return {
        "engine": "Nomad v1.5",
        "status": "online",
        "message": "Nomad API ready"
    }