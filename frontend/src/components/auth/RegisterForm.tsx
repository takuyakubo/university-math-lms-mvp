'use client';

import React, { useState } from 'react';
import { useForm } from 'react-hook-form';
import { FaUser, FaEnvelope, FaLock, FaUserGraduate } from 'react-icons/fa';
import Link from 'next/link';
import { useAuth } from '@/context/AuthContext';
import { useUI } from '@/context/UIContext';
import Input from '../ui/Input';
import Button from '../ui/Button';

type RegisterFormData = {
  name: string;
  email: string;
  password: string;
  confirmPassword: string;
  role: 'student' | 'teacher';
};

const RegisterForm: React.FC = () => {
  const { register: registerUser } = useAuth();
  const { showAlert } = useUI();
  const [isSubmitting, setIsSubmitting] = useState(false);
  
  const {
    register,
    handleSubmit,
    watch,
    formState: { errors },
  } = useForm<RegisterFormData>({
    defaultValues: {
      role: 'student'
    }
  });

  const password = watch('password');

  const onSubmit = async (data: RegisterFormData) => {
    setIsSubmitting(true);
    
    try {
      await registerUser(data.name, data.email, data.password, data.role);
      showAlert('アカウント登録に成功しました。', 'success');
    } catch (error) {
      console.error('Registration error:', error);
      showAlert('登録に失敗しました。入力内容を確認するか、別のメールアドレスを試してください。', 'error');
    } finally {
      setIsSubmitting(false);
    }
  };

  return (
    <div className="bg-white p-8 rounded-lg shadow-md max-w-md w-full mx-auto">
      <h2 className="text-2xl font-bold text-center mb-6">アカウント登録</h2>
      
      <form onSubmit={handleSubmit(onSubmit)} className="space-y-6">
        <Input
          label="氏名"
          leftIcon={<FaUser className="text-gray-400" />}
          error={errors.name?.message}
          {...register('name', {
            required: '氏名を入力してください',
            maxLength: {
              value: 50,
              message: '氏名は50文字以内で入力してください',
            },
          })}
        />
        
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
          helperText="6文字以上の英数字を使用してください"
          {...register('password', {
            required: 'パスワードを入力してください',
            minLength: {
              value: 6,
              message: 'パスワードは6文字以上で入力してください',
            },
          })}
        />
        
        <Input
          label="パスワード確認"
          type="password"
          leftIcon={<FaLock className="text-gray-400" />}
          error={errors.confirmPassword?.message}
          {...register('confirmPassword', {
            required: 'パスワードを再入力してください',
            validate: value => value === password || 'パスワードが一致しません',
          })}
        />
        
        <div className="space-y-2">
          <label className="block text-sm font-medium text-gray-700">
            ユーザータイプ
          </label>
          <div className="flex space-x-4">
            <label className="inline-flex items-center">
              <input
                type="radio"
                className="form-radio text-blue-600"
                value="student"
                {...register('role')}
              />
              <span className="ml-2">学生</span>
            </label>
            <label className="inline-flex items-center">
              <input
                type="radio"
                className="form-radio text-blue-600"
                value="teacher"
                {...register('role')}
              />
              <span className="ml-2">教員</span>
            </label>
          </div>
        </div>
        
        <Button
          type="submit"
          isLoading={isSubmitting}
          isFullWidth
          size="lg"
        >
          登録する
        </Button>
      </form>
      
      <div className="mt-6 text-center text-sm">
        <p>
          すでにアカウントをお持ちの場合は{' '}
          <Link href="/login" className="text-blue-600 hover:text-blue-800 font-medium">
            ログイン
          </Link>
        </p>
      </div>
    </div>
  );
};

export default RegisterForm;