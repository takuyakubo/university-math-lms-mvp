'use client';

import React, { ReactNode } from 'react';
import { useAuth } from '@/context/AuthContext';
import Header from './Header';
import Sidebar from './Sidebar';
import { useUI } from '@/context/UIContext';

type AppLayoutProps = {
  children: ReactNode;
};

const AppLayout: React.FC<AppLayoutProps> = ({ children }) => {
  const { isAuthenticated, isLoading } = useAuth();
  const { alert } = useUI();

  if (isLoading) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-gray-50">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-800" />
      </div>
    );
  }

  return (
    <div className="flex flex-col min-h-screen bg-gray-50">
      <Header />
      
      <div className="flex flex-1">
        {isAuthenticated && <Sidebar />}
        
        <main className={`flex-1 ${isAuthenticated ? 'md:ml-64' : ''} p-4 md:p-8 transition-all duration-300`}>
          {/* アラート表示 */}
          {alert.show && (
            <div 
              className={`mb-4 p-4 rounded shadow-md ${
                alert.type === 'success' 
                  ? 'bg-green-100 text-green-800 border-l-4 border-green-500' 
                  : alert.type === 'error' 
                  ? 'bg-red-100 text-red-800 border-l-4 border-red-500'
                  : alert.type === 'warning'
                  ? 'bg-yellow-100 text-yellow-800 border-l-4 border-yellow-500'
                  : 'bg-blue-100 text-blue-800 border-l-4 border-blue-500'
              }`}
              role="alert"
            >
              {alert.message}
            </div>
          )}
          
          {children}
        </main>
      </div>
    </div>
  );
};

export default AppLayout;