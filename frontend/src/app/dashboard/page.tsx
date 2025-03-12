import { Metadata } from 'next';
import { FaBook, FaChartLine, FaGraduationCap, FaClock } from 'react-icons/fa';
import MathRenderer from '@/components/math/MathRenderer';
import Link from 'next/link';

export const metadata: Metadata = {
  title: 'ダッシュボード - Math LMS',
  description: '数学学習の進捗状況やおすすめの問題を確認できます',
};

// ダミーデータ（後でAPIから取得するように変更）
const dummyRecentProblems = [
  { id: '1', title: '微分方程式の解法', category: '微分方程式', difficulty: '中級' },
  { id: '2', title: '三角関数の性質', category: '三角関数', difficulty: '初級' },
  { id: '3', title: '線形代数の基礎', category: '線形代数', difficulty: '初級' },
];

export default function DashboardPage() {
  const completedProblems = 15;
  const totalProblems = 50;

  return (
    <div className="space-y-8">
      <div className="flex items-center justify-between">
        <h1 className="text-2xl font-bold">ダッシュボード</h1>
      </div>

      {/* 概要統計 */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        <div className="bg-white rounded-lg shadow p-6 flex items-center">
          <div className="rounded-full bg-blue-100 p-3 mr-4">
            <FaBook className="text-blue-600 text-xl" />
          </div>
          <div>
            <p className="text-sm text-gray-500">完了した問題</p>
            <p className="text-2xl font-bold">{completedProblems}</p>
          </div>
        </div>

        <div className="bg-white rounded-lg shadow p-6 flex items-center">
          <div className="rounded-full bg-green-100 p-3 mr-4">
            <FaChartLine className="text-green-600 text-xl" />
          </div>
          <div>
            <p className="text-sm text-gray-500">正答率</p>
            <p className="text-2xl font-bold">
              {Math.round((completedProblems / totalProblems) * 100)}%
            </p>
          </div>
        </div>

        <div className="bg-white rounded-lg shadow p-6 flex items-center">
          <div className="rounded-full bg-purple-100 p-3 mr-4">
            <FaGraduationCap className="text-purple-600 text-xl" />
          </div>
          <div>
            <p className="text-sm text-gray-500">現在のレベル</p>
            <p className="text-2xl font-bold">初級</p>
          </div>
        </div>

        <div className="bg-white rounded-lg shadow p-6 flex items-center">
          <div className="rounded-full bg-yellow-100 p-3 mr-4">
            <FaClock className="text-yellow-600 text-xl" />
          </div>
          <div>
            <p className="text-sm text-gray-500">総学習時間</p>
            <p className="text-2xl font-bold">12.5時間</p>
          </div>
        </div>
      </div>

      {/* 学習進捗 */}
      <div className="bg-white rounded-lg shadow p-6">
        <h2 className="text-xl font-semibold mb-4">学習進捗</h2>
        <div className="w-full bg-gray-200 rounded-full h-4 mb-4">
          <div
            className="bg-blue-600 h-4 rounded-full"
            style={{ width: `${(completedProblems / totalProblems) * 100}%` }}
          ></div>
        </div>
        <p className="text-gray-600">
          {completedProblems} / {totalProblems} 問題完了
        </p>
      </div>

      {/* 最近の問題 */}
      <div className="bg-white rounded-lg shadow p-6">
        <h2 className="text-xl font-semibold mb-4">最近の問題</h2>
        <div className="space-y-4">
          {dummyRecentProblems.map((problem) => (
            <Link
              key={problem.id}
              href={`/problems/${problem.id}`}
              className="block border rounded-md p-4 hover:bg-gray-50 transition"
            >
              <h3 className="font-medium">{problem.title}</h3>
              <div className="flex items-center text-sm text-gray-500 mt-2">
                <span className="mr-4">カテゴリ: {problem.category}</span>
                <span>難易度: {problem.difficulty}</span>
              </div>
            </Link>
          ))}
        </div>
      </div>

      {/* 数式サンプル */}
      <div className="bg-white rounded-lg shadow p-6">
        <h2 className="text-xl font-semibold mb-4">今日のピックアップ数式</h2>
        <div className="p-4 bg-gray-50 rounded-md">
          <MathRenderer
            block
            latex="e^{i\pi} + 1 = 0"
          />
          <p className="text-center text-gray-600 mt-2">
            オイラーの等式：数学で最も美しい公式の一つ
          </p>
        </div>
      </div>
    </div>
  );
}