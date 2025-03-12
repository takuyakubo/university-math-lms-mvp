'use client';

import React from 'react';
import Link from 'next/link';
import { usePathname } from 'next/navigation';
import { FaBars, FaSignOutAlt, FaUser } from 'react-icons/fa';
import { useAuth } from '@/context/AuthContext';
import { useUI } from '@/context/UIContext';

const Header: React.FC = () => {
  const { user, logout } = useAuth();
  const { toggleSidebar } = useUI();
  const pathname = usePathname();

  const handleLogout = () => {
    logout();
  };

  return (
    <header 
      className="bg-blue-800 text-white shadow-md sticky top-0 z-50" 
      data-testid="app-header"
    >
      <div className="container mx-auto px-4 py-3 flex justify-between items-center">
        <div className="flex items-center">
          <button
            className="mr-4 md:hidden text-white focus:outline-none"
            onClick={toggleSidebar}
            aria-label="Toggle menu"
          >
            <FaBars size={24} />
          </button>
          <Link href="/" className="text-xl font-bold">
            Math LMS
          </Link>
        </div>

        <nav className="hidden md:flex space-x-6">
          {user && (
            <>
              <Link 
                href="/dashboard" 
                className={`hover:text-blue-200 ${pathname === '/dashboard' ? 'border-b-2 border-white' : ''}`}
              >
                ダッシュボード
              </Link>
              <Link 
                href="/problems" 
                className={`hover:text-blue-200 ${pathname === '/problems' ? 'border-b-2 border-white' : ''}`}
              >
                問題一覧
              </Link>
              <Link 
                href="/progress" 
                className={`hover:text-blue-200 ${pathname === '/progress' ? 'border-b-2 border-white' : ''}`}
              >
                学習進捗
              </Link>
            </>
          )}
        </nav>

        <div className="flex items-center">
          {user ? (
            <div className="flex items-center space-x-4">
              <Link href="/profile" className="flex items-center hover:text-blue-200">
                <FaUser className="mr-2" />
                <span className="hidden sm:inline">{user.name}</span>
              </Link>
              <button
                onClick={handleLogout}
                className="flex items-center hover:text-blue-200"
                aria-label="Logout"
              >
                <FaSignOutAlt className="mr-2" />
                <span className="hidden sm:inline">ログアウト</span>
              </button>
            </div>
          ) : (
            <div className="space-x-4">
              <Link href="/login" className="hover:text-blue-200">
                ログイン
              </Link>
              <Link
                href="/register"
                className="bg-white text-blue-800 px-4 py-2 rounded-md hover:bg-blue-100"
              >
                新規登録
              </Link>
            </div>
          )}
        </div>
      </div>
    </header>
  );
};

export default Header;