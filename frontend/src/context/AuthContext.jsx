import React, { createContext, useContext, useState, useEffect } from 'react';
import { authService } from '../services/api';

const AuthContext = createContext(null);

export const AuthProvider = ({ children }) => {
  const [user, setUser] = useState(null);
  const [token, setToken] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const initializeAuth = async () => {
      const storedToken = localStorage.getItem('agrisaathi_token');
      const storedUser = localStorage.getItem('agrisaathi_user');

      if (storedToken && storedUser) {
        setToken(storedToken);
        try {
          setUser(JSON.parse(storedUser));
          // Verify token validity with backend
          const freshUser = await authService.getMe();
          setUser(freshUser);
          localStorage.setItem('agrisaathi_user', JSON.stringify(freshUser));
        } catch (err) {
          console.warn('Session expired or invalid, logging out:', err.message);
          logout();
        }
      }
      setLoading(false);
    };

    initializeAuth();
  }, []);

  const login = async (email, password) => {
    const data = await authService.login({ email, password });
    setToken(data.access_token);
    setUser(data.user);
    localStorage.setItem('agrisaathi_token', data.access_token);
    localStorage.setItem('agrisaathi_user', JSON.stringify(data.user));
    return data.user;
  };

  const register = async (formData) => {
    const data = await authService.register(formData);
    setToken(data.access_token);
    setUser(data.user);
    localStorage.setItem('agrisaathi_token', data.access_token);
    localStorage.setItem('agrisaathi_user', JSON.stringify(data.user));
    return data.user;
  };

  const logout = () => {
    setToken(null);
    setUser(null);
    localStorage.removeItem('agrisaathi_token');
    localStorage.removeItem('agrisaathi_user');
  };

  return (
    <AuthContext.Provider
      value={{
        user,
        token,
        loading,
        isAuthenticated: !!token && !!user,
        login,
        register,
        logout,
      }}
    >
      {children}
    </AuthContext.Provider>
  );
};

export const useAuth = () => {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
};

