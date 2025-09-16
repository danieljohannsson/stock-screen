import { useState } from "react";

interface Stock {
  symbol: string;
  price: number;
  pe_ratio: number;
  ps_ratio: number;
  peg_ratio: number;
  average_analyst_rating?: string;
  roe?: number;
  de_ratio?: number;
  score?: number;
}

function App() {
  const [symbol, setSymbol] = useState("");
  const [industry, setIndustry] = useState("");
  const [country, setCountry] = useState("US");
  const [stocks, setStocks] = useState<Stock[]>([]);
  const [error, setError] = useState("");

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    const params = new URLSearchParams();

    if (symbol.trim()) params.append("symbol", symbol.trim());
    else if (industry.trim()) {
      params.append("industry", industry.trim());
      params.append("country", country.trim());
    } else {
      setError("Enter a ticker symbol or an industry.");
      return;
    }

    try {
      const res = await fetch(
        //`http://localhost:8000/search?${params.toString()}`
        `http://localhost:8000/stocks`
      );
      const data = await res.json();
      console.log(data);

      if (!Array.isArray(data) || data.length === 0) {
        setError("No undervalued stocks found.");
      } else {
        setStocks(data);
        setError("");
      }
    } catch (err) {
      console.error(err);
      setError("Error fetching data.");
    }
  };

  return (
    <div className="min-h-screen bg-gray-100 p-6">
      <h1 className="text-3xl font-bold mb-6 text-center">
        📊 Undervalued Stock Search
      </h1>

      <form
        onSubmit={handleSubmit}
        className="flex flex-col items-center gap-4 mb-6"
      >
        <input
          className="border p-2 rounded w-64"
          placeholder="Ticker symbol (e.g., AAPL)"
          value={symbol}
          onChange={(e) => setSymbol(e.target.value)}
        />

        <button className="bg-blue-600 text-white px-4 py-2 rounded hover:bg-blue-700">
          Search
        </button>
      </form>

      {error && <p className="text-red-500 text-center mb-4">{error}</p>}

      <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 gap-4">
        {stocks.map((stock) => (
          <div key={stock.symbol} className="bg-white p-4 rounded-xl shadow">
            <h2 className="text-xl font-bold">{stock.symbol}</h2>
            <p>Price: ${stock.price?.toFixed(2)}</p>
            <p>P/E: {stock.pe_ratio?.toFixed(2)}</p>
            <p>P/S: {stock.ps_ratio?.toFixed(2)}</p>
            <p>PEG: {stock.peg_ratio?.toFixed(2)}</p>
            {stock.roe && <p>ROE: {stock.roe.toFixed(2)}%</p>}

            {stock.de_ratio && <p>D/E: {stock.de_ratio.toFixed(2)}</p>}
            {stock.average_analyst_rating && (
              <p>Analyst rating: {stock.average_analyst_rating}</p>
            )}
            {stock.score && (
              <p className="text-indigo-600">Score: {stock.score}</p>
            )}
          </div>
        ))}
      </div>
    </div>
  );
}

export default App;
