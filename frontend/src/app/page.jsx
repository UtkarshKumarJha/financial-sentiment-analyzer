'use client';

import { useState } from 'react';
import axios from 'axios';
import './globals.css';

const TICKERS = {
  Apple: 'AAPL',
  Google: 'GOOGL',
  Microsoft: 'MSFT',
  Amazon: 'AMZN',
  Tesla: 'TSLA',
  Nvidia: 'NVDA',
  Facebook: 'META',
};

export default function Home() {
  const [query, setQuery] = useState('');
  const [suggestions, setSuggestions] = useState([]);
  const [selectedTicker, setSelectedTicker] = useState('');
  const [results, setResults] = useState([]);
  const [loading, setLoading] = useState(false);

  const handleInputChange = (e) => {
    const value = e.target.value;
    setQuery(value);
    const matches = Object.keys(TICKERS).filter((company) =>
      company.toLowerCase().includes(value.toLowerCase())
    );
    setSuggestions(matches);
  };

  const handleSelect = async (company) => {
    const ticker = TICKERS[company];
    setSelectedTicker(ticker);
    setQuery(company);
    setSuggestions([]);
    setLoading(true);
    try {
      const res = await axios.get(`http://localhost:5000/analyze?ticker=${ticker}`);
      setResults(res.data);
    } catch (err) {
      console.error('Error fetching sentiment:', err);
      setResults([]);
    }
    setLoading(false);
  };

  const handleClear = () => {
    setQuery('');
    setResults([]);
    setSelectedTicker('');
    setSuggestions([]);
  };

  const getSentimentColor = (sentiment) => {
    if (sentiment === 'positive') return 'text-green-600';
    if (sentiment === 'negative') return 'text-red-600';
    return 'text-yellow-600';
  };

  return (
  <div className="min-h-screen bg-gray-50 py-10 px-4">
    <div className="max-w-3xl mx-auto bg-white p-8 rounded-xl shadow-md">
      <h1 className="text-4xl font-bold mb-6 text-center text-blue-800">
        📊 Stock Sentiment Analyzer
      </h1>

      <div className="flex gap-2 mb-4">
        <input
          type="text"
          placeholder="Enter company name (e.g., Apple)"
          value={query}
          onChange={handleInputChange}
          className="flex-1 border border-gray-300 px-4 py-2 rounded-lg shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-400"
        />
        <button
          onClick={handleClear}
          className="bg-gray-200 text-gray-700 px-4 py-2 rounded-lg hover:bg-gray-300"
        >
          Clear
        </button>
      </div>

      {suggestions.length > 0 && (
        <ul className="bg-white border border-gray-300 rounded-lg shadow mb-4 max-h-40 overflow-y-auto">
          {suggestions.map((company) => (
            <li
              key={company}
              onClick={() => handleSelect(company)}
              className="px-4 py-2 hover:bg-blue-100 cursor-pointer"
            >
              {company}
            </li>
          ))}
        </ul>
      )}

      {loading && (
        <p className="text-blue-600 font-medium animate-pulse">
          🔄 Analyzing news articles...
        </p>
      )}

      {!loading && results.length === 0 && selectedTicker && (
        <p className="text-gray-500">No sentiment data found for "{selectedTicker}".</p>
      )}

      {!loading && results.length > 0 && (
        <div className="space-y-6 mt-6">
          {results.map((article, idx) => (
            <div
              key={idx}
              className="border border-gray-200 p-6 rounded-xl shadow-md bg-white hover:shadow-lg transition-shadow"
            >
              <a
                href={article.url}
                target="_blank"
                rel="noopener noreferrer"
                className="text-xl font-semibold text-blue-700 hover:underline"
              >
                {article.title}
              </a>
              <p className="text-sm text-gray-500 mt-1">
                Published: {new Date(article.publishedAt).toLocaleString()}
              </p>
              <p className={`mt-2 text-base font-medium ${getSentimentColor(article.sentiment)}`}>
                Sentiment: {article.sentiment} ({Math.round(article.confidence * 100)}%)
              </p>
            </div>
          ))}
        </div>
      )}
    </div>
  </div>
);

}
