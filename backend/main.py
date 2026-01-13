from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes.navigation import router as navigation_router
from routes.sos import router as sos_router
from routes.user import router as user_router

app = FastAPI(title="SHAKTI Safety Navigation API")

# CORS for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(navigation_router, prefix="/navigation", tags=["Navigation"])
app.include_router(sos_router, prefix="/sos", tags=["SOS & Emergency"])
app.include_router(user_router, prefix="/user", tags=["User Management"])

@app.get("/")
def root():
    return {
        "message": "🚀 SHAKTI Safety Navigation API",
        "version": "1.0",
        "endpoints": {
            "navigation": "/navigation/navigate",
            "sos": "/sos/sos",
            "user_profile": "/user/profile/{user_id}",
            "user_contacts": "/user/contacts/{user_id}"
        }
    }

@app.get("/health")
def health_check():
    return {"status": "healthy", "service": "shakti_backend"}