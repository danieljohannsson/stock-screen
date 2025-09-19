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
  summary?: string;
  balanced_score: number;
  value_score: number;
  growth_score: number;
  momentum_score: number;
  quality_score: number;
}

type SortField = keyof Stock;
type SortDirection = "asc" | "desc";

function App() {
  const [stocks, setStocks] = useState<Stock[]>([]);
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);
  const [sortField, setSortField] = useState<SortField>("balanced_score");
  const [sortDirection, setSortDirection] = useState<SortDirection>("desc");
  const [selectedStrategy, setSelectedStrategy] = useState("balanced");

  useEffect(() => {
    const fetchStocks = async () => {
      setLoading(true);
      try {
        const res = await fetch(
          `http://localhost:8000/stocks?limit=100&strategy=${selectedStrategy}`
        );
        const data = await res.json();
        console.log(data);

        if (!Array.isArray(data) || data.length === 0) {
          setError("No undervalued stocks found.");
        } else {
          setStocks(data);
          setSortField(`${selectedStrategy}_score` as SortField);
          setSortDirection("desc");
          setError("");
        }
      } catch (err) {
        console.error(err);
        setError("Error fetching data.");
      } finally {
        setLoading(false);
      }
    };
    fetchStocks();
  }, [selectedStrategy]);

  const handleSort = (field: SortField) => {
    if (sortField === field) {
      setSortDirection(sortDirection === "asc" ? "desc" : "asc");
    } else {
      setSortField(field);
      setSortDirection("desc");
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
        <div className="mb-6">
          <div className="flex items-center justify-between mb-4">
            <div>
              <h1 className="text-2xl font-semibold text-foreground">
                Stock Screener
              </h1>
              <p className="text-sm text-muted-foreground mt-1">
                Discover undervalued stocks with comprehensive financial metrics
              </p>
            </div>
            <div className="flex items-center gap-2">
              <div className="h-2 w-2 bg-green-500 rounded-full"></div>
              <span className="text-xs text-muted-foreground">
                {stocks.length} stocks
              </span>
            </div>
          </div>
        </div>

        {/* Strategy Selection Cards */}
        <div className="mb-6">
          <h2 className="text-lg font-medium text-foreground mb-4">
            Investment Strategy
          </h2>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-5 gap-4">
            <div
              className={`p-4 rounded-lg border-2 cursor-pointer transition-all duration-200 ${
                selectedStrategy === "balanced"
                  ? "border-blue-500 bg-blue-50 shadow-md"
                  : "border-gray-200 bg-white hover:border-gray-300 hover:shadow-sm"
              }`}
              onClick={() => setSelectedStrategy("balanced")}
            >
              <div className="flex items-center space-x-3">
                <div className="w-3 h-3 rounded-full bg-blue-500"></div>
                <div>
                  <h3 className="font-medium text-sm">Balanced</h3>
                  <p className="text-xs text-muted-foreground">
                    Equal weight all factors
                  </p>
                </div>
              </div>
            </div>

            <div
              className={`p-4 rounded-lg border-2 cursor-pointer transition-all duration-200 ${
                selectedStrategy === "value"
                  ? "border-green-500 bg-green-50 shadow-md"
                  : "border-gray-200 bg-white hover:border-gray-300 hover:shadow-sm"
              }`}
              onClick={() => setSelectedStrategy("value")}
            >
              <div className="flex items-center space-x-3">
                <div className="w-3 h-3 rounded-full bg-green-500"></div>
                <div>
                  <h3 className="font-medium text-sm">Value</h3>
                  <p className="text-xs text-muted-foreground">
                    Focus on undervalued stocks
                  </p>
                </div>
              </div>
            </div>

            <div
              className={`p-4 rounded-lg border-2 cursor-pointer transition-all duration-200 ${
                selectedStrategy === "growth"
                  ? "border-purple-500 bg-purple-50 shadow-md"
                  : "border-gray-200 bg-white hover:border-gray-300 hover:shadow-sm"
              }`}
              onClick={() => setSelectedStrategy("growth")}
            >
              <div className="flex items-center space-x-3">
                <div className="w-3 h-3 rounded-full bg-purple-500"></div>
                <div>
                  <h3 className="font-medium text-sm">Growth</h3>
                  <p className="text-xs text-muted-foreground">
                    High growth potential
                  </p>
                </div>
              </div>
            </div>

            <div
              className={`p-4 rounded-lg border-2 cursor-pointer transition-all duration-200 ${
                selectedStrategy === "momentum"
                  ? "border-orange-500 bg-orange-50 shadow-md"
                  : "border-gray-200 bg-white hover:border-gray-300 hover:shadow-sm"
              }`}
              onClick={() => setSelectedStrategy("momentum")}
            >
              <div className="flex items-center space-x-3">
                <div className="w-3 h-3 rounded-full bg-orange-500"></div>
                <div>
                  <h3 className="font-medium text-sm">Momentum</h3>
                  <p className="text-xs text-muted-foreground">
                    Strong recent performance
                  </p>
                </div>
              </div>
            </div>

            <div
              className={`p-4 rounded-lg border-2 cursor-pointer transition-all duration-200 ${
                selectedStrategy === "quality"
                  ? "border-indigo-500 bg-indigo-50 shadow-md"
                  : "border-gray-200 bg-white hover:border-gray-300 hover:shadow-sm"
              }`}
              onClick={() => setSelectedStrategy("quality")}
            >
              <div className="flex items-center space-x-3">
                <div className="w-3 h-3 rounded-full bg-indigo-500"></div>
                <div>
                  <h3 className="font-medium text-sm">Quality</h3>
                  <p className="text-xs text-muted-foreground">
                    Financially strong companies
                  </p>
                </div>
              </div>
            </div>
          </div>
        </div>

        {loading && (
          <div className="mb-6 p-4 bg-blue-50 border border-blue-200 rounded-lg">
            <p className="text-blue-600 text-center">
              Loading stocks with {selectedStrategy} strategy...
            </p>
          </div>
        )}

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
                  onClick={() =>
                    handleSort(`${selectedStrategy}_score` as SortField)
                  }
                >
                  <div className="flex items-center gap-2">
                    Score
                    <ArrowUpDown className="h-4 w-4" />
                  </div>
                </TableHead>
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
                  <TableCell>
                    <Badge
                      variant="outline"
                      className={`text-sm font-bold ${
                        (stock[
                          `${selectedStrategy}_score` as keyof Stock
                        ] as number) >= 80
                          ? "bg-green-100 text-green-800 border-green-200"
                          : (stock[
                              `${selectedStrategy}_score` as keyof Stock
                            ] as number) >= 60
                          ? "bg-blue-100 text-blue-800 border-blue-200"
                          : (stock[
                              `${selectedStrategy}_score` as keyof Stock
                            ] as number) >= 40
                          ? "bg-yellow-100 text-yellow-800 border-yellow-200"
                          : "bg-red-100 text-red-800 border-red-200"
                      }`}
                    >
                      {stock[`${selectedStrategy}_score` as keyof Stock] || 0}
                    </Badge>
                  </TableCell>
                  <TableCell className="font-medium">{stock.symbol}</TableCell>
                  <TableCell>
                    <Badge variant="outline" className="text-sm">
                      ${stock.price?.toFixed(2)}
                    </Badge>
                  </TableCell>
                  <TableCell>
                    {stock.pe_ratio ? stock.pe_ratio?.toFixed(2) : "--"}
                  </TableCell>
                  <TableCell>
                    {stock.ps_ratio ? stock.ps_ratio?.toFixed(2) : "--"}
                  </TableCell>
                  <TableCell>
                    {stock.peg_ratio ? stock.peg_ratio?.toFixed(2) : "--"}
                  </TableCell>
                  <TableCell>
                    <span
                      className={`font-semibold ${
                        stock.revenue_growth > 0
                          ? "text-green-600"
                          : stock.revenue_growth < 0
                          ? "text-red-600"
                          : "text-black"
                      }`}
                    >
                      {stock.revenue_growth
                        ? (stock.revenue_growth * 100).toFixed(1) + "%"
                        : "--"}
                    </span>
                  </TableCell>
                  <TableCell>
                    <span
                      className={`font-semibold ${
                        stock.earnings_growth > 0
                          ? "text-green-600"
                          : stock.earnings_growth < 0
                          ? "text-red-600"
                          : "text-black"
                      }`}
                    >
                      {stock.earnings_growth
                        ? (stock.earnings_growth * 100).toFixed(1) + "%"
                        : "--"}
                    </span>
                  </TableCell>
                  <TableCell>
                    {stock.de_ratio?.toFixed(2)
                      ? stock.de_ratio?.toFixed(2)
                      : "--"}
                  </TableCell>
                  <TableCell>
                    {stock.average_analyst_rating ? (
                      <Badge
                        variant="outline"
                        className={`${getRatingColor(
                          stock.average_analyst_rating
                        )}`}
                      >
                        {stock.average_analyst_rating}
                      </Badge>
                    ) : (
                      <Badge variant="outline" className="text-sm">
                        N/A
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
