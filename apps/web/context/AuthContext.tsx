"use client";

import api from "@/lib/api";
import { AuthResponse, User } from "@/types";
import React, { createContext, useContext, useEffect, useState } from "react";
import { toast } from "sonner";

interface AuthContextType {
  user: User | null;
  loading: boolean;
  login: (email: string, password: string) => Promise<boolean>;
  register: (name: string, email: string, password: string) => Promise<boolean>;
  logout: () => void;
  updatePreferences: (preferences: any) => Promise<boolean>;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

export function AuthProvider({ children }: { children: React.ReactNode }) {
  const [user, setUser] = useState<User | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    checkAuth();
  }, []);

  const checkAuth = async () => {
    try {
      const token = localStorage.getItem("access_token");
      if (!token) {
        setLoading(false);
        return;
      }

      const response = await api.get("/auth/me");
      if (response.data.success) {
        setUser(response.data.user);
      }
    } catch (error) {
      localStorage.removeItem("access_token");
      localStorage.removeItem("refresh_token");
    } finally {
      setLoading(false);
    }
  };

  const login = async (email: string, password: string): Promise<boolean> => {
    try {
      const response = await api.post("/auth/login", { email, password });
      const data: AuthResponse = response.data;

      if (data.success && data.access_token && data.refresh_token) {
        localStorage.setItem("access_token", data.access_token);
        localStorage.setItem("refresh_token", data.refresh_token);
        setUser(data.user!);
        toast("Вход выполнен успешно!");
        return true;
      } else {
        toast.error(data.message || "Ошибка входа");
        return false;
      }
    } catch (error: any) {
      toast.error(error.response?.data?.message || "Login failed");
      return false;
    }
  };

  const register = async (
    name: string,
    email: string,
    password: string
  ): Promise<boolean> => {
    try {
      const response = await api.post("/auth/register", {
        name,
        email,
        password,
      });
      const data: AuthResponse = response.data;

      if (data.success && data.access_token && data.refresh_token) {
        localStorage.setItem("access_token", data.access_token);
        localStorage.setItem("refresh_token", data.refresh_token);
        setUser(data.user!);
        toast("Регистрация прошла успешно!");
        return true;
      } else {
        toast.error(data.message || "Ошибка регистрации");
        return false;
      }
    } catch (error: any) {
      toast.error(error.response?.data?.message || "Registration failed");
      return false;
    }
  };

  const logout = () => {
    localStorage.removeItem("access_token");
    localStorage.removeItem("refresh_token");
    setUser(null);
    toast("Вы успешно вышли из системы");
  };

  const updatePreferences = async (preferences: any): Promise<boolean> => {
    try {
      const response = await api.put("/auth/preferences", preferences);
      if (response.data.success) {
        setUser(response.data.user);
        toast("Предпочтения успешно обновлены!");
        return true;
      } else {
        toast.error(response.data.message || "Не удалось обновить предпочтения");
        return false;
      }
    } catch (error: any) {
      toast.error(
        error.response?.data?.message || "Failed to update preferences"
      );
      return false;
    }
  };

  return (
    <AuthContext.Provider
      value={{
        user,
        loading,
        login,
        register,
        logout,
        updatePreferences,
      }}
    >
      {children}
    </AuthContext.Provider>
  );
}

export function useAuth() {
  const context = useContext(AuthContext);
  if (context === undefined) {
    throw new Error("useAuth must be used within an AuthProvider");
  }
  return context;
}
