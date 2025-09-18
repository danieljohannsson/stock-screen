import { useState, useEffect } from "react";
import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from "@/components/ui/table";
import { Badge } from "@/components/ui/badge";
import {
  TrendingUp,
  TrendingDown,
  DollarSign,
  BarChart3,
  Target,
  Building2,
  ArrowUpDown,
} from "lucide-react";

interface Stock {
  symbol: string;
  price: number;
  pe_ratio: number;
  ps_ratio: number;
  peg_ratio: number;
  revenue_growth: number;
  earnings_growth: number;
  de_ratio: number;
  average_analyst_rating?: string;
}

type SortField = keyof Stock;
type SortDirection = "asc" | "desc";

function App() {
  const [stocks, setStocks] = useState<Stock[]>([]);
  const [error, setError] = useState("");
  const [sortField, setSortField] = useState<SortField>("symbol");
  const [sortDirection, setSortDirection] = useState<SortDirection>("asc");

  useEffect(() => {
    const fetchStocks = async () => {
      try {
        const res = await fetch(`http://localhost:8000/stocks`);
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

    fetchStocks();
  }, []);

  const handleSort = (field: SortField) => {
    if (sortField === field) {
      setSortDirection(sortDirection === "asc" ? "desc" : "asc");
    } else {
      setSortField(field);
      setSortDirection("asc");
    }
  };

  const sortedStocks = [...stocks].sort((a, b) => {
    const aValue = a[sortField];
    const bValue = b[sortField];

    if (aValue === undefined || bValue === undefined) return 0;

    if (typeof aValue === "string" && typeof bValue === "string") {
      return sortDirection === "asc"
        ? aValue.localeCompare(bValue)
        : bValue.localeCompare(aValue);
    }

    if (typeof aValue === "number" && typeof bValue === "number") {
      return sortDirection === "asc" ? aValue - bValue : bValue - aValue;
    }

    return 0;
  });

  const getRatingColor = (rating: string) => {
    if (rating.includes("Strong Buy"))
      return "bg-green-100 text-green-800 border-green-200 justify-center";
    if (rating.includes("Buy"))
      return "bg-blue-100 text-blue-800 border-blue-200";
    if (rating.includes("Hold"))
      return "bg-yellow-100 text-yellow-800 border-yellow-200";
    if (rating.includes("Sell"))
      return "bg-red-100 text-red-800 border-red-200";
    return "bg-gray-100 text-gray-800 border-gray-200";
  };

  return (
    <div className="min-h-screen bg-background p-6">
      <div className="max-w-7xl mx-auto">
        <div className="text-center mb-8">
          <h1 className="text-4xl font-bold text-foreground mb-2">
            📊 Stock Screener
          </h1>
          <p className="text-muted-foreground">
            Discover undervalued stocks with comprehensive financial metrics
          </p>
        </div>

        {error && (
          <div className="mb-6 p-4 bg-destructive/10 border border-destructive/20 rounded-lg">
            <p className="text-destructive text-center">{error}</p>
          </div>
        )}

        <div className="rounded-md border">
          <Table>
            <TableHeader>
              <TableRow>
                <TableHead
                  className="cursor-pointer hover:bg-muted/50"
                  onClick={() => handleSort("symbol")}
                >
                  <div className="flex items-center gap-2">
                    Symbol
                    <ArrowUpDown className="h-4 w-4" />
                  </div>
                </TableHead>
                <TableHead
                  className="cursor-pointer hover:bg-muted/50"
                  onClick={() => handleSort("price")}
                >
                  <div className="flex items-center gap-2">
                    <DollarSign className="h-4 w-4" />
                    Price
                    <ArrowUpDown className="h-4 w-4" />
                  </div>
                </TableHead>
                <TableHead
                  className="cursor-pointer hover:bg-muted/50"
                  onClick={() => handleSort("pe_ratio")}
                >
                  <div className="flex items-center gap-2">
                    <BarChart3 className="h-4 w-4" />
                    P/E Ratio
                    <ArrowUpDown className="h-4 w-4" />
                  </div>
                </TableHead>
                <TableHead
                  className="cursor-pointer hover:bg-muted/50"
                  onClick={() => handleSort("ps_ratio")}
                >
                  <div className="flex items-center gap-2">
                    <Target className="h-4 w-4" />
                    P/S Ratio
                    <ArrowUpDown className="h-4 w-4" />
                  </div>
                </TableHead>
                <TableHead
                  className="cursor-pointer hover:bg-muted/50"
                  onClick={() => handleSort("peg_ratio")}
                >
                  <div className="flex items-center gap-2">
                    <TrendingUp className="h-4 w-4" />
                    PEG Ratio
                    <ArrowUpDown className="h-4 w-4" />
                  </div>
                </TableHead>
                <TableHead
                  className="cursor-pointer hover:bg-muted/50"
                  onClick={() => handleSort("revenue_growth")}
                >
                  <div className="flex items-center gap-2">
                    <TrendingUp className="h-4 w-4" />
                    Revenue Growth
                    <ArrowUpDown className="h-4 w-4" />
                  </div>
                </TableHead>
                <TableHead
                  className="cursor-pointer hover:bg-muted/50"
                  onClick={() => handleSort("earnings_growth")}
                >
                  <div className="flex items-center gap-2">
                    <TrendingDown className="h-4 w-4" />
                    Earnings Growth
                    <ArrowUpDown className="h-4 w-4" />
                  </div>
                </TableHead>
                <TableHead
                  className="cursor-pointer hover:bg-muted/50"
                  onClick={() => handleSort("de_ratio")}
                >
                  <div className="flex items-center gap-2">
                    <Building2 className="h-4 w-4" />
                    D/E Ratio
                    <ArrowUpDown className="h-4 w-4" />
                  </div>
                </TableHead>
                <TableHead>Analyst Rating</TableHead>
              </TableRow>
            </TableHeader>
            <TableBody>
              {sortedStocks.map((stock) => (
                <TableRow key={stock.symbol} className="hover:bg-muted/50">
                  <TableCell className="font-medium">{stock.symbol}</TableCell>
                  <TableCell>
                    <Badge variant="outline" className="text-sm">
                      ${stock.price?.toFixed(2)}
                    </Badge>
                  </TableCell>
                  <TableCell>{stock.pe_ratio?.toFixed(2)}</TableCell>
                  <TableCell>{stock.ps_ratio?.toFixed(2)}</TableCell>
                  <TableCell>{stock.peg_ratio?.toFixed(2)}</TableCell>
                  <TableCell>
                    <span
                      className={`font-semibold ${
                        stock.revenue_growth >= 0
                          ? "text-green-600"
                          : "text-red-600"
                      }`}
                    >
                      {(stock.revenue_growth * 100).toFixed(1)}%
                    </span>
                  </TableCell>
                  <TableCell>
                    <span
                      className={`font-semibold ${
                        stock.earnings_growth >= 0
                          ? "text-green-600"
                          : "text-red-600"
                      }`}
                    >
                      {(stock.earnings_growth * 100).toFixed(1)}%
                    </span>
                  </TableCell>
                  <TableCell>{stock.de_ratio?.toFixed(2)}</TableCell>
                  <TableCell>
                    {stock.average_analyst_rating && (
                      <Badge
                        variant="outline"
                        className={`${getRatingColor(
                          stock.average_analyst_rating
                        )}`}
                      >
                        {stock.average_analyst_rating.split(" - ")[1]}
                      </Badge>
                    )}
                  </TableCell>
                </TableRow>
              ))}
            </TableBody>
          </Table>
        </div>
      </div>
    </div>
  );
}

export default App;
