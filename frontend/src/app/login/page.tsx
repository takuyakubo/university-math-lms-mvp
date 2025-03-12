import { Metadata } from 'next';
import LoginForm from '@/components/auth/LoginForm';
import AuthRedirect from '@/components/auth/AuthRedirect';

export const metadata: Metadata = {
  title: 'ログイン - Math LMS',
  description: '数学学習管理システムへのログインページです',
};

export default function LoginPage() {
  return (
    <>
      <AuthRedirect>
        <div className="min-h-screen flex items-center justify-center bg-gray-50 py-12 px-4 sm:px-6 lg:px-8">
          <div className="max-w-md w-full space-y-8">
            <div className="text-center">
              <h1 className="text-3xl font-extrabold text-gray-900 mb-2">Math LMS</h1>
              <p className="text-gray-600">
                大学数学のための学習管理システム
              </p>
            </div>
            
            <LoginForm />
          </div>
        </div>
      </AuthRedirect>
    </>
  );
}