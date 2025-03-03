from flask import Flask, jsonify, request, send_file
from flask_cors import CORS
import os
import sqlite3
from datetime import datetime
from dotenv import load_dotenv
import json
import tempfile
import shutil
from youtube_analyzer import YoutubeAnalyzer
from ai_tools import AIToolkit
from community import CommunityManager
from youtube_service import YoutubeAnalyzer
from services.trend_service import TrendService
from services.tool_recommendation_service import ToolRecommendationService
from services.api_integration_service import APIIntegrationService

app = Flask(__name__)
CORS(app, resources={
    r"/api/*": {
        "origins": ["http://localhost:8082", "http://127.0.0.1:8082"],
        "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
        "allow_headers": ["Content-Type", "Authorization"]
    }
})

# Load environment variables
load_dotenv()

# Initialize analyzers
youtube_analyzer = YoutubeAnalyzer()
ai_toolkit = AIToolkit()
community_manager = CommunityManager()
trend_service = TrendService(os.getenv('TWITTER_BEARER_TOKEN'))
tool_service = ToolRecommendationService('data/ai_tools_db.json')
api_service = APIIntegrationService()
youtube_service = YoutubeAnalyzer()

# 임시 디렉토리 생성
TEMP_DIR = "temp_files"
os.makedirs(TEMP_DIR, exist_ok=True)

def init_db():
    conn = sqlite3.connect('creator_tool.db')
    c = conn.cursor()
    
    # AI 도구 데이터베이스 테이블
    c.execute('''CREATE TABLE IF NOT EXISTS ai_tools
                (id INTEGER PRIMARY KEY,
                name TEXT,
                category TEXT,
                description TEXT,
                pricing_type TEXT,
                base_price REAL,
                api_available BOOLEAN,
                website_url TEXT,
                features TEXT,
                use_cases TEXT,
                tutorials TEXT,
                last_updated TIMESTAMP)''')
    
    # AI 도구 리뷰 테이블
    c.execute('''CREATE TABLE IF NOT EXISTS ai_tool_reviews
                (id INTEGER PRIMARY KEY,
                tool_id INTEGER,
                user_rating FLOAT,
                review_text TEXT,
                pros TEXT,
                cons TEXT,
                review_date TIMESTAMP,
                FOREIGN KEY(tool_id) REFERENCES ai_tools(id))''')
    
    # 유튜브 채널 분석 테이블
    c.execute('''CREATE TABLE IF NOT EXISTS youtube_channels
                (id INTEGER PRIMARY KEY,
                channel_id TEXT UNIQUE,
                title TEXT,
                subscriber_count INTEGER,
                video_count INTEGER,
                avg_views INTEGER,
                last_analyzed TIMESTAMP)''')
    
    conn.commit()
    conn.close()

init_db()

@app.route('/')
def hello():
    return "Creator Tool API is running!"

# AI 도구 관련 엔드포인트
@app.route('/api/ai-tools', methods=['GET'])
def get_ai_tools():
    try:
        category = request.args.get('category')
        keyword = request.args.get('keyword')
        price_range = request.args.get('price_range')
        
        conn = sqlite3.connect('creator_tool.db')
        c = conn.cursor()
        
        query = "SELECT * FROM ai_tools WHERE 1=1"
        params = []
        
        if category:
            query += " AND category = ?"
            params.append(category)
        
        if keyword:
            query += " AND (name LIKE ? OR description LIKE ?)"
            params.extend([f"%{keyword}%", f"%{keyword}%"])
            
        if price_range:
            min_price, max_price = map(float, price_range.split('-'))
            query += " AND base_price BETWEEN ? AND ?"
            params.extend([min_price, max_price])
            
        c.execute(query, params)
        tools = c.fetchall()
        
        result = []
        for tool in tools:
            tool_data = {
                'id': tool[0],
                'name': tool[1],
                'category': tool[2],
                'description': tool[3],
                'pricing_type': tool[4],
                'base_price': tool[5],
                'api_available': bool(tool[6]),
                'website_url': tool[7],
                'features': json.loads(tool[8]) if tool[8] else [],
                'use_cases': json.loads(tool[9]) if tool[9] else [],
                'tutorials': json.loads(tool[10]) if tool[10] else [],
                'last_updated': tool[11]
            }
            result.append(tool_data)
            
        return jsonify({'success': True, 'tools': result})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/ai-tools/recommend', methods=['POST'])
def recommend_ai_tools():
    try:
        data = request.get_json()
        content_type = data.get('content_type')  # video, image, text, audio
        task_description = data.get('task_description')
        budget = data.get('budget', float('inf'))
        
        # 컨텐츠 타입과 작업 설명을 기반으로 적절한 AI 도구 추천
        conn = sqlite3.connect('creator_tool.db')
        c = conn.cursor()
        
        query = """
        SELECT * FROM ai_tools 
        WHERE category LIKE ? 
        AND base_price <= ?
        ORDER BY id DESC
        LIMIT 5
        """
        
        c.execute(query, (f"%{content_type}%", budget))
        recommendations = c.fetchall()
        
        result = []
        for tool in recommendations:
            tool_data = {
                'name': tool[1],
                'description': tool[3],
                'pricing': {
                    'type': tool[4],
                    'base_price': tool[5]
                },
                'features': json.loads(tool[8]) if tool[8] else [],
                'use_cases': json.loads(tool[9]) if tool[9] else [],
                'tutorials': json.loads(tool[10]) if tool[10] else []
            }
            result.append(tool_data)
            
        return jsonify({
            'success': True, 
            'recommendations': result,
            'task_description': task_description
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

# AI 도구 통합 엔드포인트
@app.route('/api/tools/translate', methods=['POST'])
def translate_text():
    try:
        data = request.get_json()
        text = data.get('text')
        target_lang = data.get('target_lang', 'en')
        
        if not text:
            return jsonify({'success': False, 'error': 'No text provided'}), 400
            
        result = ai_toolkit.translate_text(text, target_lang)
        return jsonify(result)
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/tools/text-to-speech', methods=['POST'])
def convert_text_to_speech():
    try:
        data = request.get_json()
        text = data.get('text')
        lang = data.get('lang', 'ko')
        
        if not text:
            return jsonify({'success': False, 'error': 'No text provided'}), 400
            
        result = ai_toolkit.text_to_speech(text, lang)
        if result['success']:
            return send_file(
                result['audio_path'],
                mimetype='audio/mp3',
                as_attachment=True,
                download_name='speech.mp3'
            )
        return jsonify(result)
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/translate', methods=['POST'])
def translate():
    data = request.get_json()
    text = data.get('text', '')
    target_lang = data.get('target_lang', 'en')
    
    result = ai_toolkit.translate_text(text, target_lang)
    return jsonify(result)

@app.route('/api/text-to-speech', methods=['POST'])
def text_to_speech():
    data = request.get_json()
    text = data.get('text', '')
    lang = data.get('lang', 'ko')
    
    result = ai_toolkit.text_to_speech(text, lang)
    return jsonify(result)

# 커뮤니티 관련 엔드포인트
@app.route('/api/posts', methods=['GET'])
def get_posts():
    page = int(request.args.get('page', 1))
    per_page = int(request.args.get('per_page', 20))
    category = request.args.get('category')
    search = request.args.get('search')
    sort_by = request.args.get('sort_by', 'latest')
    
    try:
        result = community_manager.get_posts(
            page=page,
            per_page=per_page,
            category=category,
            search=search,
            sort_by=sort_by
        )
        return jsonify(result)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/posts', methods=['POST'])
def create_post():
    data = request.json
    
    try:
        post = community_manager.create_post(
            user_id=data['user_id'],
            title=data['title'],
            content=data['content'],
            category=data['category'],
            tags=data.get('tags'),
            images=data.get('images')
        )
        return jsonify(post)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/posts/<int:post_id>', methods=['GET'])
def get_post(post_id):
    user_id = request.args.get('user_id')
    
    try:
        post = community_manager.get_post(post_id, user_id)
        if not post:
            return jsonify({'error': 'Post not found'}), 404
        return jsonify(post)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/posts/<int:post_id>/comments', methods=['POST'])
def create_comment():
    data = request.json
    
    try:
        comment = community_manager.create_comment(
            user_id=data['user_id'],
            post_id=data['post_id'],
            content=data['content'],
            parent_id=data.get('parent_id')
        )
        return jsonify(comment)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/posts/<int:post_id>/like', methods=['POST'])
def toggle_post_like(post_id):
    data = request.json
    
    try:
        result = community_manager.toggle_like(
            user_id=data['user_id'],
            post_id=post_id
        )
        return jsonify(result)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/comments/<int:comment_id>/like', methods=['POST'])
def toggle_comment_like(comment_id):
    data = request.json
    
    try:
        result = community_manager.toggle_like(
            user_id=data['user_id'],
            comment_id=comment_id
        )
        return jsonify(result)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# 댓글 관련 엔드포인트
@app.route('/api/comments/<int:comment_id>', methods=['PUT'])
def update_comment(comment_id):
    data = request.json
    
    try:
        comment = community_manager.update_comment(
            comment_id=comment_id,
            content=data['content']
        )
        return jsonify(comment)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/comments/<int:comment_id>', methods=['DELETE'])
def delete_comment(comment_id):
    try:
        community_manager.delete_comment(comment_id)
        return jsonify({'success': True})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/posts/<int:post_id>/comments', methods=['GET'])
def get_comments(post_id):
    page = int(request.args.get('page', 1))
    per_page = int(request.args.get('per_page', 20))
    
    try:
        result = community_manager.get_comments(
            post_id=post_id,
            page=page,
            per_page=per_page
        )
        return jsonify(result)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# YouTube 분석 엔드포인트
@app.route('/api/youtube/search', methods=['POST'])
def search_youtube_channels():
    try:
        data = request.get_json()
        keyword = data.get('keyword')
        content_type = data.get('contentType', 'all')
        
        # 실제 검색 및 분석 로직
        channels = []
        # 예시 데이터 (실제로는 YouTube API와 yt-dlp를 사용하여 데이터 수집)
        channels = [
            {
                'id': 'UC...',
                'title': '인기 크리에이터',
                'subscribers': 1000000,
                'views': 50000000,
                'videos': 200,
                'avgViews': 250000,
                'thumbnail': 'https://example.com/thumbnail.jpg',
                'popularTopics': ['일상', '브이로그', '먹방'],
                'avgDuration': '10:30',
                'uploadFrequency': '주 3회',
                'growthTips': [
                    '일관된 업로드 주기 유지',
                    '트렌딩 주제 활용',
                    'SEO 최적화'
                ]
            }
        ]
        
        return jsonify({'success': True, 'channels': channels})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/youtube/analyze', methods=['POST'])
def analyze_youtube_channel():
    try:
        data = request.get_json()
        channel_url = data.get('channelUrl')
        
        if not channel_url:
            return jsonify({'success': False, 'error': 'Channel URL is required'}), 400
            
        # 채널 분석 수행
        analysis = youtube_analyzer.analyze_channel(channel_url)
        
        if not analysis:
            return jsonify({'success': False, 'error': 'Failed to analyze channel'}), 500
            
        # 성장 제안 가져오기
        suggestions = youtube_analyzer.get_growth_suggestions(analysis)
        analysis['growth_suggestions'] = suggestions
        
        return jsonify({'success': True, 'analysis': analysis})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/youtube/shorts-analysis', methods=['POST'])
def analyze_shorts():
    try:
        data = request.get_json()
        keyword = data.get('keyword')
        max_results = data.get('maxResults', 10)
        
        if not keyword:
            return jsonify({'error': '키워드를 입력해주세요'}), 400
            
        results = youtube_analyzer.analyze_shorts(keyword, max_results)
        return jsonify(results)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/youtube/video-analysis', methods=['POST'])
def analyze_videos():
    try:
        data = request.get_json()
        keyword = data.get('keyword')
        max_results = data.get('maxResults', 5)
        
        if not keyword:
            return jsonify({'error': '키워드를 입력해주세요'}), 400
            
        results = youtube_analyzer.analyze_top_videos(keyword, max_results)
        return jsonify(results)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# AI 트렌드 엔드포인트
@app.route('/api/trends', methods=['GET'])
def get_trends():
    """Get latest AI trends and news"""
    try:
        trends = trend_service.get_latest_ai_trends()
        return jsonify(trends)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# AI 도구 추천 엔드포인트
@app.route('/api/tools/recommend', methods=['POST'])
def recommend_tools():
    """Get AI tool recommendations based on query"""
    data = request.get_json()
    query = data.get('query')
    limit = data.get('limit', 5)
    
    if not query:
        return jsonify({"error": "Query is required"}), 400
        
    try:
        recommendations = tool_service.recommend_tools(query, limit)
        return jsonify(recommendations)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/tools/categories/<category>', methods=['GET'])
def get_tools_by_category(category):
    """Get AI tools by category"""
    try:
        tools = tool_service.get_tools_by_category(category)
        return jsonify(tools)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# API 통합 엔드포인트
@app.route('/api/generate/text', methods=['POST'])
def generate_text():
    """Generate text using AI"""
    data = request.get_json()
    prompt = data.get('prompt')
    max_tokens = data.get('max_tokens', 500)
    
    if not prompt:
        return jsonify({"error": "Prompt is required"}), 400
        
    try:
        result = api_service.generate_text(prompt, max_tokens)
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/generate/image', methods=['POST'])
def generate_image():
    """Generate image using AI"""
    data = request.get_json()
    prompt = data.get('prompt')
    size = data.get('size', '1024x1024')
    
    if not prompt:
        return jsonify({"error": "Prompt is required"}), 400
        
    try:
        result = api_service.generate_image(prompt, size)
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/generate/video-script', methods=['POST'])
def generate_video_script():
    """Generate video script using AI"""
    data = request.get_json()
    topic = data.get('topic')
    duration = data.get('duration', 'short')
    
    if not topic:
        return jsonify({"error": "Topic is required"}), 400
        
    try:
        result = api_service.generate_video_script(topic, duration)
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# YouTube Shorts 분석 엔드포인트
@app.route('/api/youtube/shorts-analysis', methods=['POST'])
def analyze_shorts():
    """Analyze YouTube shorts"""
    data = request.get_json()
    keyword = data.get('keyword')
    max_results = data.get('max_results', 10)
    
    if not keyword:
        return jsonify({"error": "Keyword is required"}), 400
        
    try:
        results = youtube_service.analyze_shorts(keyword, max_results)
        return jsonify(results)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# YouTube 비디오 분석 엔드포인트
@app.route('/api/youtube/video-analysis', methods=['POST'])
def analyze_videos():
    """Analyze regular YouTube videos"""
    data = request.get_json()
    keyword = data.get('keyword')
    max_results = data.get('max_results', 5)
    
    if not keyword:
        return jsonify({"error": "Keyword is required"}), 400
        
    try:
        results = youtube_service.analyze_top_videos(keyword, max_results)
        return jsonify(results)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# 서버 종료 시 임시 파일 정리
@app.teardown_appcontext
def cleanup_temp_files(error):
    try:
        shutil.rmtree(TEMP_DIR)
        os.makedirs(TEMP_DIR)
    except Exception as e:
        print(f"Error cleaning up temp files: {e}")

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5003))
    app.run(host='0.0.0.0', port=port, debug=True)