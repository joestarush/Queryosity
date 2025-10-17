import React, { useState, useEffect, useRef } from "react";
import { api } from "../services/api";
import ReactMarkdown from "react-markdown";

export default function ChatPage({ token, onLogout }) {

  const [files, setFiles] = useState([]); 
  const [messages, setMessages] = useState([]); 
  const [input, setInput] = useState(""); 
  const [isLoading, setIsLoading] = useState(false); 

  const fileInputRef = useRef(null);

  useEffect(() => {
    const fetchFiles = async () => {
      try {
        const data = await api.getFiles(token);
        setFiles(data.files || []);
      } catch (error) {
        console.error("Failed to fetch files:", error);
      }
    };


    fetchFiles();
    
    setMessages([
      { text: "Welcome to Queryosity Ask me anything about your uploaded documents.", isUser: false },
    ]);
  }, [token]);

  const handleFileUpload = async (event) => {
    const file = event.target.files[0];
    if (!file) return;

    setIsLoading(true);
    try {
      await api.uploadFile(file, token);

      const data = await api.getFiles(token);
      setFiles(data.files || []);
    } catch (error) {
      console.error("File upload failed:", error);
    } finally {
      setIsLoading(false);
      fileInputRef.current.value = ""; 
    }
  };

 
  const handleDeleteFile = async (fileName) => {
    setIsLoading(true);
    try {
      await api.deleteFile(fileName, token);

      const data = await api.getFiles(token);
      setFiles(data.files || []);
    } catch (error) {
      console.error("Failed to delete file:", error);
    } finally {
      setIsLoading(false);
    }
  };

  const handleSendMessage = async (e) => {
    e.preventDefault();
    if (!input.trim() || isLoading) return;


    const userMessage = { text: input, isUser: true };
    setMessages((prev) => [...prev, userMessage]);
    setInput("");
    setIsLoading(true);

    try {

      const data = await api.postQuery(input, token);
      const botMessage = { text: data.answer, isUser: false };

      setMessages((prev) => [...prev, botMessage]);
    } catch {

      setMessages((prev) => [
        ...prev,
        { text: "⚠️ Sorry, I couldn’t get a response. Please try again.", isUser: false },
      ]);
    } finally {
      setIsLoading(false);
    }
  };

  const handleClearChat = async () => {
    try {
      await api.clearHistory(token);
      setMessages([{ text: "🧹 Chat history cleared. Ask something new!", isUser: false }]);
    } catch (error) {
      console.error("Failed to clear chat:", error);
    }
  };


  return (
    <div className="app-container">
      <header className="app-header">
        <h1>Queryosity</h1>
        <button onClick={onLogout} className="btn btn-logout">
          Logout
        </button>
      </header>

      <div className="main-content">
        <aside className="sidebar">
          <h2>Your Files</h2>
          <button
            onClick={() => fileInputRef.current.click()}
            className="btn btn-primary full-width"
            disabled={isLoading}
          >
            {isLoading ? "Processing..." : "Upload File"}
          </button>
          <input
            type="file"
            ref={fileInputRef}
            onChange={handleFileUpload}
            style={{ display: "none" }} 
            accept=".pdf,.txt"
          />

          <ul className="file-list">
            {files.length > 0 ? (
              files.map((file, i) => (
                <li key={i} className="file-item">
                  <span className="file-name">{file.original_filename || file}</span>
                  <button
                    onClick={() => handleDeleteFile(file.original_filename || file)}
                    className="btn-delete"
                    disabled={isLoading}
                  >
                    DELETE
                  </button>
                </li>
              ))
            ) : (
              <p className="no-files-text">No files uploaded yet.</p>
            )}
          </ul>
        </aside>

        <main className="chat-window">
          <div className="messages-container">
            {messages.map((msg, i) => (
              <div key={i} className={`message-wrapper ${msg.isUser ? "user" : "bot"}`}>
                <div className="message-bubble">
                  {msg.isUser ? msg.text : <ReactMarkdown>{msg.text}</ReactMarkdown>}
                </div>
              </div>
            ))}
          </div>

          <div className="chat-input-area">
            <form onSubmit={handleSendMessage} className="chat-form">
              <input
                type="text"
                value={input}
                onChange={(e) => setInput(e.target.value)}
                placeholder="Ask a question..."
                className="chat-input"
                disabled={isLoading}
              />
              <button
                type="submit"
                className="btn btn-send"
                disabled={!input.trim() || isLoading}
              >
                {isLoading ? "..." : "Send"}
              </button>
              <button
                type="button"
                onClick={handleClearChat}
                className="btn btn-clear"
                disabled={isLoading}
              >
                Clear
              </button>
            </form>
          </div>
        </main>
      </div>
    </div>
  );
}
