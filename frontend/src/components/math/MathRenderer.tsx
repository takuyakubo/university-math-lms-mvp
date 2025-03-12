'use client';

import React from 'react';
import 'katex/dist/katex.min.css';
import { InlineMath, BlockMath } from 'react-katex';

export interface MathRendererProps {
  latex: string;
  block?: boolean;
  className?: string;
  errorColor?: string;
}

/**
 * KaTeXを使用してLaTeX数式をレンダリングするコンポーネント
 * @param latex LaTeX形式の数式文字列
 * @param block ブロック表示（中央揃え）にするかどうか
 * @param className 追加のCSSクラス
 * @param errorColor エラー表示時の色
 */
const MathRenderer: React.FC<MathRendererProps> = ({
  latex,
  block = false,
  className = '',
  errorColor = '#cc0000',
}) => {
  // LaTeX文字列が空の場合は何も表示しない
  if (!latex || latex.trim() === '') {
    return null;
  }

  try {
    if (block) {
      return (
        <div className={`my-4 ${className}`} data-testid="math-block">
          <BlockMath math={latex} errorColor={errorColor} />
        </div>
      );
    }

    return (
      <span className={className} data-testid="math-inline">
        <InlineMath math={latex} errorColor={errorColor} />
      </span>
    );
  } catch (error) {
    console.error('LaTeX rendering error:', error);
    return (
      <span
        style={{ color: errorColor }}
        className={`italic ${className}`}
        title={`LaTeX error: ${error}`}
      >
        [LaTeX error: {String(error).substring(0, 50)}]
      </span>
    );
  }
};

export default MathRenderer;