'use client';

import React, { createContext, useContext, useState, ReactNode } from 'react';

// UIコンテキストの型定義
type UIContextType = {
  isSidebarOpen: boolean;
  toggleSidebar: () => void;
  closeSidebar: () => void;
  alert: {
    show: boolean;
    message: string;
    type: 'success' | 'error' | 'info' | 'warning';
  };
  showAlert: (message: string, type: 'success' | 'error' | 'info' | 'warning') => void;
  hideAlert: () => void;
};

// デフォルト値を持つコンテキスト作成
const UIContext = createContext<UIContextType>({
  isSidebarOpen: false,
  toggleSidebar: () => {},
  closeSidebar: () => {},
  alert: {
    show: false,
    message: '',
    type: 'info',
  },
  showAlert: () => {},
  hideAlert: () => {},
});

// カスタムフックの作成
export const useUI = () => useContext(UIContext);

type UIProviderProps = {
  children: ReactNode;
};

export const UIProvider = ({ children }: UIProviderProps) => {
  const [isSidebarOpen, setIsSidebarOpen] = useState(false);
  const [alert, setAlert] = useState({
    show: false,
    message: '',
    type: 'info' as 'success' | 'error' | 'info' | 'warning',
  });

  // サイドバー開閉のトグル
  const toggleSidebar = () => {
    setIsSidebarOpen(!isSidebarOpen);
  };

  // サイドバーを閉じる
  const closeSidebar = () => {
    setIsSidebarOpen(false);
  };

  // アラートを表示
  const showAlert = (message: string, type: 'success' | 'error' | 'info' | 'warning') => {
    setAlert({ show: true, message, type });
    
    // 5秒後に自動的に非表示
    setTimeout(() => {
      hideAlert();
    }, 5000);
  };

  // アラートを非表示
  const hideAlert = () => {
    setAlert({ ...alert, show: false });
  };

  return (
    <UIContext.Provider
      value={{
        isSidebarOpen,
        toggleSidebar,
        closeSidebar,
        alert,
        showAlert,
        hideAlert,
      }}
    >
      {children}
    </UIContext.Provider>
  );
};

export default UIContext;