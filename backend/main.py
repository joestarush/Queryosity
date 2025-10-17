from fastapi import FastAPI, UploadFile, Form, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from backend.services.auth_service import get_current_user, register_user, login_user
from backend.services.ingest_service import process_document, delete_document, META_PATH
from backend.services.query_service import answer_query, clear_user_memory
from backend.core.config import settings
import os, shutil, json

app = FastAPI(title="Knowledge-Base Search Engine")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

os.makedirs(settings.UPLOAD_DIR, exist_ok=True)

@app.post("/register")
def register(username: str = Form(...), password: str = Form(...)):
    return register_user(username, password)

@app.post("/login")
def login(username: str = Form(...), password: str = Form(...)):
    return login_user(username, password)


@app.post("/upload")
async def upload_file(file: UploadFile, current_user: dict = Depends(get_current_user)):
    username = current_user["username"]
    user_dir = os.path.join(settings.UPLOAD_DIR, username)
    os.makedirs(user_dir, exist_ok=True)

    filename = os.path.basename(file.filename)
    file_path = os.path.join(user_dir, filename)

    if os.path.exists(file_path):
        raise HTTPException(status_code=400, detail="File already exists")

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    msg = process_document(file_path, owner=username)
    return {"success": True, "detail": msg}


@app.post("/chat")
async def chat(question: str = Form(...), user_id: str = Form(...), current_user: dict = Depends(get_current_user)):
    username = current_user["username"]
    print(answer_query(question, user_id, owner=username))
    return answer_query(question, user_id, owner=username)


@app.get("/files")
async def list_files(current_user: dict = Depends(get_current_user)):
    username = current_user["username"]
    if os.path.exists(META_PATH):
        with open(META_PATH, "r", encoding="utf-8") as f:
            data = json.load(f)
        user_files = [f for f in data.get("files", []) if f.get("owner") == username]
        return {"files": user_files}
    return {"files": []}


@app.post("/delete")
async def delete_file(file_name: str = Form(...), current_user: dict = Depends(get_current_user)):
    username = current_user["username"]
    result = delete_document(file_name, owner=username)
    return {"result": result}


@app.post("/clear")
async def clear_user(user_id: str = Form(...), current_user: dict = Depends(get_current_user)):
    username = current_user["username"]
    result = clear_user_memory(user_id, owner=username)
    return {"result": result}
