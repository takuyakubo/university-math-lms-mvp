'use client';

import { useEffect, ReactNode } from 'react';
import { useRouter } from 'next/navigation';
import { useAuth } from '@/context/AuthContext';

type RequireAuthProps = {
  children: ReactNode;
};

// 認証済みユーザー用ページ向けのコンポーネント
// 未認証ユーザーはログインページにリダイレクト
export default function RequireAuth({ children }: RequireAuthProps) {
  const { isAuthenticated, isLoading } = useAuth();
  const router = useRouter();

  useEffect(() => {
    if (!isLoading && !isAuthenticated) {
      router.push('/login');
    }
  }, [isAuthenticated, isLoading, router]);

  // ローディング中または未認証の場合はローディング表示
  if (isLoading || !isAuthenticated) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-gray-50">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-800" />
      </div>
    );
  }

  // 認証済みならchildrenを表示
  return <>{children}</>;
}