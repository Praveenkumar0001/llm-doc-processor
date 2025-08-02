import { useState } from 'react';
import axios from 'axios';

export default function Home() {
  const [query, setQuery] = useState('');
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const handleSearch = async () => {
    try {
      setLoading(true);
      setError(null);
      const res = await axios.post('/api/query', { query });
      setResult(res.data);
    } catch (e) {
      setError('Failed to fetch results.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="p-4 max-w-xl mx-auto">
      <h1 className="text-2xl font-bold mb-4">LLM Document Processor</h1>
      <input
        className="border p-2 w-full mb-2 rounded"
        value={query}
        onChange={e => setQuery(e.target.value)}
        placeholder="Enter your query"
      />
      <button onClick={handleSearch} className="bg-blue-600 hover:bg-blue-700 text-white px-4 py-2 rounded disabled:opacity-50" disabled={loading}>
        {loading ? 'Searching...' : 'Search'}
      </button>
      {error && <div className="text-red-500 mt-2">{error}</div>}
      {result && (
        <pre className="mt-4 bg-gray-100 p-4 rounded overflow-x-auto text-sm">{JSON.stringify(result, null, 2)}</pre>
      )}
    </div>
  );
}