from typing import List, Dict
import json
import os
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

class ToolRecommendationService:
    def __init__(self, tools_db_path: str):
        """Initialize with path to JSON file containing AI tools database"""
        try:
            with open(tools_db_path, 'r', encoding='utf-8') as f:
                self.tools_db = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            # 기본 도구 데이터베이스 제공
            self.tools_db = {
                "tools": [
                    {
                        "id": "1",
                        "name": "AI 스크립트 생성기",
                        "description": "유튜브 영상을 위한 스크립트를 자동으로 생성합니다.",
                        "categories": ["content", "writing", "youtube"],
                        "keywords": ["script", "content", "youtube", "writing"],
                        "features": ["자동 스크립트 생성", "키워드 기반 내용 구성", "SEO 최적화"]
                    },
                    {
                        "id": "2",
                        "name": "AI 음성 합성기",
                        "description": "자연스러운 음성을 자동으로 생성합니다.",
                        "categories": ["audio", "voice", "synthesis"],
                        "keywords": ["voice", "audio", "tts", "synthesis"],
                        "features": ["다국어 지원", "감정 표현", "음성 커스터마이징"]
                    },
                    {
                        "id": "3",
                        "name": "AI 자막 생성기",
                        "description": "영상에서 음성을 인식하여 자동으로 자막을 생성합니다.",
                        "categories": ["video", "subtitle", "transcription"],
                        "keywords": ["subtitle", "caption", "transcription", "video"],
                        "features": ["자동 음성 인식", "다국어 번역", "타이밍 동기화"]
                    }
                ]
            }
            # 기본 데이터베이스 저장
            os.makedirs(os.path.dirname(tools_db_path), exist_ok=True)
            with open(tools_db_path, 'w', encoding='utf-8') as f:
                json.dump(self.tools_db, f, ensure_ascii=False, indent=2)
        
        # Prepare TF-IDF vectorizer
        self.vectorizer = TfidfVectorizer(stop_words='english')
        tool_descriptions = [f"{tool['name']} {tool['description']} {' '.join(tool['keywords'])}" 
                           for tool in self.tools_db['tools']]
        self.tfidf_matrix = self.vectorizer.fit_transform(tool_descriptions)
        
    def recommend_tools(self, query: str, limit: int = 5) -> List[Dict]:
        """Recommend AI tools based on user query"""
        # Transform query using same vectorizer
        query_vector = self.vectorizer.transform([query])
        
        # Calculate similarity scores
        similarity_scores = cosine_similarity(query_vector, self.tfidf_matrix)
        
        # Get top N similar tools
        top_indices = similarity_scores[0].argsort()[-limit:][::-1]
        
        recommendations = []
        for idx in top_indices:
            tool = self.tools_db['tools'][idx].copy()
            tool['similarity_score'] = float(similarity_scores[0][idx])
            recommendations.append(tool)
            
        return recommendations
    
    def get_tool_details(self, tool_id: str) -> Dict:
        """Get detailed information about a specific tool"""
        for tool in self.tools_db['tools']:
            if tool['id'] == tool_id:
                return tool
        return None
    
    def get_tools_by_category(self, category: str) -> List[Dict]:
        """Get all tools in a specific category"""
        return [tool for tool in self.tools_db['tools'] if category in tool['categories']]
