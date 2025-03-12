'use client';

import { useState, useEffect } from 'react';
import { useParams, useRouter } from 'next/navigation';
import { FaArrowLeft, FaCheck, FaTimes } from 'react-icons/fa';
import MathRenderer from '@/components/math/MathRenderer';
import Button from '@/components/ui/Button';
import { useUI } from '@/context/UIContext';

// ダミーデータ（後でAPIから取得するように変更）
const dummyProblemDetails = {
  id: '1',
  title: '微分方程式の解法',
  category: '微分方程式',
  difficulty: '中級',
  description:
    '次の微分方程式を解け: \\frac{dy}{dx} + P(x)y = Q(x)',
  options: [
    {
      id: 'a',
      text: 'y = e^{-\\int P(x)dx} \\int Q(x)e^{\\int P(x)dx}dx + C',
    },
    {
      id: 'b',
      text: 'y = e^{\\int P(x)dx} \\int Q(x)e^{-\\int P(x)dx}dx + C',
    },
    {
      id: 'c',
      text: 'y = e^{-\\int P(x)dx} \\left( \\int Q(x)dx + C \\right)',
    },
    {
      id: 'd',
      text: 'y = \\int P(x)dx \\cdot \\int Q(x)dx + C',
    },
  ],
  correctOption: 'a',
  explanation:
    '一階線形微分方程式 \\frac{dy}{dx} + P(x)y = Q(x) の一般解は積分因子法を用いて解くことができる。\\\\\\\\積分因子は \\mu(x) = e^{\\int P(x)dx} であり、両辺に掛けると:\\\\\\\\e^{\\int P(x)dx}\\frac{dy}{dx} + P(x)e^{\\int P(x)dx}y = Q(x)e^{\\int P(x)dx}\\\\\\\\左辺は導関数の形になり:\\\\\\\\\\frac{d}{dx}\\left(e^{\\int P(x)dx}y\\right) = Q(x)e^{\\int P(x)dx}\\\\\\\\両辺を積分すると:\\\\\\\\e^{\\int P(x)dx}y = \\int Q(x)e^{\\int P(x)dx}dx + C\\\\\\\\したがって:\\\\\\\\y = e^{-\\int P(x)dx} \\int Q(x)e^{\\int P(x)dx}dx + Ce^{-\\int P(x)dx}',
};

export default function ProblemDetailPage() {
  const params = useParams();
  const router = useRouter();
  const { showAlert } = useUI();
  const [selectedOption, setSelectedOption] = useState<string | null>(null);
  const [isSubmitted, setIsSubmitted] = useState(false);
  const [isCorrect, setIsCorrect] = useState(false);
  const [problem, setProblem] = useState(dummyProblemDetails);

  useEffect(() => {
    // 実際の実装ではここでAPIから問題データを取得
    // 今はダミーデータを使用
    setProblem(dummyProblemDetails);
  }, [params.id]);

  const handleOptionSelect = (optionId: string) => {
    if (!isSubmitted) {
      setSelectedOption(optionId);
    }
  };

  const handleSubmit = () => {
    if (!selectedOption) {
      showAlert('回答を選択してください', 'warning');
      return;
    }

    const correct = selectedOption === problem.correctOption;
    setIsCorrect(correct);
    setIsSubmitted(true);

    if (correct) {
      showAlert('正解です！', 'success');
    } else {
      showAlert('不正解です。解説を確認してください。', 'error');
    }
  };

  const handleNext = () => {
    // 次の問題へ進む処理（仮実装）
    const nextId = Number(params.id) + 1;
    router.push(`/problems/${nextId}`);
  };

  return (
    <div className="max-w-4xl mx-auto">
      {/* 戻るボタン */}
      <button
        onClick={() => router.push('/problems')}
        className="mb-6 flex items-center text-blue-600 hover:text-blue-800"
      >
        <FaArrowLeft className="mr-2" />
        <span>問題一覧に戻る</span>
      </button>

      {/* 問題ヘッダー */}
      <div className="bg-white rounded-lg shadow-md p-6 mb-6">
        <div className="flex justify-between items-start">
          <h1 className="text-2xl font-bold">{problem.title}</h1>
          <div className="flex space-x-2">
            <span
              className={`px-3 py-1 rounded-full text-sm ${
                problem.difficulty === '初級'
                  ? 'bg-green-100 text-green-800'
                  : problem.difficulty === '中級'
                  ? 'bg-yellow-100 text-yellow-800'
                  : 'bg-red-100 text-red-800'
              }`}
            >
              {problem.difficulty}
            </span>
            <span className="px-3 py-1 bg-blue-100 text-blue-800 rounded-full text-sm">
              {problem.category}
            </span>
          </div>
        </div>

        <div className="mt-6">
          <MathRenderer latex={problem.description} block />
        </div>
      </div>

      {/* 選択肢 */}
      <div className="bg-white rounded-lg shadow-md p-6 mb-6">
        <h2 className="text-lg font-semibold mb-4">解答を選択してください</h2>
        <div className="space-y-4">
          {problem.options.map((option) => (
            <div
              key={option.id}
              className={`p-4 border rounded-lg cursor-pointer transition-all duration-200 ${
                selectedOption === option.id
                  ? 'border-blue-500 bg-blue-50 shadow-md'
                  : 'border-gray-200 hover:border-blue-200 hover:shadow-sm'
              } ${
                isSubmitted && option.id === problem.correctOption
                  ? 'border-green-500 bg-green-50 shadow-md'
                  : isSubmitted && option.id === selectedOption && option.id !== problem.correctOption
                  ? 'border-red-500 bg-red-50 shadow-md'
                  : ''
              }`}
              onClick={() => handleOptionSelect(option.id)}
            >
              <div className="flex items-start">
                <div className="mr-3 flex-shrink-0">
                  <div
                    className={`w-6 h-6 flex items-center justify-center rounded-full transition-colors ${
                      selectedOption === option.id
                        ? 'bg-blue-500 text-white'
                        : 'bg-gray-200'
                    } ${
                      isSubmitted && option.id === problem.correctOption
                        ? 'bg-green-500 text-white'
                        : isSubmitted && option.id === selectedOption && option.id !== problem.correctOption
                        ? 'bg-red-500 text-white'
                        : ''
                    }`}
                  >
                    {isSubmitted && option.id === problem.correctOption ? (
                      <FaCheck size={12} />
                    ) : isSubmitted && option.id === selectedOption && option.id !== problem.correctOption ? (
                      <FaTimes size={12} />
                    ) : (
                      <span className="text-sm">{option.id.toUpperCase()}</span>
                    )}
                  </div>
                </div>
                <div className="flex-1">
                  <MathRenderer latex={option.text} />
                </div>
              </div>
            </div>
          ))}
        </div>

        <div className="flex justify-center mt-8">
          {!isSubmitted ? (
            <Button
              variant="primary"
              size="lg"
              onClick={handleSubmit}
              disabled={!selectedOption}
            >
              回答を提出する
            </Button>
          ) : (
            <Button variant="success" size="lg" onClick={handleNext}>
              次の問題へ
            </Button>
          )}
        </div>
      </div>

      {/* 解説（提出後に表示） */}
      {isSubmitted && (
        <div className="bg-white rounded-lg shadow-md p-6">
          <h2 className="text-lg font-semibold mb-4">解説</h2>
          <div className="p-4 bg-gray-50 rounded-lg">
            <MathRenderer latex={problem.explanation} block />
          </div>
        </div>
      )}
    </div>
  );
}