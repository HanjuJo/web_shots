// frontend/src/App.js
import React from 'react';
import ThumbnailGenerator from './components/ThumbnailGenerator';
import CompetitorAnalysis from './components/CompetitorAnalysis';

const App = () => {
    return (
        <div className="min-h-screen bg-gray-100 p-8">
            <h1 className="text-3xl font-bold text-center mb-8">🎯 유튜브 쇼츠 제작자 도구</h1>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
                <ThumbnailGenerator />
                <CompetitorAnalysis />
            </div>
        </div>
    );
};

export default App;
