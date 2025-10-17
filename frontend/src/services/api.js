
const API_BASE_URL = 'http://127.0.0.1:8000'; 

export const api = {
  register: async (username, password) => {
    const formData = new FormData();
    formData.append('username', username);
    formData.append('password', password);
    const response = await fetch(`${API_BASE_URL}/register`, {
      method: 'POST',
      body: formData,
    });
    return response.json();
  },

  login: async (username, password) => {
    const formData = new FormData();
    formData.append('username', username);
    formData.append('password', password);
    const response = await fetch(`${API_BASE_URL}/login`, {
      method: 'POST',
      body: formData,
    });
    if (!response.ok) {
        throw new Error('Login failed');
    }
    return response.json();
  },

  getFiles: async (token) => {
    const response = await fetch(`${API_BASE_URL}/files`, {
      headers: { 'Authorization': `Bearer ${token}` },
    });
    return response.json();
  },

  uploadFile: async (file, token) => {
    const formData = new FormData();
    formData.append('file', file);
    const response = await fetch(`${API_BASE_URL}/upload`, {
      method: 'POST',
      headers: { 'Authorization': `Bearer ${token}` },
      body: formData,
    });
    return response.json();
  },

  deleteFile: async (fileName, token) => {
    const formData = new FormData();
    formData.append('file_name', fileName);
    const response = await fetch(`${API_BASE_URL}/delete`, {
      method: 'POST',
      headers: { 'Authorization': `Bearer ${token}` },
      body: formData,
    });
    return response.json();
  },

  postQuery: async (question, token) => {
    const formData = new FormData();
    formData.append('question', question);
    formData.append('user_id', 'dummy_user_id'); 
    const response = await fetch(`${API_BASE_URL}/chat`, {
      method: 'POST',
      headers: { 'Authorization': `Bearer ${token}` },
      body: formData,
    });
    return response.json();
  },

  clearHistory: async (token) => {
    const formData = new FormData();
    formData.append('user_id', 'dummy_user_id');
    const response = await fetch(`${API_BASE_URL}/clear`, {
      method: 'POST',
      headers: { 'Authorization': `Bearer ${token}` },
      body: formData,
    });
    return response.json();
  },
};
