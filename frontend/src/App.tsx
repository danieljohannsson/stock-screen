import { useState, useEffect } from "react";
import {
  BrowserRouter as Router,
  Routes,
  Route,
  useNavigate,
  useParams,
  useLocation,
  Link,
} from "react-router-dom";
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
  BarChart3,
  Building2,
  ArrowUpDown,
  DollarSign,
  ArrowLeft,
} from "lucide-react";
import CompanyProfile from "./components/CompanyProfile";
import HealthIndicator from "./components/HealthIndicator";

interface Stock {
  symbol: string;
  name: string;
  price: number;
  pe_ratio: number;
  ps_ratio: number;
  pb_ratio: number;
  peg_ratio: number;
  dividend_yield?: number;
  revenue_growth: number;
  earnings_growth: number;
  de_ratio: number;
  roe?: number;
  free_cash_flow?: number;
  average_analyst_rating?: string;
  summary?: string;
  industry?: string;
  website?: string;
  balanced_score: number;
  value_score: number;
  growth_score: number;
  momentum_score: number;
  quality_score: number;
}

type SortField = keyof Stock;
type SortDirection = "asc" | "desc";

function StockScreener() {
  const [stocks, setStocks] = useState<Stock[]>([]);
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);
  const [sortField, setSortField] = useState<SortField>("balanced_score");
  const [sortDirection, setSortDirection] = useState<SortDirection>("desc");
  const [selectedStrategy, setSelectedStrategy] = useState("balanced");
  const navigate = useNavigate();

  useEffect(() => {
    const interval = setInterval(() => {
      fetch(
        `${
          import.meta.env.VITE_BACKEND_PRODUCTION_URL ||
          import.meta.env.VITE_BACKEND_LOCAL_URL
        }/health`
      ).catch(() => {});
    }, 5 * 60 * 1000); // every 5 minutes
    return () => clearInterval(interval);
  }, []);

  useEffect(() => {
    const fetchStocks = async () => {
      setLoading(true);
      try {
        const res = await fetch(
          `${
            import.meta.env.VITE_BACKEND_PRODUCTION_URL ||
            import.meta.env.VITE_BACKEND_LOCAL_URL
          }/stocks?limit=100&strategy=${selectedStrategy}`
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

  const getColumnsForStrategy = (strategy: string) => {
    const baseColumns = [
      {
        key: "score",
        label: "Score",
        icon: <ArrowUpDown className="h-4 w-4" />,
      },
      {
        key: "symbol",
        label: "Symbol",
        icon: <ArrowUpDown className="h-4 w-4" />,
      },
      {
        key: "name",
        label: "Company",
        icon: <ArrowUpDown className="h-4 w-4" />,
      },
    ];

    switch (strategy) {
      case "growth":
        return [
          ...baseColumns,
          {
            key: "peg_ratio",
            label: "PEG Ratio",
            icon: <TrendingUp className="h-4 w-4" />,
          },
          {
            key: "revenue_growth",
            label: "Revenue Growth (yoy)",
            icon: <TrendingUp className="h-4 w-4" />,
          },
          {
            key: "de_ratio",
            label: "D/E Ratio",
            icon: <Building2 className="h-4 w-4" />,
          },
          {
            key: "average_analyst_rating",
            label: "Analyst Rating",
            icon: null,
          },
        ];
      case "value":
        return [
          ...baseColumns,
          {
            key: "revenue_growth",
            label: "Revenue Growth (yoy)",
            icon: <TrendingUp className="h-4 w-4" />,
          },
          {
            key: "earnings_growth",
            label: "Earnings Growth (yoy)",
            icon: <TrendingDown className="h-4 w-4" />,
          },
          {
            key: "roe",
            label: "ROE",
            icon: <BarChart3 className="h-4 w-4" />,
          },
          {
            key: "de_ratio",
            label: "D/E Ratio",
            icon: <Building2 className="h-4 w-4" />,
          },
          {
            key: "free_cash_flow",
            label: "Free Cash Flow",
            icon: <DollarSign className="h-4 w-4" />,
          },
          {
            key: "peg_ratio",
            label: "PEG Ratio",
            icon: <TrendingUp className="h-4 w-4" />,
          },
          {
            key: "average_analyst_rating",
            label: "Analyst Rating",
            icon: null,
          },
        ];
      case "momentum":
        return [
          ...baseColumns,
          {
            key: "earnings_growth",
            label: "Earnings Growth (yoy)",
            icon: <TrendingDown className="h-4 w-4" />,
          },
          {
            key: "revenue_growth",
            label: "Revenue Growth (yoy)",
            icon: <TrendingUp className="h-4 w-4" />,
          },
          {
            key: "roe",
            label: "ROE",
            icon: <BarChart3 className="h-4 w-4" />,
          },
          {
            key: "average_analyst_rating",
            label: "Analyst Rating",
            icon: null,
          },
        ];
      case "quality":
        return [
          ...baseColumns,
          {
            key: "pb_ratio",
            label: "P/B Ratio",
            icon: <BarChart3 className="h-4 w-4" />,
          },
          {
            key: "roe",
            label: "ROE",
            icon: <BarChart3 className="h-4 w-4" />,
          },
          {
            key: "de_ratio",
            label: "D/E Ratio",
            icon: <Building2 className="h-4 w-4" />,
          },
          {
            key: "free_cash_flow",
            label: "Free Cash Flow",
            icon: <DollarSign className="h-4 w-4" />,
          },
          {
            key: "dividend_yield",
            label: "Dividend Yield",
            icon: <DollarSign className="h-4 w-4" />,
          },
          {
            key: "revenue_growth",
            label: "Revenue Growth (yoy)",
            icon: <TrendingUp className="h-4 w-4" />,
          },
          {
            key: "average_analyst_rating",
            label: "Analyst Rating",
            icon: null,
          },
        ];
      default: // balanced
        return [
          ...baseColumns,
          {
            key: "revenue_growth",
            label: "Revenue Growth (yoy)",
            icon: <TrendingUp className="h-4 w-4" />,
          },
          {
            key: "earnings_growth",
            label: "Earnings Growth (yoy)",
            icon: <TrendingDown className="h-4 w-4" />,
          },
          {
            key: "roe",
            label: "ROE",
            icon: <BarChart3 className="h-4 w-4" />,
          },
          {
            key: "de_ratio",
            label: "D/E Ratio",
            icon: <Building2 className="h-4 w-4" />,
          },
          {
            key: "free_cash_flow",
            label: "Free Cash Flow",
            icon: <DollarSign className="h-4 w-4" />,
          },
          {
            key: "peg_ratio",
            label: "PEG Ratio",
            icon: <TrendingUp className="h-4 w-4" />,
          },
          {
            key: "average_analyst_rating",
            label: "Analyst Rating",
            icon: null,
          },
        ];
    }
  };

  const renderCellContent = (stock: Stock, columnKey: string) => {
    switch (columnKey) {
      case "score":
        return (
          <Badge
            variant="outline"
            className={`text-sm font-bold ${
              (stock[`${selectedStrategy}_score` as keyof Stock] as number) >=
              80
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
        );
      case "symbol":
        return <span className="font-medium">{stock.symbol}</span>;
      case "name":
        return (
          <span className="text-muted-foreground">{stock.name || "--"}</span>
        );
      case "pe_ratio":
        return stock.pe_ratio ? stock.pe_ratio.toFixed(2) : "--";
      case "ps_ratio":
        return stock.ps_ratio ? stock.ps_ratio.toFixed(2) : "--";
      case "peg_ratio":
        return stock.peg_ratio ? stock.peg_ratio.toFixed(2) : "--";
      case "revenue_growth":
        return (
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
        );
      case "earnings_growth":
        return (
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
        );
      case "de_ratio":
        return stock.de_ratio?.toFixed(2) ? stock.de_ratio.toFixed(2) : "--";
      case "roe":
        return stock.roe ? (stock.roe * 100).toFixed(1) + "%" : "--";
      case "free_cash_flow":
        return stock.free_cash_flow ? (
          <span
            className={`font-semibold ${
              stock.free_cash_flow > 0
                ? "text-green-600"
                : stock.free_cash_flow < 0
                ? "text-red-600"
                : "text-black"
            }`}
          >
            ${(stock.free_cash_flow / 1000000000).toFixed(1)}B
          </span>
        ) : (
          "--"
        );
      case "dividend_yield":
        return stock.dividend_yield ? (
          <span className="font-semibold">
            {stock.dividend_yield.toFixed(2)}%
          </span>
        ) : (
          "--"
        );
      case "pb_ratio":
        return stock.pb_ratio ? stock.pb_ratio.toFixed(2) : "--";
      case "average_analyst_rating":
        return stock.average_analyst_rating ? (
          <Badge
            variant="outline"
            className={`${getRatingColor(stock.average_analyst_rating)}`}
          >
            {stock.average_analyst_rating}
          </Badge>
        ) : (
          <Badge variant="outline" className="text-sm">
            N/A
          </Badge>
        );
      default:
        return "--";
    }
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
            <div className="flex items-center gap-4">
              <HealthIndicator showDetails={true} />
              <div className="flex items-center gap-2">
                <div className="h-2 w-2 bg-green-500 rounded-full"></div>
                <span className="text-xs text-muted-foreground">
                  {stocks.length} stocks
                </span>
              </div>
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
                {getColumnsForStrategy(selectedStrategy).map((column) => (
                  <TableHead
                    key={column.key}
                    className="cursor-pointer hover:bg-muted/50"
                    onClick={() => {
                      if (column.key === "score") {
                        handleSort(`${selectedStrategy}_score` as SortField);
                      } else {
                        handleSort(column.key as SortField);
                      }
                    }}
                  >
                    <div className="flex items-center gap-2">
                      {column.icon}
                      {column.label}
                      {column.key !== "average_analyst_rating" && (
                        <ArrowUpDown className="h-4 w-4" />
                      )}
                    </div>
                  </TableHead>
                ))}
              </TableRow>
            </TableHeader>
            <TableBody>
              {sortedStocks.map((stock) => (
                <TableRow
                  key={stock.symbol}
                  className="hover:bg-muted/50 cursor-pointer"
                  onClick={() =>
                    navigate(`/company/${stock.symbol}`, { state: { stock } })
                  }
                >
                  {getColumnsForStrategy(selectedStrategy).map((column) => (
                    <TableCell key={column.key}>
                      {renderCellContent(stock, column.key)}
                    </TableCell>
                  ))}
                </TableRow>
              ))}
            </TableBody>
          </Table>
        </div>
      </div>
    </div>
  );
}

// Wrapper component to handle stock data passing
function CompanyProfileWrapper() {
  const { symbol } = useParams<{ symbol: string }>();
  const location = useLocation();
  const [stock, setStock] = useState<Stock | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  useEffect(() => {
    // Check if stock data was passed via navigation state
    const passedStock = location.state?.stock;

    if (passedStock && passedStock.symbol === symbol) {
      setStock(passedStock);
      setLoading(false);
      return;
    }

    // Fallback: fetch stock data if not passed
    const fetchStock = async () => {
      if (!symbol) return;

      setLoading(true);
      try {
        const res = await fetch(
          `${
            import.meta.env.VITE_API_URL || "http://localhost:8000"
          }/stocks?limit=1000&strategy=balanced`
        );
        const data = await res.json();

        if (Array.isArray(data)) {
          const foundStock = data.find((s: Stock) => s.symbol === symbol);
          if (foundStock) {
            setStock(foundStock);
          } else {
            setError("Company not found");
          }
        } else {
          setError("Error fetching company data");
        }
      } catch (err) {
        console.error(err);
        setError("Error fetching company data");
      } finally {
        setLoading(false);
      }
    };

    fetchStock();
  }, [symbol, location.state]);

  if (loading) {
    return (
      <div className="min-h-screen bg-background p-6">
        <div className="max-w-4xl mx-auto">
          <div className="flex items-center justify-center h-64">
            <div className="text-center">
              <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600 mx-auto mb-4"></div>
              <p className="text-muted-foreground">
                Loading company profile...
              </p>
            </div>
          </div>
        </div>
      </div>
    );
  }

  if (error || !stock) {
    return (
      <div className="min-h-screen bg-background p-6">
        <div className="max-w-4xl mx-auto">
          <div className="flex items-center justify-center h-64">
            <div className="text-center">
              <h1 className="text-2xl font-semibold text-destructive mb-4">
                Company Not Found
              </h1>
              <p className="text-muted-foreground mb-6">{error}</p>
              <Link
                to="/"
                className="inline-flex items-center gap-2 px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors"
              >
                <ArrowLeft className="h-4 w-4" />
                Back to Stock Screener
              </Link>
            </div>
          </div>
        </div>
      </div>
    );
  }

  return <CompanyProfile stock={stock} />;
}

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<StockScreener />} />
        <Route path="/company/:symbol" element={<CompanyProfileWrapper />} />
      </Routes>
    </Router>
  );
}

export default App;
