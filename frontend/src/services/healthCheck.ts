// Health check service for monitoring backend status
export interface HealthStatus {
  status: "ok" | "error" | "checking";
  lastCheck: string;
  isOnline: boolean;
  errorMessage?: string;
}

class HealthCheckService {
  private intervalId: number | null = null;
  private checkInterval: number = 30000; // 30 seconds
  private apiUrl: string;
  private callbacks: ((status: HealthStatus) => void)[] = [];

  constructor() {
    this.apiUrl =
      import.meta.env.VITE_BACKEND_PRODUCTION_URL ||
      import.meta.env.VITE_BACKEND_LOCAL_URL;
  }

  // Start health checking
  start() {
    if (this.intervalId) {
      this.stop();
    }

    // Initial check
    this.checkHealth();

    // Set up interval
    this.intervalId = setInterval(() => {
      this.checkHealth();
    }, this.checkInterval);

    console.log(
      `🏥 Health check started - checking every ${this.checkInterval / 1000}s`
    );
  }

  // Stop health checking
  stop() {
    if (this.intervalId) {
      clearInterval(this.intervalId);
      this.intervalId = null;
      console.log("🏥 Health check stopped");
    }
  }

  // Set check interval (in milliseconds)
  setInterval(interval: number) {
    this.checkInterval = interval;
    if (this.intervalId) {
      this.stop();
      this.start();
    }
  }

  // Add callback for health status updates
  onStatusChange(callback: (status: HealthStatus) => void) {
    this.callbacks.push(callback);
  }

  // Remove callback
  removeCallback(callback: (status: HealthStatus) => void) {
    this.callbacks = this.callbacks.filter((cb) => cb !== callback);
  }

  // Perform health check
  private async checkHealth() {
    const status: HealthStatus = {
      status: "checking",
      lastCheck: new Date().toISOString(),
      isOnline: false,
    };

    try {
      const response = await fetch(`${this.apiUrl}/health`, {
        method: "GET",
        headers: {
          "Content-Type": "application/json",
        },
        // Add timeout
        signal: AbortSignal.timeout(10000), // 10 second timeout
      });

      if (response.ok) {
        status.status = "ok";
        status.isOnline = true;
        console.log(
          `✅ Health check passed at ${new Date().toLocaleTimeString()}`
        );
      } else {
        status.status = "error";
        status.isOnline = false;
        status.errorMessage = `HTTP ${response.status}: ${response.statusText}`;
        console.warn(`❌ Health check failed: ${status.errorMessage}`);
      }
    } catch (error) {
      status.status = "error";
      status.isOnline = false;
      status.errorMessage =
        error instanceof Error ? error.message : "Unknown error";
      console.error(`❌ Health check error: ${status.errorMessage}`);
    }

    // Notify all callbacks
    this.callbacks.forEach((callback) => callback(status));
  }

  // Manual health check
  async checkHealthOnce(): Promise<HealthStatus> {
    return new Promise((resolve) => {
      const callback = (status: HealthStatus) => {
        this.removeCallback(callback);
        resolve(status);
      };
      this.onStatusChange(callback);
      this.checkHealth();
    });
  }
}

// Export singleton instance
export const healthCheckService = new HealthCheckService();
