from typing import List, Dict
import json
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

class ToolRecommendationService:
    def __init__(self, tools_db_path: str):
        """Initialize with path to JSON file containing AI tools database"""
        with open(tools_db_path, 'r') as f:
            self.tools_db = json.load(f)
        
        # Prepare TF-IDF vectorizer
        self.vectorizer = TfidfVectorizer(stop_words='english')
        tool_descriptions = [tool['description'] + ' ' + ' '.join(tool['keywords']) 
                           for tool in self.tools_db]
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
            tool = self.tools_db[idx].copy()
            tool['similarity_score'] = float(similarity_scores[0][idx])
            recommendations.append(tool)
            
        return recommendations
    
    def get_tool_details(self, tool_id: str) -> Dict:
        """Get detailed information about a specific tool"""
        for tool in self.tools_db:
            if tool['id'] == tool_id:
                return tool
        return None
    
    def get_tools_by_category(self, category: str) -> List[Dict]:
        """Get all tools in a specific category"""
        return [tool for tool in self.tools_db if category in tool['categories']]
