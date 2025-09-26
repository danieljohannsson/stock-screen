import { useState, useEffect } from "react";
import { Badge } from "@/components/ui/badge";
import { Wifi, WifiOff, Clock, AlertCircle } from "lucide-react";
import { healthCheckService, type HealthStatus } from "@/services/healthCheck";

interface HealthIndicatorProps {
  showDetails?: boolean;
  className?: string;
}

export function HealthIndicator({
  showDetails = false,
  className = "",
}: HealthIndicatorProps) {
  const [healthStatus, setHealthStatus] = useState<HealthStatus>({
    status: "checking",
    lastCheck: new Date().toISOString(),
    isOnline: false,
  });

  useEffect(() => {
    // Subscribe to health status updates
    const handleStatusChange = (status: HealthStatus) => {
      setHealthStatus(status);
    };

    healthCheckService.onStatusChange(handleStatusChange);

    // Start health checking
    healthCheckService.start();

    // Cleanup on unmount
    return () => {
      healthCheckService.removeCallback(handleStatusChange);
    };
  }, []);

  const getStatusIcon = () => {
    switch (healthStatus.status) {
      case "ok":
        return <Wifi className="h-3 w-3" />;
      case "error":
        return <WifiOff className="h-3 w-3" />;
      case "checking":
        return <Clock className="h-3 w-3 animate-spin" />;
      default:
        return <AlertCircle className="h-3 w-3" />;
    }
  };

  const getStatusColor = () => {
    switch (healthStatus.status) {
      case "ok":
        return "bg-green-100 text-green-800 border-green-200";
      case "error":
        return "bg-red-100 text-red-800 border-red-200";
      case "checking":
        return "bg-yellow-100 text-yellow-800 border-yellow-200";
      default:
        return "bg-gray-100 text-gray-800 border-gray-200";
    }
  };

  const getStatusText = () => {
    switch (healthStatus.status) {
      case "ok":
        return "Online";
      case "error":
        return "Offline";
      case "checking":
        return "Checking...";
      default:
        return "Unknown";
    }
  };

  const formatLastCheck = (isoString: string) => {
    const date = new Date(isoString);
    return date.toLocaleTimeString();
  };

  if (showDetails) {
    return (
      <div className={`flex items-center gap-2 ${className}`}>
        <Badge variant="outline" className={`${getStatusColor()} text-xs`}>
          {getStatusIcon()}
          <span className="ml-1">{getStatusText()}</span>
        </Badge>
        <div className="text-xs text-muted-foreground">
          Last check: {formatLastCheck(healthStatus.lastCheck)}
        </div>
        {healthStatus.errorMessage && (
          <div
            className="text-xs text-red-600"
            title={healthStatus.errorMessage}
          >
            Error: {healthStatus.errorMessage}
          </div>
        )}
      </div>
    );
  }

  return (
    <Badge
      variant="outline"
      className={`${getStatusColor()} text-xs ${className}`}
    >
      {getStatusIcon()}
      <span className="ml-1">{getStatusText()}</span>
    </Badge>
  );
}

export default HealthIndicator;
