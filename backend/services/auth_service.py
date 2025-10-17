from fastapi import Depends, HTTPException, status, Form
from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext
from jose import JWTError,jwt
from datetime import datetime, timedelta
from typing import Dict

users_db: Dict[str, dict] = {}  # username -> user dict


SECRET_KEY = "22BCE8345" 
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60

pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto"
)
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

def get_password_hash(password: str):
    pw_bytes = password.encode("utf-8")[:72]
    return pwd_context.hash(pw_bytes)

def verify_password(plain_password: str, hashed_password: str):
    pw_bytes = plain_password.encode("utf-8")[:72]
    return pwd_context.verify(pw_bytes, hashed_password)

def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None or username not in users_db:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    return users_db[username]

def register_user(username: str = Form(...), password: str = Form(...)):
    if username in users_db:
        raise HTTPException(status_code=400, detail="Username already exists")
    hashed_password = get_password_hash(password)
    users_db[username] = {
        "username": username,
        "hashed_password": hashed_password
    }
    return {"msg": "User registered successfully"}

def login_user(username: str = Form(...), password: str = Form(...)):
    user = users_db.get(username)
    if not user or not verify_password(password, user["hashed_password"]):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    token = create_access_token({"sub": username})
    return {"access_token": token, "token_type": "bearer"}
