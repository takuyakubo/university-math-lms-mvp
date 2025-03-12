'use client';

import React, { createContext, useContext, useState, useEffect, ReactNode } from 'react';
import axios from 'axios';
import { useRouter } from 'next/navigation';

// APIのベースURLを設定
axios.defaults.baseURL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

// ユーザータイプの定義
type User = {
  id: string;
  name: string;
  email: string;
  role: 'student' | 'teacher' | 'admin';
};

// 認証コンテキストの型定義
type AuthContextType = {
  user: User | null;
  isAuthenticated: boolean;
  isLoading: boolean;
  login: (email: string, password: string) => Promise<void>;
  register: (name: string, email: string, password: string, role: 'student' | 'teacher') => Promise<void>;
  logout: () => void;
  error: string | null;
};

// デフォルト値を持つコンテキスト作成
const AuthContext = createContext<AuthContextType>({
  user: null,
  isAuthenticated: false,
  isLoading: true,
  login: async () => {},
  register: async () => {},
  logout: () => {},
  error: null,
});

// カスタムフックの作成
export const useAuth = () => useContext(AuthContext);

type AuthProviderProps = {
  children: ReactNode;
};

export const AuthProvider = ({ children }: AuthProviderProps) => {
  const [user, setUser] = useState<User | null>(null);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const router = useRouter();

  // トークンの検証と、ユーザー情報の取得
  useEffect(() => {
    const validateToken = async () => {
      if (typeof window === 'undefined') return;
      
      const token = localStorage.getItem('token');
      
      if (!token) {
        setIsLoading(false);
        return;
      }
      
      try {
        // APIエンドポイントはバックエンドの実装に合わせて変更
        const response = await axios.get('/api/v1/auth/me', {
          headers: {
            Authorization: `Bearer ${token}`
          }
        });
        
        setUser(response.data);
        setIsLoading(false);
      } catch (err) {
        console.error('Token validation error:', err);
        localStorage.removeItem('token');
        setUser(null);
        setIsLoading(false);
      }
    };
    
    validateToken();
  }, []);

  // ログイン関数
  const login = async (email: string, password: string) => {
    setError(null);
    try {
      // APIエンドポイントはバックエンドの実装に合わせて変更
      const response = await axios.post('/api/v1/auth/login', {
        email,
        password
      });
      
      const { token, user } = response.data;
      localStorage.setItem('token', token);
      setUser(user);
      router.push('/dashboard');
    } catch (err: any) {
      setError(
        err.response?.data?.message || 
        'ログインに失敗しました。メールアドレスとパスワードを確認してください。'
      );
      throw err;
    }
  };

  // 登録関数
  const register = async (name: string, email: string, password: string, role: 'student' | 'teacher') => {
    setError(null);
    try {
      // APIエンドポイントはバックエンドの実装に合わせて変更
      const response = await axios.post('/api/v1/auth/register', {
        name,
        email,
        password,
        role
      });
      
      const { token, user } = response.data;
      localStorage.setItem('token', token);
      setUser(user);
      router.push('/dashboard');
    } catch (err: any) {
      setError(
        err.response?.data?.message || 
        '登録に失敗しました。入力内容を確認するか、別のメールアドレスを試してください。'
      );
      throw err;
    }
  };

  // ログアウト関数
  const logout = () => {
    localStorage.removeItem('token');
    setUser(null);
    router.push('/login');
  };

  return (
    <AuthContext.Provider 
      value={{ 
        user, 
        isAuthenticated: !!user, 
        isLoading, 
        login, 
        register, 
        logout, 
        error 
      }}
    >
      {children}
    </AuthContext.Provider>
  );
};

export default AuthContext;