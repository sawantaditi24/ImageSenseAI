import React from 'react';

interface Screenshot {
  id: number;
  category: string;
  imageUrl: string;
  filename?: string;
  upload_time?: string;
}

interface ScreenshotResultProps {
  screenshot: Screenshot;
}

const ScreenshotResult: React.FC<ScreenshotResultProps> = ({ screenshot }) => {
  return (
    <div className="screenshot-result">
      <div><strong>Category:</strong> {screenshot.category}</div>
      {screenshot.filename && (
        <div className="screenshot-meta">{screenshot.filename}</div>
      )}
      {screenshot.upload_time && (
        <div className="screenshot-meta">
          Uploaded: {new Date(screenshot.upload_time).toLocaleDateString()}
        </div>
      )}
      {screenshot.imageUrl && (
        <div style={{ marginTop: 8 }}>
          <img
            src={screenshot.imageUrl}
            alt="Screenshot"
            style={{ maxWidth: 240, borderRadius: 8, boxShadow: '0 2px 8px rgba(0,0,0,0.1)' }}
          />
          <div>
            <a
              href={screenshot.imageUrl}
              className="screenshot-view-link"
              target="_blank"
              rel="noopener noreferrer"
            >
              View Full Image
            </a>
          </div>
        </div>
      )}
    </div>
  );
};

export default ScreenshotResult; 