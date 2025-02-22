// frontend/src/components/ThumbnailGenerator.js
import React, { useState } from 'react';
import axios from 'axios';

const ThumbnailGenerator = () => {
    const [file, setFile] = useState(null);
    const [title, setTitle] = useState('');
    const [hashtags, setHashtags] = useState('');
    const [position, setPosition] = useState('top');
    const [textColor, setTextColor] = useState('white');
    const [borderColor, setBorderColor] = useState('black');
    const [bgColor, setBgColor] = useState('');
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
        formData.append('position', position);
        formData.append('text_color', textColor);
        formData.append('border_color', borderColor);
        if (bgColor) formData.append('bg_color', bgColor);

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
                {file && (
                    <div className="mt-2">
                        <img src={URL.createObjectURL(file)} alt="미리보기" className="w-full rounded-lg"/>
                    </div>
                )}
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

            <div className="mb-4">
                <label className="block mb-1 font-medium">제목 위치</label>
                <select value={position} onChange={(e) => setPosition(e.target.value)}
                        className="w-full border border-gray-300 rounded p-2">
                    <option value="top">상단</option>
                    <option value="bottom">하단</option>
                </select>
            </div>

            <div className="mb-4">
                <label className="block mb-1 font-medium">글자 색상</label>
                <input type="color" value={textColor} onChange={(e) => setTextColor(e.target.value)}
                       className="w-full border border-gray-300 rounded p-2"/>
            </div>

            <div className="mb-4">
                <label className="block mb-1 font-medium">테두리 색상</label>
                <input type="color" value={borderColor} onChange={(e) => setBorderColor(e.target.value)}
                       className="w-full border border-gray-300 rounded p-2"/>
            </div>

            <div className="mb-4">
                <label className="block mb-1 font-medium">배경 색상 (선택사항)</label>
                <input type="color" value={bgColor} onChange={(e) => setBgColor(e.target.value)}
                       className="w-full border border-gray-300 rounded p-2"/>
            </div>

            <button onClick={handleSubmit} className="w-full p-3 bg-blue-500 text-white rounded-lg hover:bg-blue-600">
                생성하기
            </button>

            {thumbnailUrl && (
                <div className="mt-4">
                    <h3 className="text-lg font-semibold mb-2">✨ 생성된 썸네일</h3>
                    <img src={`http://127.0.0.1:8000/${thumbnailUrl}`} alt="썸네일" className="w-full rounded-lg"/>
                    <a href={`http://127.0.0.1:8000/${thumbnailUrl}`} download className="block mt-2 text-center text-blue-500 hover:underline">
                        📥 썸네일 다운로드
                    </a>
                </div>
            )}
        </div>
    );
};

export default ThumbnailGenerator;
