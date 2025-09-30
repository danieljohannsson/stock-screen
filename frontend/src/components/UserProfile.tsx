import React, { useState } from "react";
import { useAuth } from "@/contexts/AuthContext";
import { useNavigate } from "react-router-dom";
import { LogOut, Heart } from "lucide-react";

interface UserProfileProps {
  onClose?: () => void;
}

export const UserProfile: React.FC<UserProfileProps> = ({ onClose }) => {
  const { user, logout, favorites } = useAuth();
  const navigate = useNavigate();
  const [showFavorites, setShowFavorites] = useState(false);

  if (!user) return null;

  const getProviderIcon = () => {
    // Only Google is supported now
    return (
      <svg className="w-4 h-4" viewBox="0 0 24 24">
        <path
          fill="#4285F4"
          d="M22.56 12.25c0-.78-.07-1.53-.2-2.25H12v4.26h5.92c-.26 1.37-1.04 2.53-2.21 3.31v2.77h3.57c2.08-1.92 3.28-4.74 3.28-8.09z"
        />
        <path
          fill="#34A853"
          d="M12 23c2.97 0 5.46-.98 7.28-2.66l-3.57-2.77c-.98.66-2.23 1.06-3.71 1.06-2.86 0-5.29-1.93-6.16-4.53H2.18v2.84C3.99 20.53 7.7 23 12 23z"
        />
        <path
          fill="#FBBC05"
          d="M5.84 14.09c-.22-.66-.35-1.36-.35-2.09s.13-1.43.35-2.09V7.07H2.18C1.43 8.55 1 10.22 1 12s.43 3.45 1.18 4.93l2.85-2.22.81-.62z"
        />
        <path
          fill="#EA4335"
          d="M12 5.38c1.62 0 3.06.56 4.21 1.64l3.15-3.15C17.45 2.09 14.97 1 12 1 7.7 1 3.99 3.47 2.18 7.07l3.66 2.84c.87-2.6 3.3-4.53 6.16-4.53z"
        />
      </svg>
    );
  };

  const getProviderName = (provider: string) => {
    return provider.charAt(0).toUpperCase() + provider.slice(1);
  };

  return (
    <div className="bg-white rounded-lg shadow-lg p-6 w-80">
      {/* Header */}
      <div className="flex items-center justify-between mb-4">
        <h3 className="text-lg font-semibold text-gray-900">Profile</h3>
        {onClose && (
          <button
            onClick={onClose}
            className="text-gray-400 hover:text-gray-600 transition-colors"
          >
            ×
          </button>
        )}
      </div>

      {/* User Info */}
      <div className="flex items-center space-x-3 mb-6">
        {user.picture ? (
          <img
            src={user.picture}
            alt={user.name}
            className="w-12 h-12 rounded-full object-cover"
          />
        ) : (
          <div className="w-12 h-12 bg-gray-200 rounded-full flex items-center justify-center">
            <span className="text-gray-600 font-medium text-lg">
              {user.name.charAt(0).toUpperCase()}
            </span>
          </div>
        )}
        <div>
          <h4 className="font-medium text-gray-900">{user.name}</h4>
          <p className="text-sm text-gray-500">{user.email}</p>
        </div>
      </div>

      {/* Provider Info */}
      <div className="flex items-center space-x-2 mb-6 p-3 bg-gray-50 rounded-lg">
        {getProviderIcon()}
        <span className="text-sm text-gray-600">
          Signed in with {getProviderName(user.provider)}
        </span>
      </div>

      {/* Favorites Section */}
      <div className="mb-6">
        <button
          onClick={() => setShowFavorites(!showFavorites)}
          className="flex items-center space-x-2 text-gray-700 hover:text-gray-900 transition-colors"
        >
          <Heart className="w-4 h-4" />
          <span className="font-medium">Favorites ({favorites.length})</span>
        </button>

        {showFavorites && (
          <div className="mt-3 max-h-32 overflow-y-auto">
            {favorites.length > 0 ? (
              <div className="flex flex-wrap gap-2">
                {favorites.map((symbol) => (
                  <span
                    key={symbol}
                    className="px-2 py-1 bg-blue-100 text-blue-800 text-xs rounded-full"
                  >
                    {symbol}
                  </span>
                ))}
              </div>
            ) : (
              <p className="text-sm text-gray-500">No favorites yet</p>
            )}
          </div>
        )}
      </div>

      {/* Account Info */}
      <div className="mb-6 text-sm text-gray-500">
        <p>Member since {new Date(user.created_at).toLocaleDateString()}</p>
        {user.last_login && (
          <p>Last active {new Date(user.last_login).toLocaleDateString()}</p>
        )}
      </div>

      {/* Logout Button */}
      <button
        onClick={() => {
          onClose?.(); // Close the modal first
          logout(() => navigate("/"));
        }}
        className="w-full flex items-center justify-center space-x-2 px-4 py-2 bg-red-50 text-red-700 rounded-lg hover:bg-red-100 transition-colors"
      >
        <LogOut className="w-4 h-4" />
        <span>Sign Out</span>
      </button>
    </div>
  );
};
