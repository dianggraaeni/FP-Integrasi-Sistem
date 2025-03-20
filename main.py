from database import db
from fastapi import FastAPI
from routers import users, email

app = FastAPI()

# Tambahkan root endpoint
@app.get("/")
def read_root():
    return {"message": "Welcome to my FastAPI app!"}

# Include routers
app.include_router(users.router)
app.include_router(email.router)
