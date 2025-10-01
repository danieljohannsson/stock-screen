import { Link } from "react-router-dom";
import { Badge } from "@/components/ui/badge";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import {
  ArrowLeft,
  ExternalLink,
  Building2,
  Globe,
  BarChart3,
} from "lucide-react";
import HealthIndicator from "./HealthIndicator";

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
  revenue_growth_3yr?: number;
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
  last_fetched?: string;
}

interface CompanyProfileProps {
  stock: Stock;
}

function CompanyProfile({ stock }: CompanyProfileProps) {
  const getRatingColor = (rating: string) => {
    if (rating.includes("Strong Buy"))
      return "bg-green-100 text-green-800 border-green-200";
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
      <div className="max-w-4xl mx-auto">
        {/* Header */}
        <div className="mb-6">
          <Link
            to="/"
            className="inline-flex items-center gap-2 text-muted-foreground hover:text-foreground transition-colors mb-4"
          >
            <ArrowLeft className="h-4 w-4" />
            Back to Stock Screener
          </Link>

          <div className="flex items-start justify-between">
            <div>
              <div className="flex items-center gap-4 mb-2">
                <h1 className="text-3xl font-bold text-foreground">
                  {stock.symbol}
                  {stock.name && (
                    <span className="text-xl font-normal text-muted-foreground ml-3">
                      - {stock.name}
                    </span>
                  )}
                </h1>
                <HealthIndicator />
              </div>
              <div className="flex items-center gap-4 text-muted-foreground">
                <div className="flex items-center gap-2">
                  <Building2 className="h-4 w-4" />
                  <span>{stock.industry || "N/A"}</span>
                </div>
                {stock.website && (
                  <a
                    href={stock.website}
                    target="_blank"
                    rel="noopener noreferrer"
                    className="flex items-center gap-2 text-blue-600 hover:text-blue-700 transition-colors"
                  >
                    <Globe className="h-4 w-4" />
                    <span>Website</span>
                    <ExternalLink className="h-3 w-3" />
                  </a>
                )}
                {stock.last_fetched && (
                  <div className="flex items-center gap-2">
                    <span className="text-xs">
                      Data fetched:{" "}
                      {new Date(stock.last_fetched).toLocaleString()}
                    </span>
                  </div>
                )}
              </div>
            </div>

            <div className="text-right">
              <div className="text-2xl font-bold text-foreground">
                ${stock.price?.toFixed(2)}
              </div>
              <div className="text-sm text-muted-foreground">Current Price</div>
            </div>
          </div>
        </div>

        {/* Company Description */}
        {stock.summary && (
          <Card className="mb-6">
            <CardHeader>
              <CardTitle className="flex items-center gap-2">
                <BarChart3 className="h-5 w-5" />
                Company Overview
              </CardTitle>
            </CardHeader>
            <CardContent>
              <p className="text-muted-foreground leading-relaxed">
                {stock.summary}
              </p>
            </CardContent>
          </Card>
        )}

        {/* Financial Metrics Grid */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6 mb-6">
          <Card>
            <CardHeader className="pb-3">
              <CardTitle className="text-sm font-medium text-muted-foreground">
                P/E Ratio
              </CardTitle>
            </CardHeader>
            <CardContent>
              <div className="text-2xl font-bold">
                {stock.pe_ratio ? stock.pe_ratio.toFixed(2) : "--"}
              </div>
            </CardContent>
          </Card>

          <Card>
            <CardHeader className="pb-3">
              <CardTitle className="text-sm font-medium text-muted-foreground">
                P/S Ratio
              </CardTitle>
            </CardHeader>
            <CardContent>
              <div className="text-2xl font-bold">
                {stock.ps_ratio ? stock.ps_ratio.toFixed(2) : "--"}
              </div>
            </CardContent>
          </Card>

          <Card>
            <CardHeader className="pb-3">
              <CardTitle className="text-sm font-medium text-muted-foreground">
                P/B Ratio
              </CardTitle>
            </CardHeader>
            <CardContent>
              <div className="text-2xl font-bold">
                {stock.pb_ratio ? stock.pb_ratio.toFixed(2) : "--"}
              </div>
            </CardContent>
          </Card>

          <Card>
            <CardHeader className="pb-3">
              <CardTitle className="text-sm font-medium text-muted-foreground">
                PEG Ratio
              </CardTitle>
            </CardHeader>
            <CardContent>
              <div className="text-2xl font-bold">
                {stock.peg_ratio ? stock.peg_ratio.toFixed(2) : "--"}
              </div>
            </CardContent>
          </Card>

          <Card>
            <CardHeader className="pb-3">
              <CardTitle className="text-sm font-medium text-muted-foreground">
                Revenue Growth (yoy)
              </CardTitle>
            </CardHeader>
            <CardContent>
              <div
                className={`text-2xl font-bold ${
                  stock.revenue_growth > 0
                    ? "text-green-600"
                    : stock.revenue_growth < 0
                    ? "text-red-600"
                    : "text-foreground"
                }`}
              >
                {stock.revenue_growth
                  ? (stock.revenue_growth * 100).toFixed(1) + "%"
                  : "--"}
              </div>
            </CardContent>
          </Card>

          <Card>
            <CardHeader className="pb-3">
              <CardTitle className="text-sm font-medium text-muted-foreground">
                Revenue Growth (3yr)
              </CardTitle>
            </CardHeader>
            <CardContent>
              <div
                className={`text-2xl font-bold ${
                  stock.revenue_growth_3yr && stock.revenue_growth_3yr > 0
                    ? "text-green-600"
                    : stock.revenue_growth_3yr && stock.revenue_growth_3yr < 0
                    ? "text-red-600"
                    : "text-foreground"
                }`}
              >
                {stock.revenue_growth_3yr
                  ? (stock.revenue_growth_3yr * 100).toFixed(1) + "%"
                  : "--"}
              </div>
            </CardContent>
          </Card>

          <Card>
            <CardHeader className="pb-3">
              <CardTitle className="text-sm font-medium text-muted-foreground">
                Earnings Growth (yoy)
              </CardTitle>
            </CardHeader>
            <CardContent>
              <div
                className={`text-2xl font-bold ${
                  stock.earnings_growth > 0
                    ? "text-green-600"
                    : stock.earnings_growth < 0
                    ? "text-red-600"
                    : "text-foreground"
                }`}
              >
                {stock.earnings_growth
                  ? (stock.earnings_growth * 100).toFixed(1) + "%"
                  : "--"}
              </div>
            </CardContent>
          </Card>

          <Card>
            <CardHeader className="pb-3">
              <CardTitle className="text-sm font-medium text-muted-foreground">
                D/E Ratio
              </CardTitle>
            </CardHeader>
            <CardContent>
              <div className="text-2xl font-bold">
                {stock.de_ratio?.toFixed(2) ? stock.de_ratio.toFixed(2) : "--"}
              </div>
            </CardContent>
          </Card>

          <Card>
            <CardHeader className="pb-3">
              <CardTitle className="text-sm font-medium text-muted-foreground">
                ROE
              </CardTitle>
            </CardHeader>
            <CardContent>
              <div className="text-2xl font-bold">
                {stock.roe ? (stock.roe * 100).toFixed(1) + "%" : "--"}
              </div>
            </CardContent>
          </Card>

          <Card>
            <CardHeader className="pb-3">
              <CardTitle className="text-sm font-medium text-muted-foreground">
                Free Cash Flow
              </CardTitle>
            </CardHeader>
            <CardContent>
              <div className="text-2xl font-bold">
                {stock.free_cash_flow ? (
                  <span className="font-semibold">
                    ${(stock.free_cash_flow / 1000000000).toFixed(1)}B
                  </span>
                ) : (
                  "--"
                )}
              </div>
            </CardContent>
          </Card>

          <Card>
            <CardHeader className="pb-3">
              <CardTitle className="text-sm font-medium text-muted-foreground">
                Dividend Yield
              </CardTitle>
            </CardHeader>
            <CardContent>
              <div className="text-2xl font-bold">
                {stock.dividend_yield ? (
                  <span className="font-semibold text-green-600">
                    {stock.dividend_yield.toFixed(2)}%
                  </span>
                ) : (
                  "--"
                )}
              </div>
            </CardContent>
          </Card>
        </div>

        {/* Investment Scores */}
        <Card className="mb-6">
          <CardHeader>
            <CardTitle>Investment Scores</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="grid grid-cols-2 md:grid-cols-5 gap-4">
              <div className="text-center">
                <div className="text-sm text-muted-foreground mb-2">
                  Balanced
                </div>
                <Badge
                  variant="outline"
                  className={`text-lg font-bold ${
                    stock.balanced_score >= 80
                      ? "bg-green-100 text-green-800 border-green-200"
                      : stock.balanced_score >= 60
                      ? "bg-blue-100 text-blue-800 border-blue-200"
                      : stock.balanced_score >= 40
                      ? "bg-yellow-100 text-yellow-800 border-yellow-200"
                      : "bg-red-100 text-red-800 border-red-200"
                  }`}
                >
                  {stock.balanced_score}
                </Badge>
              </div>

              <div className="text-center">
                <div className="text-sm text-muted-foreground mb-2">Value</div>
                <Badge
                  variant="outline"
                  className={`text-lg font-bold ${
                    stock.value_score >= 80
                      ? "bg-green-100 text-green-800 border-green-200"
                      : stock.value_score >= 60
                      ? "bg-blue-100 text-blue-800 border-blue-200"
                      : stock.value_score >= 40
                      ? "bg-yellow-100 text-yellow-800 border-yellow-200"
                      : "bg-red-100 text-red-800 border-red-200"
                  }`}
                >
                  {stock.value_score}
                </Badge>
              </div>

              <div className="text-center">
                <div className="text-sm text-muted-foreground mb-2">Growth</div>
                <Badge
                  variant="outline"
                  className={`text-lg font-bold ${
                    stock.growth_score >= 80
                      ? "bg-green-100 text-green-800 border-green-200"
                      : stock.growth_score >= 60
                      ? "bg-blue-100 text-blue-800 border-blue-200"
                      : stock.growth_score >= 40
                      ? "bg-yellow-100 text-yellow-800 border-yellow-200"
                      : "bg-red-100 text-red-800 border-red-200"
                  }`}
                >
                  {stock.growth_score}
                </Badge>
              </div>

              <div className="text-center">
                <div className="text-sm text-muted-foreground mb-2">
                  Momentum
                </div>
                <Badge
                  variant="outline"
                  className={`text-lg font-bold ${
                    stock.momentum_score >= 80
                      ? "bg-green-100 text-green-800 border-green-200"
                      : stock.momentum_score >= 60
                      ? "bg-blue-100 text-blue-800 border-blue-200"
                      : stock.momentum_score >= 40
                      ? "bg-yellow-100 text-yellow-800 border-yellow-200"
                      : "bg-red-100 text-red-800 border-red-200"
                  }`}
                >
                  {stock.momentum_score}
                </Badge>
              </div>

              <div className="text-center">
                <div className="text-sm text-muted-foreground mb-2">
                  Quality
                </div>
                <Badge
                  variant="outline"
                  className={`text-lg font-bold ${
                    stock.quality_score >= 80
                      ? "bg-green-100 text-green-800 border-green-200"
                      : stock.quality_score >= 60
                      ? "bg-blue-100 text-blue-800 border-blue-200"
                      : stock.quality_score >= 40
                      ? "bg-yellow-100 text-yellow-800 border-yellow-200"
                      : "bg-red-100 text-red-800 border-red-200"
                  }`}
                >
                  {stock.quality_score}
                </Badge>
              </div>
            </div>
          </CardContent>
        </Card>

        {/* Analyst Rating */}
        {stock.average_analyst_rating && (
          <Card>
            <CardHeader>
              <CardTitle>Analyst Rating</CardTitle>
            </CardHeader>
            <CardContent>
              <Badge
                variant="outline"
                className={`text-lg px-4 py-2 ${getRatingColor(
                  stock.average_analyst_rating
                )}`}
              >
                {stock.average_analyst_rating}
              </Badge>
            </CardContent>
          </Card>
        )}
      </div>
    </div>
  );
}

export default CompanyProfile;
