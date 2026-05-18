from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.routes import router as api_router
from app.api.websockets import ws_router

app = FastAPI(title="Sentinel Swarm API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # In production, restrict this to frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router, prefix="/api/v1")
app.include_router(ws_router)

@app.get("/")
def read_root():
    return {"message": "Welcome to Sentinel Swarm API"}

@app.get("/health")
def health_check():
    return {"status": "healthy"}
