from fastapi import FastAPI
from app.api import auth, users

app = FastAPI(title="VoIP App MVP")

# Register routes
app.include_router(auth.router, prefix="/auth", tags=["Auth"])
app.include_router(users.router, prefix="/users", tags=["Users"])

@app.get("/")
def root():
    return {"message": "VoIP MVP is running 🚀"}
