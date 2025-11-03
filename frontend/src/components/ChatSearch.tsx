import React, { useState } from 'react';
import ScreenshotResult from './ScreenshotResult';
import './ChatSearch.css';
import { FiSend } from 'react-icons/fi';
import api from '../services/api';

interface Screenshot {
  id: number;
  category: string;
  imageUrl: string;
  filename?: string;
  upload_time?: string;
}

interface SearchResponse {
  results: Screenshot[];
}

interface UserMessage {
  type: 'user';
  content: string;
}
interface ResultMessage {
  type: 'result';
  content: Screenshot[];
}
type ChatMessage = UserMessage | ResultMessage;

const ChatSearch: React.FC = () => {
  const [messages, setMessages] = useState<ChatMessage[]>([]);
  const [input, setInput] = useState('');
  const [loading, setLoading] = useState(false);

  const handleInputChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setInput(e.target.value);
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!input.trim()) return;
    const userMessage: UserMessage = { type: 'user', content: input };
    setMessages((prev) => [...prev, userMessage]);
    setLoading(true);
    try {
      const response = await api.post<SearchResponse>('/api/v1/search', { query: input });
      const data = response.data;
      // Defensive: ensure results is always an array
      const results = Array.isArray(data?.results) ? data.results : [];
      const resultMessage: ResultMessage = { type: 'result', content: results };
      setMessages((prev) => [...prev, resultMessage]);
    } catch (error) {
      console.error('Search error:', error);
      setMessages((prev) => [...prev, { type: 'result', content: [] }]);
    } finally {
      setLoading(false);
      setInput('');
    }
  };

  return (
    <div className="chat-search-container">
      <div className="chat-messages">
        {messages.map((msg, idx) => {
          if (msg.type === 'user') {
            return (
              <div key={idx} className="chat-message user-message">
                <div className="user-message-content">{msg.content}</div>
                <div className="avatar">U</div>
              </div>
            );
          } else {
            return (
              <div key={idx} className="chat-message result-message">
                <div className="avatar">AI</div>
                <div className="result-message-content">
                  {Array.isArray(msg.content) && msg.content.length > 0 ? (
                    msg.content.map((screenshot) => (
                      <ScreenshotResult key={screenshot.id} screenshot={screenshot} />
                    ))
                  ) : (
                    <div>No results found.</div>
                  )}
                </div>
              </div>
            );
          }
        })}
        {loading && <div className="chat-message loading-message">Searching...</div>}
      </div>
      <form className="chat-input-form" onSubmit={handleSubmit}>
        <input
          type="text"
          value={input}
          onChange={handleInputChange}
          placeholder="Type your search..."
          disabled={loading}
        />
        <button type="submit" disabled={loading || !input.trim()}>
          <FiSend size={20} style={{ marginBottom: -2 }} />
        </button>
      </form>
    </div>
  );
};

export default ChatSearch; 