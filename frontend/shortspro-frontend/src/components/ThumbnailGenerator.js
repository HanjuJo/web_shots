// frontend/src/components/ThumbnailGenerator.js
import React, { useState } from 'react';
import axios from 'axios';

const ThumbnailGenerator = () => {
    const [file, setFile] = useState(null);
    const [title, setTitle] = useState('');
    const [hashtags, setHashtags] = useState('');
    const [thumbnailUrl, setThumbnailUrl] = useState('');

    const handleFileChange = (e) => {
        setFile(e.target.files[0]);
    };

    const handleSubmit = async () => {
        if (!file || !title) {
            alert("이미지와 제목을 입력하세요.");
            return;
        }

        const formData = new FormData();
        formData.append('file', file);
        formData.append('title', title);
        formData.append('hashtags', hashtags);

        try {
            const response = await axios.post('http://127.0.0.1:8000/api/thumbnail', formData);
            setThumbnailUrl(response.data.output_path);
        } catch (error) {
            console.error("Error uploading file:", error);
            alert("썸네일 생성에 실패했습니다.");
        }
    };

    return (
        <div className="p-6 bg-white rounded-lg shadow-md">
            <h2 className="text-xl font-bold mb-4">🖼️ 쇼츠 썸네일 생성기</h2>

            <div className="mb-4">
                <label className="block mb-1 font-medium">이미지 업로드</label>
                <input type="file" onChange={handleFileChange} className="w-full border border-gray-300 rounded p-2"/>
            </div>

            <div className="mb-4">
                <label className="block mb-1 font-medium">제목</label>
                <input type="text" value={title} onChange={(e) => setTitle(e.target.value)}
                       className="w-full border border-gray-300 rounded p-2" placeholder="예: 귀여운 고양이"/>
            </div>

            <div className="mb-4">
                <label className="block mb-1 font-medium">해시태그 (쉼표로 구분)</label>
                <input type="text" value={hashtags} onChange={(e) => setHashtags(e.target.value)}
                       className="w-full border border-gray-300 rounded p-2" placeholder="예: #고양이, #귀여움, #쇼츠"/>
            </div>

            <button onClick={handleSubmit} className="w-full p-3 bg-blue-500 text-white rounded-lg hover:bg-blue-600">
                생성하기
            </button>

            {thumbnailUrl && (
                <div className="mt-4">
                    <h3 className="text-lg font-semibold mb-2">✨ 생성된 썸네일</h3>
                    <img src={`http://127.0.0.1:8000/${thumbnailUrl}`} alt="썸네일" className="w-full rounded-lg"/>
                </div>
            )}
        </div>
    );
};

export default ThumbnailGenerator;
