import { useState } from "react";

interface Stock {
  symbol: string;
  price: number;
  pe_ratio: number;
  pb_ratio: number;
  revenue_growth: number;
  roe?: number;
  de_ratio?: number;
  score?: number;
}

function App() {
  const [input, setInput] = useState("");
  const [stocks, setStocks] = useState<Stock[]>([]);
  const [error, setError] = useState("");

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!input.trim()) return;

    try {
      const res = await fetch(`http://localhost:8000/stocks?symbol=${input}`);
      const data = await res.json();
      console.log(data);

      if (data.length === 0) {
        setError("Stock could not be found.");
        return;
      }

      setStocks((prev) => [data[0], ...prev]);
      setError("");
    } catch (err) {
      console.error(err);
      setError("Failed to fetch stock data.");
    }

    setInput("");
  };

  return (
    <div className="min-h-screen bg-gray-100 p-6">
      <h1 className="text-3xl font-bold text-center mb-6">
        📉 Undervalued Stocks
      </h1>

      <form onSubmit={handleSubmit} className="flex justify-center gap-2 mb-6">
        <input
          className="border border-gray-300 p-2 rounded w-64"
          placeholder="Enter ticker (e.g., AAPL)"
          value={input}
          onChange={(e) => setInput(e.target.value)}
        />
        <button className="bg-blue-600 text-white px-4 py-2 rounded hover:bg-blue-700">
          Add
        </button>
      </form>

      {error && <p className="text-center text-red-500 mb-4">{error}</p>}

      <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 gap-4">
        {stocks.map((stock) => (
          <div
            key={stock.symbol}
            className="bg-white p-4 rounded-xl shadow hover:shadow-lg"
          >
            <h2 className="text-xl font-bold">{stock.symbol}</h2>
            <p>💲 Price: ${stock.price.toFixed(2)}</p>
            <p
              className={`text-sm ${
                stock.revenue_growth > 15 ? "text-green-600" : "text-red-500"
              }`}
            >
              Revenue Growth: {stock.revenue_growth.toFixed(2)}
            </p>
            <p
              className={`text-sm ${
                stock.pb_ratio < 1 ? "text-green-600" : "text-red-500"
              }`}
            >
              P/B: {stock.pb_ratio.toFixed(2)}
            </p>
            {stock.roe && (
              <p className="text-sm">ROE: {stock.roe.toFixed(2)}%</p>
            )}
            {stock.de_ratio && (
              <p className="text-sm">D/E: {stock.de_ratio.toFixed(2)}</p>
            )}
            {stock.score && (
              <p className="text-sm font-semibold text-indigo-600">
                Score: {stock.score}
              </p>
            )}
          </div>
        ))}
      </div>
    </div>
  );
}

export default App;
