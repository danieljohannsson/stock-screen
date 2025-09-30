import React, {
  createContext,
  useContext,
  useState,
  useEffect,
  type ReactNode,
} from "react";

interface User {
  id: number;
  email: string;
  name: string;
  picture?: string;
  provider: string;
  created_at: string;
  last_login?: string;
}

interface AuthContextType {
  user: User | null;
  token: string | null;
  login: (provider: string, accessToken: string) => Promise<void>;
  logout: (onLogout?: () => void) => void;
  loading: boolean;
  isAuthenticated: boolean;
  addToFavorites: (stockSymbol: string) => Promise<void>;
  removeFromFavorites: (stockSymbol: string) => Promise<void>;
  favorites: string[];
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

interface AuthProviderProps {
  children: ReactNode;
}

export const AuthProvider: React.FC<AuthProviderProps> = ({ children }) => {
  const [user, setUser] = useState<User | null>(null);
  const [token, setToken] = useState<string | null>(null);
  const [loading, setLoading] = useState(true);
  const [favorites, setFavorites] = useState<string[]>([]);

  const API_BASE_URL =
    import.meta.env.VITE_BACKEND_PRODUCTION_URL ||
    import.meta.env.VITE_BACKEND_LOCAL_URL;

  // Check for existing token on mount
  useEffect(() => {
    const savedToken = localStorage.getItem("auth_token");
    if (savedToken) {
      setToken(savedToken);
      fetchUserProfile(savedToken);
    } else {
      setLoading(false);
    }
  }, []);

  // Fetch user profile when token changes
  useEffect(() => {
    if (token) {
      fetchUserProfile(token);
      fetchFavorites(token);
    } else {
      setUser(null);
      setFavorites([]);
    }
  }, [token]);

  const fetchUserProfile = async (authToken: string) => {
    try {
      const response = await fetch(`${API_BASE_URL}/auth/me`, {
        headers: {
          Authorization: `Bearer ${authToken}`,
          "Content-Type": "application/json",
        },
      });

      if (response.ok) {
        const userData = await response.json();
        setUser(userData);
      } else {
        // Token is invalid, clear it
        localStorage.removeItem("auth_token");
        setToken(null);
      }
    } catch (error) {
      console.error("Error fetching user profile:", error);
      localStorage.removeItem("auth_token");
      setToken(null);
    } finally {
      setLoading(false);
    }
  };

  const fetchFavorites = async (authToken: string) => {
    try {
      const response = await fetch(`${API_BASE_URL}/auth/favorites`, {
        headers: {
          Authorization: `Bearer ${authToken}`,
          "Content-Type": "application/json",
        },
      });

      if (response.ok) {
        const favoritesData = await response.json();
        setFavorites(favoritesData.map((fav: any) => fav.stock_symbol));
      }
    } catch (error) {
      console.error("Error fetching favorites:", error);
    }
  };

  const login = async (provider: string, accessToken: string) => {
    try {
      setLoading(true);
      const response = await fetch(`${API_BASE_URL}/auth/${provider}`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ access_token: accessToken }),
      });

      if (response.ok) {
        const data = await response.json();
        localStorage.setItem("auth_token", data.access_token);
        setToken(data.access_token);
        setUser(data.user);
        await fetchFavorites(data.access_token);
      } else {
        const errorData = await response.json();
        throw new Error(errorData.detail || "Login failed");
      }
    } catch (error) {
      console.error("Login error:", error);
      throw error;
    } finally {
      setLoading(false);
    }
  };

  const logout = (onLogout?: () => void) => {
    localStorage.removeItem("auth_token");
    setToken(null);
    setUser(null);
    setFavorites([]);
    onLogout?.();
  };

  const addToFavorites = async (stockSymbol: string) => {
    if (!token) return;

    try {
      const response = await fetch(`${API_BASE_URL}/auth/favorites`, {
        method: "POST",
        headers: {
          Authorization: `Bearer ${token}`,
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ stock_symbol: stockSymbol }),
      });

      if (response.ok) {
        setFavorites((prev) => [...prev, stockSymbol]);
      } else {
        throw new Error("Failed to add to favorites");
      }
    } catch (error) {
      console.error("Error adding to favorites:", error);
      throw error;
    }
  };

  const removeFromFavorites = async (stockSymbol: string) => {
    if (!token) return;

    try {
      const response = await fetch(
        `${API_BASE_URL}/auth/favorites/${stockSymbol}`,
        {
          method: "DELETE",
          headers: {
            Authorization: `Bearer ${token}`,
          },
        }
      );

      if (response.ok) {
        setFavorites((prev) => prev.filter((symbol) => symbol !== stockSymbol));
      } else {
        throw new Error("Failed to remove from favorites");
      }
    } catch (error) {
      console.error("Error removing from favorites:", error);
      throw error;
    }
  };

  const value: AuthContextType = {
    user,
    token,
    login,
    logout,
    loading,
    isAuthenticated: !!user && !!token,
    addToFavorites,
    removeFromFavorites,
    favorites,
  };

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
};

export const useAuth = () => {
  const context = useContext(AuthContext);
  if (context === undefined) {
    throw new Error("useAuth must be used within an AuthProvider");
  }
  return context;
};
