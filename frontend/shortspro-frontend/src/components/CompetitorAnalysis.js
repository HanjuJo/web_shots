// frontend/src/components/CompetitorAnalysis.js
import React, { useState } from 'react';
import axios from 'axios';

const CompetitorAnalysis = () => {
    const [channelUrl, setChannelUrl] = useState('');
    const [maxVideos, setMaxVideos] = useState(10);
    const [videoData, setVideoData] = useState([]);
    const [graphHtml, setGraphHtml] = useState('');

    const handleSubmit = async () => {
        if (!channelUrl) {
            alert("채널 URL을 입력하세요.");
            return;
        }

        try {
            const response = await axios.get('http://127.0.0.1:8000/api/competitor_analysis', {
                params: {
                    channel_url: channelUrl,
                    max_videos: maxVideos
                }
            });
            setVideoData(response.data.data);
            setGraphHtml(response.data.graph_html);
        } catch (error) {
            console.error("Error fetching channel data:", error);
            alert("채널 데이터를 가져오는 데 실패했습니다.");
        }
    };

    return (
        <div className="p-6 bg-white rounded-lg shadow-md">
            <h2 className="text-xl font-bold mb-4">📊 경쟁 채널 분석</h2>

            <div className="mb-4">
                <label className="block mb-1 font-medium">채널 URL</label>
                <input type="text" value={channelUrl} onChange={(e) => setChannelUrl(e.target.value)}
                       className="w-full border border-gray-300 rounded p-2"
                       placeholder="예: https://www.youtube.com/channel/UCxyz"/>
            </div>

            <div className="mb-4">
                <label className="block mb-1 font-medium">분석할 쇼츠 수 (1-20)</label>
                <input type="number" value={maxVideos} onChange={(e) => setMaxVideos(e.target.value)}
                       className="w-full border border-gray-300 rounded p-2" min="1" max="20"/>
            </div>

            <button onClick={handleSubmit} className="w-full p-3 bg-blue-500 text-white rounded-lg hover:bg-blue-600">
                분석 시작
            </button>

            {videoData.length > 0 && (
                <div className="mt-4">
                    <h3 className="text-lg font-semibold mb-2">✨ 최근 쇼츠 목록</h3>
                    <ul className="list-disc pl-5">
                        {videoData.map((video, index) => (
                            <li key={index} className="mb-2">
                                <a href={video.url} target="_blank" rel="noopener noreferrer" className="text-blue-500 hover:underline">
                                    {video.title}
                                </a> - 조회수: {video.view_count.toLocaleString()}회, 증가율: {video.view_growth.toFixed(2)}%
                            </li>
                        ))}
                    </ul>
                </div>
            )}

            {graphHtml && (
                <div className="mt-4">
                    <h3 className="text-lg font-semibold mb-2">📈 조회수 증가율 그래프</h3>
                    <div dangerouslySetInnerHTML={{ __html: graphHtml }} />
                </div>
            )}
        </div>
    );
};

export default CompetitorAnalysis;
