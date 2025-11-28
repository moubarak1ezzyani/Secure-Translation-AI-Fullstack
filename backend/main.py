import os
import httpx
from datetime import datetime, timedelta, timezone
from typing import Optional
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from passlib.context import CryptContext
from jose import JWTError, jwt
from dotenv import load_dotenv

# --- CONFIG ---
# url_db = postgresql://user:password@host:port/database
load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL")
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
HF_TOKEN = os.getenv("HF_API_TOKEN")

# --- DB SETUP ---
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    hashed_password = Column(String)

Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try: yield db
    finally: db.close()

# --- SECURITY ---
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=30)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

async def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None: raise HTTPException(status_code=401)
    except JWTError: raise HTTPException(status_code=401)
    user = db.query(User).filter(User.username == username).first()
    if user is None: raise HTTPException(status_code=401)
    return user

# --- APP ---
app = FastAPI()
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])

# --- MODELS Pydantic ---
class UserAuth(BaseModel):
    username: str
    password: str

class TranslationRequest(BaseModel):
    text: str
    direction: str      # fr -> en / en -> fr

# --- ROUTES ---
@app.post("/register")
def register(user: UserAuth, db: Session = Depends(get_db)):
    if db.query(User).filter(User.username == user.username).first():
        raise HTTPException(status_code=400, detail="Username already registered")
    hashed_pw = pwd_context.hash(user.password)
    db_user = User(username=user.username, hashed_password=hashed_pw)
    db.add(db_user)
    db.commit()
    return {"message": "User created"}

@app.post("/login")
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(User).filter(User.username == form_data.username).first()
    if not user or not pwd_context.verify(form_data.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Incorrect credentials")
    token = create_access_token(data={"sub": user.username})
    return {"access_token": token, "token_type": "bearer"}

@app.post("/translate")
async def translate(req: TranslationRequest, current_user: User = Depends(get_current_user)):
    model = "Helsinki-NLP/opus-mt-fr-en" if req.direction == "fr-en" else "Helsinki-NLP/opus-mt-en-fr"
    # model = "Helsinki-NLP/opus-mt-fr-en"
    # api_url = f"https://api-inference.huggingface.co/models/{model}"
    # api_url = f"https://router.huggingface.co/hf-inference/models/Helsinki-NLP/opus-mt-en-fr"
    api_url = f"https://router.huggingface.co/hf-inference/models/{model}"  
    headers = {"Authorization": f"Bearer {HF_TOKEN}"}
    # print("token affiche",HF_TOKEN)
    
    async with httpx.AsyncClient() as client:
        response = await client.post(api_url, headers=headers, json={"inputs": req.text})
    print("status code :", response.status_code)
    print("Response Body",response.text)
    if response.status_code == 503:
        raise HTTPException(status_code=503, detail="Model loading, please wait")
    if response.status_code != 200:
        raise HTTPException(status_code=500, detail="Error from HF API")
        
    return {"translation": response.json()[0]['translation_text']}