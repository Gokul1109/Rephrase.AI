import React, { useState, useRef, useEffect } from "react";
import "./ChatInterface.css";
import { rephraseMessage, saveMessage } from "../services/api";

const ChatInterface = () => {
  const [messages, setMessages] = useState([]);
  const [currentUser, setCurrentUser] = useState("john");
  const [inputText, setInputText] = useState("");
  const [suggestions, setSuggestions] = useState([]);
  const [isLoading, setIsLoading] = useState(false);
  const chatEndRef = useRef(null);
  const typingTimeoutRef = useRef(null);

  const users = {
    john: { name: "John Doe", color: "#4A90E2", avatar: "👨‍💼" },
    sarah: { name: "Sarah Smith", color: "#E24A90", avatar: "👩‍💼" },
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const scrollToBottom = () => {
    chatEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  const handleInputChange = async (e) => {
    const text = e.target.value;
    setInputText(text);

    // Clear previous timeout
    if (typingTimeoutRef.current) {
      clearTimeout(typingTimeoutRef.current);
    }

    // Only get suggestions if text is meaningful (more than 2 characters)
    if (text.trim().length > 2) {
      typingTimeoutRef.current = setTimeout(async () => {
        await fetchSuggestions(text);
      }, 200); // Wait 200ms after user stops typing
    } else {
      setSuggestions([]);
    }
  };

  const fetchSuggestions = async (text) => {
    setIsLoading(true);
    try {
      const response = await rephraseMessage(text, {
        chat_history: messages.map((msg) => ({
          role: msg.sender === currentUser ? "user" : "assistant",
          content: msg.text,
        })),
        include_jira: true,
        include_calendar: true,
      });

      if (response.success && response.rephrased) {
        setSuggestions([
          {
            text: response.rephrased,
            type: "ai",
            analysis: response.analysis,
          },
        ]);
      }
    } catch (error) {
      console.error("Error fetching suggestions:", error);
      setSuggestions([]);
    } finally {
      setIsLoading(false);
    }
  };

  const handleSendMessage = async () => {
    if (inputText.trim()) {
      const newMessage = {
        id: Date.now(),
        sender: currentUser,
        text: inputText,
        timestamp: new Date().toLocaleTimeString([], {
          hour: "2-digit",
          minute: "2-digit",
        }),
      };
      setMessages([...messages, newMessage]);
      
      // Save message to backend
      try {
        await saveMessage(users[currentUser].name, inputText);
      } catch (error) {
        console.error("Failed to save message:", error);
      }
      
      setInputText("");
      setSuggestions([]);
      
      // Clear any pending suggestion requests
      if (typingTimeoutRef.current) {
        clearTimeout(typingTimeoutRef.current);
      }
    }
  };

  const handleUseSuggestion = (suggestedText) => {
    const cleanText = suggestedText.replace(/\s\(\d+\.\d+\)$/, '');
    setInputText(cleanText);
    setSuggestions([]);
  };

  const handleKeyPress = (e) => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      handleSendMessage();
    }
  };

  const switchUser = () => {
    setCurrentUser(currentUser === "john" ? "sarah" : "john");
    setInputText("");
    setSuggestions([]);
  };

  const clearChat = () => {
    setMessages([]);
    setInputText("");
    setSuggestions([]);
  };

  return (
    <div className="chat-interface">
      <div className="chat-header">
        <div className="header-left">
          <h2>💬 Workplace Chat - AI Powered</h2>
          <p className="header-subtitle">
            Real-time AI suggestions as you type
          </p>
        </div>
        <div className="header-right">
          <button onClick={clearChat} className="clear-btn">
            🗑️ Clear Chat
          </button>
        </div>
      </div>

      <div className="chat-container">
        <div className="chat-messages">
          {messages.length === 0 ? (
            <div className="empty-chat">
              <div className="welcome-message">
                <h3>👋 Welcome to AI-Powered Chat!</h3>
                <p>Start typing to get intelligent message suggestions</p>
                <div className="demo-hints">
                  <h4>Try asking about:</h4>
                  <ul>
                    <li>📋 Project updates (PROJ-102 memory leak)</li>
                    <li>📅 Meeting availability</li>
                    <li>🔄 Task status inquiries</li>
                  </ul>
                </div>
              </div>
            </div>
          ) : (
            messages.map((msg) => (
              <div
                key={msg.id}
                className={`message ${
                  msg.sender === currentUser ? "sent" : "received"
                }`}
              >
                <div className="message-avatar">{users[msg.sender].avatar}</div>
                <div className="message-content">
                  <div className="message-header">
                    <span className="message-sender">
                      {users[msg.sender].name}
                    </span>
                    <span className="message-time">{msg.timestamp}</span>
                  </div>
                  <div className="message-text">{msg.text}</div>
                </div>
              </div>
            ))
          )}
          <div ref={chatEndRef} />
        </div>

        <div className="chat-input-section">
          {/* AI Suggestions */}
          {suggestions.length > 0 && (
            <div className="suggestions-panel">
              <div className="suggestions-header">
                <span className="ai-badge">✨ AI Suggestion</span>
                {isLoading && (
                  <span className="loading-indicator">Thinking...</span>
                )}
              </div>
              {suggestions.map((suggestion, index) => (
                <div
                  key={index}
                  className="suggestion-item"
                  onClick={() => handleUseSuggestion(suggestion.text)}
                >
                  <div className="suggestion-text">{suggestion.text}</div>
                  <button className="use-suggestion-btn">Use This →</button>
                </div>
              ))}
            </div>
          )}

          {/* User Switcher */}
          <div className="user-switcher">
            <span className="current-user-label">Chatting as:</span>
            <button
              className="user-toggle"
              onClick={switchUser}
              style={{ backgroundColor: users[currentUser].color }}
            >
              {users[currentUser].avatar} {users[currentUser].name}
            </button>
            <span className="switch-hint">Click to switch user</span>
          </div>

          {/* Input Area */}
          <div className="input-container">
            <textarea
              className="chat-input"
              placeholder={`Type a message as ${users[currentUser].name}...`}
              value={inputText}
              onChange={handleInputChange}
              onKeyPress={handleKeyPress}
              rows="2"
            />
            <button
              className="send-btn"
              onClick={handleSendMessage}
              disabled={!inputText.trim()}
            >
              Send 📨
            </button>
          </div>
        </div>
      </div>
    </div>
  );
};

export default ChatInterface;
