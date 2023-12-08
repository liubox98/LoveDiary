from fastapi.middleware.cors import CORSMiddleware
from motor.motor_asyncio import AsyncIOMotorClient
from fastapi import FastAPI, HTTPException, Depends, Request
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from urllib.parse import quote_plus
from pydantic import BaseModel
from typing import List
from datetime import datetime, timedelta
import secrets

app = FastAPI()

# 配置CORS中间件，允许跨域请求
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# MongoDB 配置
username = "liubox98"
password = "abc123!@"
cluster_url = "cluster0.h41guuq.mongodb.net"
database_name = "hamburger"

uri = f"mongodb+srv://{quote_plus(username)}:{quote_plus(password)}@{cluster_url}/{database_name}?retryWrites=true&w=majority"

# MongoDB连接
client = AsyncIOMotorClient(uri)
db = client[database_name]
user_collection = db['user']
action_collection = db['activities']


# 用于签名令牌的密钥
SECRET_KEY = secrets.token_urlsafe(32)
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

class User(BaseModel):
    username: str
    password: str

class Action(BaseModel):
    action: str
    description:str

async def get_user(username: str):
    return await user_collection.find_one({"username": username})

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

async def create_jwt_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

async def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=401,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    user = await get_user(username)
    if user is None:
        raise credentials_exception
    return user

@app.post("/token")
async def login_for_access_token(request: Request):
    data = await request.json()
    username = data.get("username")
    password = data.get("password")

    user = await user_collection.find_one({"username": username, "password": password})
    if user:
        access_token = await create_jwt_token({"sub": username})
        return {"access_token": access_token, "token_type": "bearer"}
    raise HTTPException(status_code=401, detail="Unauthorized")

@app.get("/users/me", response_model=User)
async def read_users_me(current_user: User = Depends(get_current_user)):
    return current_user


@app.post("/activities/", status_code=201)
async def create_activity(activity: Action):
    await action_collection.insert_one(
        {"action": activity.action, "description": activity.description}
    )

@app.get("/activities/", response_model=List[Action])
async def read_activities():
    activities = await action_collection.find({}).to_list(None)
    return activities


