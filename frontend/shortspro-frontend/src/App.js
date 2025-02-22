// src/App.js
import React from 'react';
import ThumbnailGenerator from './components/ThumbnailGenerator';
import CompetitorAnalysis from './components/CompetitorAnalysis';

const App = () => {
    return (
        <div className="min-h-screen bg-gray-100 p-8">
            <h1 className="text-3xl font-bold text-center mb-8 text-primary">🎯 유튜브 쇼츠 제작자 도구</h1>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
                <ThumbnailGenerator />
                <CompetitorAnalysis />
            </div>
            <footer className="mt-8 text-center text-gray-500">
                &copy; 2025 유튜브 쇼츠 제작자 도구. All Rights Reserved.
            </footer>
        </div>
    );
};

export default App;
