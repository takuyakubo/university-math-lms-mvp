'use client';

import { useEffect, ReactNode } from 'react';
import { useRouter } from 'next/navigation';
import { useAuth } from '@/context/AuthContext';

type AuthRedirectProps = {
  children: ReactNode;
};

// 未認証ユーザー用ページ（ログイン、登録）向けのコンポーネント
// 認証済みユーザーはダッシュボードにリダイレクト
export default function AuthRedirect({ children }: AuthRedirectProps) {
  const { isAuthenticated, isLoading } = useAuth();
  const router = useRouter();

  useEffect(() => {
    if (isAuthenticated && !isLoading) {
      router.push('/dashboard');
    }
  }, [isAuthenticated, isLoading, router]);

  // ローディング中は何も表示しない
  if (isLoading) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-gray-50">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-800" />
      </div>
    );
  }

  // 未認証ならchildren（ログインフォームなど）を表示
  return !isAuthenticated ? <>{children}</> : null;
}