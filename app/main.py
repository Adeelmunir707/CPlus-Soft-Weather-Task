from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from passlib.context import CryptContext
import jwt
import json
import os
from datetime import datetime, timedelta

from . import models, schemas, weather
from .database import Base, engine, get_db

# Create DB tables
Base.metadata.create_all(bind=engine)

# Load JWT config
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
with open(os.path.join(BASE_DIR, "config.json")) as f:
    jwt_config = json.load(f)["jwt"]

SECRET_KEY = jwt_config["secret_key"]
ALGORITHM = jwt_config["algorithm"]
ACCESS_TOKEN_EXPIRE_MINUTES = jwt_config["access_token_expires_minutes"]

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

app = FastAPI(title="Weather API Project")

def hash_password(password: str):
    return pwd_context.hash(password)

def verify_password(plain, hashed):
    return pwd_context.verify(plain, hashed)

def create_access_token(data: dict):
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    data.update({"exp": expire})
    return jwt.encode(data, SECRET_KEY, algorithm=ALGORITHM)

@app.post("/signup")
def signup(user: schemas.UserCreate, db: Session = Depends(get_db)):
    if db.query(models.User).filter(models.User.username == user.username).first():
        raise HTTPException(status_code=400, detail="Username already exists")
    new_user = models.User(username=user.username, password=hash_password(user.password))
    db.add(new_user)
    db.commit()
    return {"message": "User created successfully"}

@app.post("/login", response_model=schemas.Token)
def login(user: schemas.UserLogin, db: Session = Depends(get_db)):
    db_user = db.query(models.User).filter(models.User.username == user.username).first()
    if not db_user or not verify_password(user.password, db_user.password):
        raise HTTPException(status_code=400, detail="Invalid username or password")
    token = create_access_token({"sub": db_user.username})
    return {"access_token": token}

@app.get("/weather")
def get_weather():
    return weather.get_weather_forecast()
