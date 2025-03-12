'use client';

import React, { useState } from 'react';
import { useForm } from 'react-hook-form';
import { FaEnvelope, FaLock } from 'react-icons/fa';
import Link from 'next/link';
import { useAuth } from '@/context/AuthContext';
import { useUI } from '@/context/UIContext';
import Input from '../ui/Input';
import Button from '../ui/Button';

type LoginFormData = {
  email: string;
  password: string;
};

const LoginForm: React.FC = () => {
  const { login } = useAuth();
  const { showAlert } = useUI();
  const [isSubmitting, setIsSubmitting] = useState(false);
  
  const {
    register,
    handleSubmit,
    formState: { errors },
  } = useForm<LoginFormData>();

  const onSubmit = async (data: LoginFormData) => {
    setIsSubmitting(true);
    
    try {
      await login(data.email, data.password);
      showAlert('ログインに成功しました。', 'success');
    } catch (error) {
      console.error('Login error:', error);
      showAlert('ログインに失敗しました。メールアドレスとパスワードを確認してください。', 'error');
    } finally {
      setIsSubmitting(false);
    }
  };

  return (
    <div className="bg-white p-8 rounded-lg shadow-md max-w-md w-full mx-auto">
      <h2 className="text-2xl font-bold text-center mb-6">ログイン</h2>
      
      <form onSubmit={handleSubmit(onSubmit)} className="space-y-6">
        <Input
          label="メールアドレス"
          type="email"
          leftIcon={<FaEnvelope className="text-gray-400" />}
          error={errors.email?.message}
          {...register('email', {
            required: 'メールアドレスを入力してください',
            pattern: {
              value: /^[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}$/i,
              message: '有効なメールアドレスを入力してください',
            },
          })}
        />
        
        <Input
          label="パスワード"
          type="password"
          leftIcon={<FaLock className="text-gray-400" />}
          error={errors.password?.message}
          {...register('password', {
            required: 'パスワードを入力してください',
            minLength: {
              value: 6,
              message: 'パスワードは6文字以上で入力してください',
            },
          })}
        />
        
        <div className="text-right">
          <Link href="/forgot-password" className="text-sm text-blue-600 hover:text-blue-800">
            パスワードをお忘れですか？
          </Link>
        </div>
        
        <Button
          type="submit"
          isLoading={isSubmitting}
          isFullWidth
          size="lg"
        >
          ログイン
        </Button>
      </form>
      
      <div className="mt-6 text-center text-sm">
        <p>
          アカウントをお持ちでない場合は{' '}
          <Link href="/register" className="text-blue-600 hover:text-blue-800 font-medium">
            新規登録
          </Link>
        </p>
      </div>
    </div>
  );
};

export default LoginForm;