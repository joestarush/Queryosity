import os
from collections import defaultdict
from dotenv import load_dotenv
from langchain.chains import ConversationalRetrievalChain
from langchain.memory import ConversationBufferMemory
from langchain_community.vectorstores import FAISS
from backend.core.config import settings
from backend.core.utils import get_embeddings, get_llm

load_dotenv()

user_memories = defaultdict(
    lambda: ConversationBufferMemory(
        memory_key="chat_history",
        return_messages=True,
        output_key="answer"
    )
)

def answer_query(question: str, user_id: str, owner: str):

    user_index_dir = os.path.join(settings.VECTOR_STORE_DIR, owner)
    index_path = os.path.join(user_index_dir, "index.faiss")

    if not os.path.exists(index_path):
        return {"answer": "No documents indexed"}

    embeddings = get_embeddings()
    db = FAISS.load_local(user_index_dir, embeddings, allow_dangerous_deserialization=True)
    retriever = db.as_retriever(search_kwargs={"k": 4})
    llm = get_llm()

    memory = user_memories[owner]

    chain = ConversationalRetrievalChain.from_llm(
        llm=llm,
        retriever=retriever,
        memory=memory,
        return_source_documents=False
    )

    result = chain.invoke({"question": question})
    return {"answer": result["answer"]}


def clear_user_memory(user_id: str, owner: str):
    if owner in user_memories:
        del user_memories[owner]
        return f"Chat history cleared : {owner}"
    return f"No memory: {owner}"
