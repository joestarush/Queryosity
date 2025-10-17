# Queryosity 🔮

## [![Queryosity Demo Video]](https://www.youtube.com/watch?v=lpMS8QK6TJM)

Queryosity is a full-stack "Chat with your Documents" application. It allows users to upload their own PDF and text files, which are then processed and indexed into a vector store. Users can then ask questions in a conversational interface to get answers based on the content of their documents.

This project demonstrates a complete Retrieval-Augmented Generation (RAG) pipeline, featuring a Python backend powered by FastAPI and LangChain, and a responsive frontend built with React.

![!\[Queryosity Screenshot\](https://github.com/joestarush/Queryosity.git/Sample.png)](Sample.png)

## ✨ MVP Features

The current version of the application includes the following core features:

* **👤 User Authentication:** Secure user registration and login system using JWT (JSON Web Tokens). Each user has their own private document space.
* **📄 Document Upload:** Users can upload `.pdf` and `.txt` files. The backend processes these documents, splits them into manageable chunks, and creates vector embeddings.
* **🗂️ Per-User Vector Stores:** Each user's documents are stored in a separate FAISS vector index, ensuring that a user's queries only search against their own data.
* **🗑️ File Management:** Users can view a list of their uploaded documents and delete them. Deleting a file correctly removes it and rebuilds the user's search index.
* **💬 Conversational Chat Interface:** A familiar chat window where users can ask questions. The application maintains conversation history to allow for follow-up questions.
* **🧠 RAG-Powered Responses:** The backend uses a Conversational Retrieval Chain (powered by LangChain and an LLM like Gemini) to find relevant document chunks and generate accurate answers.
* **🔄 Clear Chat History:** Users can clear their current conversation memory to start fresh.

## 🛠️ Technology Stack

This project is built with a modern, modular technology stack:

* **Backend:**
    * **Framework:** FastAPI
    * **LLM Orchestration:** LangChain
    * **Vector Database:** FAISS (local storage)
    * **Authentication:** `python-jose` for JWT, `passlib` for hashing
    * **LLM & Embeddings:** Configured for Gemini or other major providers.
* **Frontend:**
    * **Library:** React
    * **Styling:** Plain CSS (`index.css`)
    * **API Communication:** `fetch` API

## 🚀 Getting Started

To run this project locally, you will need to set up the backend and the frontend separately.

### **1. Backend Setup (FastAPI)**

First, navigate to the `backend` directory.

```
cd backend
```

**a. Create a Virtual Environment (Recommended)**

```
python -m venv venv
source venv/bin/activate  # On macOS/Linux
# venv\Scripts\activate    # On Windows
```

**b. Install Dependencies**

```
pip install -r requirements.txt
```

**c. Set Up Environment Variables**
Create a `.env` file in the `backend` directory and add your API keys (e.g., for your LLM provider).

```
# .env file
# Example for Google Gemini
GEMINI_API_KEY="YOUR_API_KEY_HERE"
```

**d. Run the Backend Server**

```
cd ..# To root folder
uvicorn backend.main:app --reload
```

The backend will be running at `http://127.0.0.1:8000`.

### **2. Frontend Setup (React)**

In a new terminal, navigate to the `frontend` directory.

```
cd frontend
```

**a. Create `package.json` (If Missing)**
If you don't have a `package.json` file, create one and paste the contents provided in our previous conversations.

**b. Install Dependencies**
This command reads `package.json` and installs React and all other necessary libraries.

```
npm install
```

**c. Run the Frontend App**

```
npm start
```

The frontend will open in your browser at `http://localhost:3000`.

## usages

1.  **Register:** Create a new account from the login screen.
2.  **Login:** Sign in with your credentials.
3.  **Upload Files:** Use the "Upload File" button to add your `.pdf` or `.txt` documents.
4.  **Ask Questions:** Type your questions into the chat box and get answers sourced from your documents!
