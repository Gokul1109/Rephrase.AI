import React from "react";
import "./MessageInput.css";

function MessageInput({ value, onChange, onRephrase, loading }) {
  const handleSubmit = (e) => {
    e.preventDefault();
    onRephrase(value);
  };

  return (
    <div className="message-input-container">
      <form onSubmit={handleSubmit}>
        <div className="input-wrapper">
          <textarea
            className="message-textarea"
            placeholder="Type your message here... (e.g., 'Update?', 'Need this today', 'Can we talk now?')"
            value={value}
            onChange={(e) => onChange(e.target.value)}
            rows="4"
            disabled={loading}
          />
        </div>
        <button
          type="submit"
          className="rephrase-button"
          disabled={loading || !value.trim()}
        >
          {loading ? "✨ Analyzing..." : "✨ Rephrase with AI"}
        </button>
      </form>
    </div>
  );
}

export default MessageInput;
