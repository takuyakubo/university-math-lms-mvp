'use client';

import React from 'react';
import Link from 'next/link';
import { usePathname } from 'next/navigation';
import { 
  FaTachometerAlt, 
  FaBook, 
  FaChartLine, 
  FaUser, 
  FaCog,
  FaChalkboardTeacher,
  FaEdit
} from 'react-icons/fa';
import { useAuth } from '@/context/AuthContext';
import { useUI } from '@/context/UIContext';

const Sidebar: React.FC = () => {
  const { user } = useAuth();
  const { isSidebarOpen, closeSidebar } = useUI();
  const pathname = usePathname();

  // サイドバーリンクのアクティブ状態を確認
  const isActive = (path: string) => {
    return pathname === path;
  };

  // リンククリック時にモバイルでは自動的にサイドバーを閉じる
  const handleLinkClick = () => {
    if (typeof window !== 'undefined' && window.innerWidth < 768) {
      closeSidebar();
    }
  };

  // アクセス制御：教員向けリンク
  const isTeacher = user?.role === 'teacher' || user?.role === 'admin';

  if (!user) return null;

  return (
    <aside 
      data-testid="app-sidebar"
      className={`fixed left-0 top-0 z-40 h-screen w-64 bg-gray-800 text-white transition-transform ${
        isSidebarOpen ? 'translate-x-0' : '-translate-x-full'
      } md:translate-x-0 pt-20`}
    >
      <div className="px-3 py-4">
        <nav className="space-y-1">
          <Link
            href="/dashboard"
            className={`flex items-center px-4 py-3 rounded-md transition-colors ${
              isActive('/dashboard')
                ? 'bg-blue-700 text-white'
                : 'text-gray-300 hover:bg-gray-700'
            }`}
            onClick={handleLinkClick}
          >
            <FaTachometerAlt className="mr-3" />
            <span>ダッシュボード</span>
          </Link>

          <Link
            href="/problems"
            className={`flex items-center px-4 py-3 rounded-md transition-colors ${
              isActive('/problems')
                ? 'bg-blue-700 text-white'
                : 'text-gray-300 hover:bg-gray-700'
            }`}
            onClick={handleLinkClick}
          >
            <FaBook className="mr-3" />
            <span>問題一覧</span>
          </Link>

          <Link
            href="/progress"
            className={`flex items-center px-4 py-3 rounded-md transition-colors ${
              isActive('/progress')
                ? 'bg-blue-700 text-white'
                : 'text-gray-300 hover:bg-gray-700'
            }`}
            onClick={handleLinkClick}
          >
            <FaChartLine className="mr-3" />
            <span>学習進捗</span>
          </Link>

          {isTeacher && (
            <>
              <hr className="border-gray-600 my-3" />
              <h3 className="px-4 text-xs font-semibold text-gray-400 uppercase tracking-wider">
                教員メニュー
              </h3>

              <Link
                href="/problems/create"
                className={`flex items-center px-4 py-3 rounded-md transition-colors ${
                  isActive('/problems/create')
                    ? 'bg-blue-700 text-white'
                    : 'text-gray-300 hover:bg-gray-700'
                }`}
                onClick={handleLinkClick}
              >
                <FaEdit className="mr-3" />
                <span>問題作成</span>
              </Link>

              <Link
                href="/students"
                className={`flex items-center px-4 py-3 rounded-md transition-colors ${
                  isActive('/students')
                    ? 'bg-blue-700 text-white'
                    : 'text-gray-300 hover:bg-gray-700'
                }`}
                onClick={handleLinkClick}
              >
                <FaChalkboardTeacher className="mr-3" />
                <span>学生管理</span>
              </Link>
            </>
          )}

          <hr className="border-gray-600 my-3" />

          <Link
            href="/profile"
            className={`flex items-center px-4 py-3 rounded-md transition-colors ${
              isActive('/profile')
                ? 'bg-blue-700 text-white'
                : 'text-gray-300 hover:bg-gray-700'
            }`}
            onClick={handleLinkClick}
          >
            <FaUser className="mr-3" />
            <span>プロフィール</span>
          </Link>

          <Link
            href="/settings"
            className={`flex items-center px-4 py-3 rounded-md transition-colors ${
              isActive('/settings')
                ? 'bg-blue-700 text-white'
                : 'text-gray-300 hover:bg-gray-700'
            }`}
            onClick={handleLinkClick}
          >
            <FaCog className="mr-3" />
            <span>設定</span>
          </Link>
        </nav>
      </div>
    </aside>
  );
};

export default Sidebar;