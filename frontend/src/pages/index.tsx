import React from 'react';
import Head from 'next/head';

export default function Home() {
  return (
    <div className="min-h-screen bg-gray-50">
      <Head>
        <title>Math LMS - University Mathematics Learning Management System</title>
        <meta name="description" content="University Mathematics Learning Management System" />
        <link rel="icon" href="/favicon.ico" />
      </Head>

      <main className="container mx-auto py-12 px-4">
        <h1 className="text-4xl font-bold text-center mb-8">
          Welcome to Math LMS
        </h1>
        <p className="text-center text-lg mb-8">
          A specialized Learning Management System for university-level mathematics.
        </p>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-6 max-w-4xl mx-auto">
          <div className="bg-white rounded-lg shadow-md p-6">
            <h2 className="text-xl font-semibold mb-3">Interactive Math Content</h2>
            <p>Advanced mathematical notation with interactive elements for better learning.</p>
          </div>
          <div className="bg-white rounded-lg shadow-md p-6">
            <h2 className="text-xl font-semibold mb-3">Personalized Learning</h2>
            <p>Adaptive learning paths based on student progress and proficiency.</p>
          </div>
          <div className="bg-white rounded-lg shadow-md p-6">
            <h2 className="text-xl font-semibold mb-3">Comprehensive Analytics</h2>
            <p>Detailed insights into learning patterns and performance metrics.</p>
          </div>
        </div>
      </main>
    </div>
  );
}