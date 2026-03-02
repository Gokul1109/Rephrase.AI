import React from "react";
import "./SuggestionDisplay.css";

function SuggestionDisplay({ suggestion, loading }) {
  if (loading) {
    return (
      <div className="suggestion-container loading">
        <div className="loading-spinner"></div>
        <p>Analyzing your message with AI agents...</p>
      </div>
    );
  }

  if (!suggestion) return null;

  if (!suggestion.success) {
    return (
      <div className="suggestion-container error">
        <h3>❌ Error</h3>
        <p>{suggestion.error}</p>
      </div>
    );
  }

  return (
    <div className="suggestion-container">
      <div className="suggestion-header">
        <h3>✨ AI Suggestion</h3>
      </div>

      <div className="message-comparison">
        <div className="message-box original">
          <h4>Original</h4>
          <p>{suggestion.original}</p>
        </div>
        <div className="arrow">→</div>
        <div className="message-box rephrased">
          <h4>Rephrased</h4>
          <p>{suggestion.rephrased}</p>
        </div>
      </div>

      {suggestion.analysis && (
        <div className="analysis-section">
          <h4>📊 Analysis</h4>
          <div className="analysis-grid">
            {suggestion.analysis.intent && (
              <div className="analysis-item">
                <span className="label">Intent:</span>
                <span className="value">
                  {suggestion.analysis.intent.detected_intent || "N/A"}
                </span>
              </div>
            )}
            {suggestion.analysis.tone_improvement && (
              <div className="analysis-item">
                <span className="label">Tone:</span>
                <span className="value">
                  {suggestion.analysis.tone_improvement}
                </span>
              </div>
            )}
            {suggestion.analysis.clarity_score !== undefined && (
              <div className="analysis-item">
                <span className="label">Clarity Score:</span>
                <span className="value">
                  {suggestion.analysis.clarity_score}/10
                </span>
              </div>
            )}
          </div>
        </div>
      )}

      {suggestion.suggestions && (
        <div className="context-suggestions">
          {suggestion.suggestions.jira &&
            suggestion.suggestions.jira !== suggestion.original && (
              <div className="context-item">
                <span className="context-icon">📋</span>
                <span>Jira context applied</span>
              </div>
            )}
          {suggestion.suggestions.calendar &&
            suggestion.suggestions.calendar !== suggestion.original && (
              <div className="context-item">
                <span className="context-icon">📅</span>
                <span>Calendar context applied</span>
              </div>
            )}
        </div>
      )}

      <button
        className="copy-button"
        onClick={() => navigator.clipboard.writeText(suggestion.rephrased)}
      >
        📋 Copy Rephrased Message
      </button>
    </div>
  );
}

export default SuggestionDisplay;
