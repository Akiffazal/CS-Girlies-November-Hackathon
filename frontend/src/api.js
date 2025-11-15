// src/api.js
import axios from "axios";

const API_URL = process.env.REACT_APP_API_URL;

export const uploadPDF = async (file) => {
  const formData = new FormData();
  formData.append("file", file);

  const res = await axios.post(`${API_URL}/upload`, formData, {
    headers: { "Content-Type": "multipart/form-data" },
  });

  return res.data;
};

export const askQuestion = async (question) => {
  const res = await axios.post(`${API_URL}/ask?question=${encodeURIComponent(question)}`);
  return res.data;
};
