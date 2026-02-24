import axios from "axios";

const API_BASE_URL =
  process.env.REACT_APP_API_URL || "http://localhost:8000/api";

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    "Content-Type": "application/json",
  },
});

/**
 * Rephrase a message using AI agents
 */
export const rephraseMessage = async (message, context = {}) => {
  try {
    const response = await api.post("/rephrase", {
      message,
      user_id: "default_user",
      context: {
        chat_history: context.chat_history || [],
        include_jira: context.include_jira !== false,
        include_calendar: context.include_calendar !== false,
      },
    });
    return response.data;
  } catch (error) {
    console.error("Error rephrasing message:", error);
    throw error;
  }
};

/**
 * Analyze message without rephrasing
 */
export const analyzeMessage = async (message, chatHistory = []) => {
  try {
    const response = await api.post("/analyze", {
      message,
      chat_history: chatHistory,
    });
    return response.data;
  } catch (error) {
    console.error("Error analyzing message:", error);
    throw error;
  }
};

/**
 * Get current context (Jira + Calendar)
 */
export const getContext = async (userId = "default_user") => {
  try {
    const response = await api.get("/context", {
      params: { user_id: userId },
    });
    return response.data;
  } catch (error) {
    console.error("Error fetching context:", error);
    throw error;
  }
};

/**
 * Get example transformations
 */
export const getExamples = async () => {
  try {
    const response = await api.get("/examples");
    return response.data;
  } catch (error) {
    console.error("Error fetching examples:", error);
    throw error;
  }
};

/**
 * Health check
 */
export const healthCheck = async () => {
  try {
    const response = await api.get("/health");
    return response.data;
  } catch (error) {
    console.error("Error checking health:", error);
    throw error;
  }
};

/**
 * Save a message to chat history
 */
export const saveMessage = async (sender, message) => {
  try {
    const response = await api.post("/save_message", {
      sender,
      message,
    });
    return response.data;
  } catch (error) {
    console.error("Error saving message:", error);
    throw error;
  }
};

export default api;
