import { useEffect, useState } from "react";

function App() {
  const [stocks, setStocks] = useState<any[]>([]);

  useEffect(() => {
    fetch("http://localhost:8000/stocks")
      .then((res) => res.json())
      .then((data) => setStocks(data))
      .catch((err) => console.error("Error fetching stocks:", err));
  }, []);

  return (
    <div>
      <h1>Undervalued Stocks</h1>
      <ul>
        {stocks.map((stock) => (
          <li key={stock.symbol}>
            {stock.symbol} - ${stock.price} (P/E: {stock.pe_ratio}, P/B:{" "}
            {stock.pb_ratio})
          </li>
        ))}
      </ul>
    </div>
  );
}

export default App;
