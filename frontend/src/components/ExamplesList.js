import React, { useState } from "react";
import "./ExamplesList.css";

function ExamplesList({ examples, onExampleClick }) {
  const [showExamples, setShowExamples] = useState(false);

  if (!examples || examples.length === 0) return null;

  return (
    <div className="examples-section">
      <button
        className="examples-toggle"
        onClick={() => setShowExamples(!showExamples)}
      >
        {showExamples ? "🔼 Hide Examples" : "🔽 Show Example Transformations"}
      </button>

      {showExamples && (
        <div className="examples-grid">
          {examples.map((example, index) => (
            <div
              key={index}
              className="example-card"
              onClick={() => onExampleClick(example)}
            >
              <div className="example-category">{example.category}</div>
              <div className="example-original">
                <strong>Original:</strong> {example.original}
              </div>
              <div className="example-arrow">↓</div>
              <div className="example-rephrased">
                <strong>Rephrased:</strong> {example.rephrased}
              </div>
              <div className="example-action">Click to try →</div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}

export default ExamplesList;
