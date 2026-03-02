import React from "react";
import "./ContextPanel.css";

function ContextPanel({ context }) {
  if (!context) return null;

  const { jira_context, calendar_context } = context;

  return (
    <div className="context-panel">
      <h3>📋 Current Context</h3>
      <p className="context-description">
        This is the context our AI agents use to enhance your messages
      </p>

      <div className="context-grid">
        {/* Jira Context */}
        {jira_context && jira_context.active_tasks && (
          <div className="context-section">
            <h4>📋 Active Jira Tasks ({jira_context.active_tasks.length})</h4>
            <div className="tasks-list">
              {jira_context.active_tasks.slice(0, 3).map((task, index) => (
                <div key={index} className="task-item">
                  <div className="task-header">
                    <span className="task-key">{task.key}</span>
                    <span
                      className={`task-priority priority-${task.priority.toLowerCase()}`}
                    >
                      {task.priority}
                    </span>
                  </div>
                  <div className="task-summary">{task.summary}</div>
                  <div className="task-meta">
                    <span>📅 Due: {task.due_date}</span>
                    <span>📊 {task.status}</span>
                  </div>
                </div>
              ))}
            </div>
          </div>
        )}

        {/* Calendar Context */}
        {calendar_context && calendar_context.events && (
          <div className="context-section">
            <h4>
              📅 Today's Calendar ({calendar_context.events.length} events)
            </h4>
            <div className="events-list">
              {calendar_context.events.slice(0, 4).map((event, index) => (
                <div key={index} className="event-item">
                  <div className="event-time">
                    {event.start_time} - {event.end_time}
                  </div>
                  <div className="event-title">{event.title}</div>
                  <div className={`event-status status-${event.status}`}>
                    {event.status}
                  </div>
                </div>
              ))}
              {calendar_context.next_free_slot && (
                <div className="next-free">
                  ⏰ Next free: {calendar_context.next_free_slot}
                </div>
              )}
            </div>
          </div>
        )}
      </div>
    </div>
  );
}

export default ContextPanel;
