import type { Metadata } from 'next';
import { Inter } from 'next/font/google';
import '../styles/globals.css';
import { AuthProvider } from '@/context/AuthContext';
import { UIProvider } from '@/context/UIContext';

const inter = Inter({ subsets: ['latin'] });

export const metadata: Metadata = {
  title: 'Math LMS - University Mathematics Learning',
  description: 'University Mathematics Learning Management System',
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="ja">
      <body className={inter.className}>
        <AuthProvider>
          <UIProvider>
            {children}
          </UIProvider>
        </AuthProvider>
      </body>
    </html>
  );
}