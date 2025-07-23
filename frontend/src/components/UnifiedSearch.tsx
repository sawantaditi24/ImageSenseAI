import React, { useState } from "react";
import axios from "axios";

type Screenshot = {
  id: number;
  filename: string;
  category: string;
  upload_time: string;
  image_url: string;
};

type QueryResponse = {
  type: "category" | "semantic";
  category?: string;
  results: Screenshot[];
};

const UnifiedSearch: React.FC = () => {
  const [query, setQuery] = useState("");
  const [results, setResults] = useState<Screenshot[]>([]);
  const [searchType, setSearchType] = useState<string | undefined>();
  const [loading, setLoading] = useState(false);

  const handleSearch = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!query.trim()) return;
    setLoading(true);
    try {
      const res = await axios.get<QueryResponse>(
        `/api/v1/query?query=${encodeURIComponent(query)}`
      );
      setResults(res.data.results);
      setSearchType(res.data.type === "category" ? res.data.category : "semantic");
    } catch (err) {
      alert("Error searching. See console for details.");
      console.error(err);
    }
    setLoading(false);
  };

  return (
    <div className="max-w-2xl mx-auto p-4">
      <form onSubmit={handleSearch} className="flex gap-2 mb-6">
        <input
          className="flex-1 border rounded px-3 py-2"
          type="text"
          placeholder="Ask anything about your screenshots…"
          value={query}
          onChange={e => setQuery(e.target.value)}
        />
        <button
          className="bg-blue-600 text-white px-4 py-2 rounded"
          type="submit"
          disabled={loading}
        >
          {loading ? "Searching..." : "Search"}
        </button>
      </form>
      {searchType && (
        <div className="mb-4 text-gray-600">
          Showing results for <b>{searchType}</b>
        </div>
      )}
      <div className="grid grid-cols-1 sm:grid-cols-2 gap-6">
        {results.map(s => (
          <div key={s.id} className="bg-white rounded shadow p-2">
            <img
              src={s.image_url}
              alt={s.filename}
              className="w-full h-40 object-cover rounded mb-2"
            />
            <div className="flex justify-between items-center">
              <span className="text-xs bg-blue-100 text-blue-800 px-2 py-1 rounded-full">
                {s.category}
              </span>
              <span className="text-xs text-gray-400">
                {new Date(s.upload_time).toLocaleDateString()}
              </span>
            </div>
            <div className="text-xs text-gray-500 mt-1">{s.filename}</div>
          </div>
        ))}
      </div>
      {!loading && results.length === 0 && (
        <div className="text-center text-gray-400 mt-8">No results yet.</div>
      )}
    </div>
  );
};

export default UnifiedSearch;
