import os, json, numpy as np
from langchain_community.document_loaders import PyPDFLoader, TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from backend.core.config import settings
from backend.core.utils import get_embeddings

META_PATH = os.path.join(settings.VECTOR_STORE_DIR, "files.json")

def _load_metadata():
    if os.path.exists(META_PATH):
        with open(META_PATH, "r", encoding="utf-8") as f:
            return json.load(f)
    return {"files": []}

def _save_metadata(meta):
    os.makedirs(settings.VECTOR_STORE_DIR, exist_ok=True)
    with open(META_PATH, "w", encoding="utf-8") as f:
        json.dump(meta, f, indent=2)

def process_document(file_path: str, owner: str):
    file_name = os.path.basename(file_path)
    meta = _load_metadata()

    if any(f["original_filename"] == file_name and f["owner"] == owner for f in meta["files"]):
        return f"'{file_name}' already indexed for user '{owner}"

    loader = PyPDFLoader(file_path) if file_path.endswith(".pdf") else TextLoader(file_path, encoding="utf-8")
    docs = loader.load()
    splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=150)
    chunks = splitter.split_documents(docs)

    embeddings = get_embeddings()
    os.makedirs(settings.VECTOR_STORE_DIR, exist_ok=True)

    user_index_dir = os.path.join(settings.VECTOR_STORE_DIR, owner)
    os.makedirs(user_index_dir, exist_ok=True)

    if os.path.exists(os.path.join(user_index_dir, "index.faiss")):
        db = FAISS.load_local(user_index_dir, embeddings, allow_dangerous_deserialization=True)
        db.add_documents(chunks)
        db.save_local(user_index_dir)
    else:
        db = FAISS.from_documents(chunks, embeddings)
        db.save_local(user_index_dir)

    meta_entry = {
        "owner": owner,
        "original_filename": file_name,
        "stored_path": file_path,
    }
    meta["files"].append(meta_entry)
    _save_metadata(meta)

    return f"Indexed {len(chunks)} chunks from '{file_name}' for user '{owner}'."

def delete_document(file_name: str, owner: str):
    meta = _load_metadata()

    entry = next((f for f in meta["files"] if f["original_filename"] == file_name and f["owner"] == owner), None)
    if not entry:
        return f"'{file_name}' not found for user '{owner}'."

    stored_path = entry.get("stored_path")
    if stored_path and os.path.exists(stored_path):
        os.remove(stored_path)

    meta["files"] = [f for f in meta["files"] if f is not entry]
    _save_metadata(meta)

    user_files = [f for f in meta["files"] if f["owner"] == owner]
    user_index_dir = os.path.join(settings.VECTOR_STORE_DIR, owner)

    if os.path.exists(os.path.join(user_index_dir, "index.faiss")):
        os.remove(os.path.join(user_index_dir, "index.faiss"))

    if not user_files:
        return f"'{file_name}' deleted. No documents left for user '{owner}'."

    embeddings = get_embeddings()
    new_db = None
    splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=150)

    for remaining in user_files:
        path = remaining["stored_path"]
        if not os.path.exists(path):
            continue
        loader = PyPDFLoader(path) if path.endswith(".pdf") else TextLoader(path, encoding="utf-8")
        docs = loader.load()
        chunks = splitter.split_documents(docs)
        if new_db is None:
            new_db = FAISS.from_documents(chunks, embeddings)
        else:
            for c in chunks:
                emb = embeddings.embed_query(c.page_content)
                emb = np.array(emb).reshape(1, -1)
                new_db.index.add(emb)
                new_db.docstore.add({"text": c.page_content})

    if new_db:
        new_db.save_local(user_index_dir)
        return f"'{file_name}' removed{owner}'."
    else:
        return f"'{file_name}' deleted.{owner}'."
