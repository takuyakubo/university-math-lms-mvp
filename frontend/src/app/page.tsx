import Link from 'next/link';
import { FaChalkboardTeacher, FaGraduationCap, FaChartLine } from 'react-icons/fa';
import MathRenderer from '@/components/math/MathRenderer';

export default function HomePage() {
  return (
    <div className="min-h-screen bg-gray-50">
      {/* ヘッダー */}
      <header className="bg-blue-800 text-white shadow-md">
        <div className="container mx-auto px-4 py-4 flex justify-between items-center">
          <h1 className="text-2xl font-bold">Math LMS</h1>
          <nav className="space-x-6">
            <Link href="/login" className="hover:text-blue-200">
              ログイン
            </Link>
            <Link
              href="/register"
              className="bg-white text-blue-800 px-4 py-2 rounded-md hover:bg-blue-100"
            >
              新規登録
            </Link>
          </nav>
        </div>
      </header>

      {/* ヒーローセクション */}
      <section className="py-20 bg-gradient-to-b from-blue-900 to-blue-700 text-white">
        <div className="container mx-auto px-4 text-center">
          <h2 className="text-4xl md:text-5xl font-bold mb-6">
            大学レベルの数学学習を、もっと効果的に
          </h2>
          <p className="text-xl mb-10 max-w-3xl mx-auto">
            Math LMSは、大学1-2年生レベルの数学学習に特化した学習管理システムです。
            インタラクティブな問題と詳細な解説で、数学の理解を深めます。
          </p>
          <div className="flex flex-col sm:flex-row justify-center gap-4">
            <Link
              href="/register"
              className="bg-white text-blue-800 hover:bg-gray-100 px-8 py-3 rounded-md font-medium text-lg transition"
            >
              無料で始める
            </Link>
            <Link
              href="/login"
              className="bg-transparent hover:bg-blue-800 text-white border border-white px-8 py-3 rounded-md font-medium text-lg transition"
            >
              ログイン
            </Link>
          </div>
          
          {/* 数式サンプル */}
          <div className="mt-16 bg-white text-black p-6 rounded-lg shadow-lg max-w-xl mx-auto">
            <MathRenderer
              block
              latex="\int_{a}^{b} f(x) \, dx = F(b) - F(a)"
            />
            <p className="mt-4 text-gray-600">
              美しい数式を正確に表示し、わかりやすく解説します
            </p>
          </div>
        </div>
      </section>

      {/* 特徴セクション */}
      <section className="py-16 bg-white">
        <div className="container mx-auto px-4">
          <h2 className="text-3xl font-bold text-center mb-12">主な特徴</h2>
          
          <div className="grid grid-cols-1 md:grid-cols-3 gap-8 max-w-5xl mx-auto">
            <div className="bg-gray-50 rounded-lg shadow-md p-6 text-center">
              <div className="rounded-full bg-blue-100 p-4 w-16 h-16 flex items-center justify-center mx-auto mb-4">
                <FaChalkboardTeacher className="text-blue-600 text-2xl" />
              </div>
              <h3 className="text-xl font-semibold mb-3">インタラクティブな学習体験</h3>
              <p className="text-gray-600">
                LaTeX対応の数式エディタで、大学レベルの数学問題を解くことができます。
                選択式問題から始め、自動採点機能で即時フィードバックを得られます。
              </p>
            </div>
            
            <div className="bg-gray-50 rounded-lg shadow-md p-6 text-center">
              <div className="rounded-full bg-green-100 p-4 w-16 h-16 flex items-center justify-center mx-auto mb-4">
                <FaGraduationCap className="text-green-600 text-2xl" />
              </div>
              <h3 className="text-xl font-semibold mb-3">学習進捗の可視化</h3>
              <p className="text-gray-600">
                学習の進捗状況をリアルタイムで追跡し、強みと弱みを分析。
                ダッシュボードでは、完了した問題数、正答率、学習時間などを確認できます。
              </p>
            </div>
            
            <div className="bg-gray-50 rounded-lg shadow-md p-6 text-center">
              <div className="rounded-full bg-purple-100 p-4 w-16 h-16 flex items-center justify-center mx-auto mb-4">
                <FaChartLine className="text-purple-600 text-2xl" />
              </div>
              <h3 className="text-xl font-semibold mb-3">教員向け機能</h3>
              <p className="text-gray-600">
                教員は独自の問題セットを作成し、学生の進捗を確認できます。
                数式エディタを使用して、複雑な数学表現を含む問題を簡単に作成できます。
              </p>
            </div>
          </div>
        </div>
      </section>

      {/* フッター */}
      <footer className="bg-gray-800 text-white py-8">
        <div className="container mx-auto px-4">
          <div className="flex flex-col md:flex-row justify-between items-center">
            <div className="mb-4 md:mb-0">
              <p className="font-bold text-lg">Math LMS</p>
              <p className="text-gray-400 text-sm">© 2023 Math LMS. All rights reserved.</p>
            </div>
            <div className="flex space-x-6">
              <Link href="/about" className="text-gray-300 hover:text-white">
                About
              </Link>
              <Link href="/contact" className="text-gray-300 hover:text-white">
                Contact
              </Link>
              <Link href="/terms" className="text-gray-300 hover:text-white">
                Terms of Service
              </Link>
              <Link href="/privacy" className="text-gray-300 hover:text-white">
                Privacy Policy
              </Link>
            </div>
          </div>
        </div>
      </footer>
    </div>
  );
}