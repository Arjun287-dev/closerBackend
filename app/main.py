from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.api.v1 import auth, couple, chat

app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url=f"{settings.API_V1_STR}/openapi.json"
)

# Set up CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8081", "http://127.0.0.1:8081", "exp://localhost:8081"],  # Allowed origins

    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

# Include routers
app.include_router(auth.router, prefix=f"{settings.API_V1_STR}/auth", tags=["auth"])
app.include_router(couple.router, prefix=f"{settings.API_V1_STR}/couple", tags=["couple"])
app.include_router(chat.router, prefix=f"{settings.API_V1_STR}", tags=["chat"])

@app.get("/")
def root():
    return {"message": "Welcome to Closer API"}
