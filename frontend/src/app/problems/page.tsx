import { Metadata } from 'next';
import Link from 'next/link';
import { FaFilter, FaSearch } from 'react-icons/fa';
import MathRenderer from '@/components/math/MathRenderer';

export const metadata: Metadata = {
  title: '問題一覧 - Math LMS',
  description: '大学レベルの数学問題を一覧で表示します',
};

// ダミーデータ（後でAPIから取得するように変更）
const dummyProblems = [
  {
    id: '1',
    title: '微分方程式の解法',
    category: '微分方程式',
    difficulty: '中級',
    description: '次の微分方程式を解け: \\frac{dy}{dx} + P(x)y = Q(x)',
    completed: true,
  },
  {
    id: '2',
    title: '三角関数の性質',
    category: '三角関数',
    difficulty: '初級',
    description: '\\sin^2 x + \\cos^2 x = 1 を証明せよ',
    completed: false,
  },
  {
    id: '3',
    title: '線形代数の基礎',
    category: '線形代数',
    difficulty: '初級',
    description: '行列 A = \\begin{pmatrix} 2 & 1 \\\\ 3 & 4 \\end{pmatrix} の固有値と固有ベクトルを求めよ',
    completed: false,
  },
  {
    id: '4',
    title: '極限の計算',
    category: '解析学',
    difficulty: '中級',
    description: '\\lim_{x \\to 0} \\frac{\\sin x}{x} を計算せよ',
    completed: true,
  },
  {
    id: '5',
    title: 'テイラー展開',
    category: '解析学',
    difficulty: '上級',
    description: '関数 f(x) = e^x のテイラー展開を求めよ',
    completed: false,
  },
];

// カテゴリとレベルの一覧（後でAPIから取得するように変更）
const categories = ['すべて', '微分方程式', '三角関数', '線形代数', '解析学', '確率・統計'];
const difficulties = ['すべて', '初級', '中級', '上級'];

export default function ProblemsPage() {
  return (
    <div className="space-y-6">
      <div className="flex justify-between items-center">
        <h1 className="text-2xl font-bold">問題一覧</h1>
        
        <div className="flex space-x-2">
          {/* 検索フォーム */}
          <div className="relative">
            <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
              <FaSearch className="text-gray-400" />
            </div>
            <input
              type="text"
              placeholder="キーワードで検索"
              className="pl-10 pr-4 py-2 border border-gray-300 rounded-md focus:ring-blue-500 focus:border-blue-500"
            />
          </div>
          
          {/* フィルターボタン */}
          <button className="bg-white border border-gray-300 rounded-md px-4 py-2 flex items-center">
            <FaFilter className="mr-2 text-gray-500" />
            <span>フィルター</span>
          </button>
        </div>
      </div>
      
      {/* フィルターパネル */}
      <div className="bg-white p-4 rounded-lg shadow">
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              カテゴリ
            </label>
            <select className="block w-full border border-gray-300 rounded-md p-2 focus:ring-blue-500 focus:border-blue-500">
              {categories.map((category) => (
                <option key={category} value={category === 'すべて' ? '' : category}>
                  {category}
                </option>
              ))}
            </select>
          </div>
          
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              難易度
            </label>
            <select className="block w-full border border-gray-300 rounded-md p-2 focus:ring-blue-500 focus:border-blue-500">
              {difficulties.map((difficulty) => (
                <option key={difficulty} value={difficulty === 'すべて' ? '' : difficulty}>
                  {difficulty}
                </option>
              ))}
            </select>
          </div>
        </div>
      </div>
      
      {/* 問題一覧 */}
      <div className="space-y-4">
        {dummyProblems.map((problem) => (
          <Link
            key={problem.id}
            href={`/problems/${problem.id}`}
            className={`block bg-white rounded-lg shadow p-6 hover:shadow-md transition ${
              problem.completed ? 'border-l-4 border-green-500' : ''
            }`}
          >
            <div className="flex justify-between">
              <h2 className="text-xl font-medium">{problem.title}</h2>
              <div className="flex space-x-2">
                <span
                  className={`px-2 py-1 text-xs rounded-full ${
                    problem.difficulty === '初級'
                      ? 'bg-green-100 text-green-800'
                      : problem.difficulty === '中級'
                      ? 'bg-yellow-100 text-yellow-800'
                      : 'bg-red-100 text-red-800'
                  }`}
                >
                  {problem.difficulty}
                </span>
                <span className="px-2 py-1 text-xs bg-blue-100 text-blue-800 rounded-full">
                  {problem.category}
                </span>
              </div>
            </div>
            <div className="mt-4">
              <MathRenderer latex={problem.description} />
            </div>
            <div className="mt-4 flex justify-between items-center">
              <div className="text-sm text-gray-500">
                {problem.completed ? (
                  <span className="text-green-600">完了済み</span>
                ) : (
                  <span>未完了</span>
                )}
              </div>
              <div className="text-blue-600 text-sm font-medium">問題を解く</div>
            </div>
          </Link>
        ))}
      </div>
      
      {/* ページネーション */}
      <div className="flex justify-center mt-8">
        <nav className="flex items-center space-x-2">
          <a
            href="#"
            className="px-4 py-2 border border-gray-300 rounded-md text-sm font-medium text-gray-700 bg-white hover:bg-gray-50"
          >
            前へ
          </a>
          <a
            href="#"
            className="px-4 py-2 border border-gray-300 rounded-md text-sm font-medium text-white bg-blue-600 hover:bg-blue-700"
          >
            1
          </a>
          <a
            href="#"
            className="px-4 py-2 border border-gray-300 rounded-md text-sm font-medium text-gray-700 bg-white hover:bg-gray-50"
          >
            2
          </a>
          <a
            href="#"
            className="px-4 py-2 border border-gray-300 rounded-md text-sm font-medium text-gray-700 bg-white hover:bg-gray-50"
          >
            3
          </a>
          <a
            href="#"
            className="px-4 py-2 border border-gray-300 rounded-md text-sm font-medium text-gray-700 bg-white hover:bg-gray-50"
          >
            次へ
          </a>
        </nav>
      </div>
    </div>
  );
}