from flask import Flask, jsonify, request, send_file
from flask_cors import CORS
import os
import sqlite3
from datetime import datetime, timedelta
from datetime import datetime, timedelta
from dotenv import load_dotenv
import json
import tempfile
import shutil
import jwt
from werkzeug.security import generate_password_hash, check_password_hash
from youtube_analyzer import YoutubeAnalyzer
from ai_tools import AIToolkit
from community import CommunityManager
from services.trend_service import TrendService
from services.tool_recommendation_service import ToolRecommendationService
from services.api_integration_service import APIIntegrationService

app = Flask(__name__)
CORS(app, resources={
    r"/*": {
        "origins": ["http://localhost:8083", "http://localhost:8084"],
        "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
        "allow_headers": ["Content-Type", "Authorization", "Accept"],
        "supports_credentials": True
    }
})

# Load environment variables
load_dotenv()

# JWT Configuration
JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY', 'your-secret-key')  # In production, use proper secret key
JWT_EXPIRATION_HOURS = 24

# Authentication endpoints
@app.route('/auth/register', methods=['POST'])
def register():
    conn = None
    try:
        if not request.is_json:
            return jsonify({
                'success': False,
                'message': '잘못된 요청 형식입니다'
            }), 400

        data = request.get_json()
        username = data.get('username')
        email = data.get('email')
        password = data.get('password')
        
        if not all([username, email, password]):
            return jsonify({
                'success': False,
                'message': '모든 필드를 입력해주세요'
            }), 400
            
        # Validate email format
        if '@' not in email or '.' not in email:
            return jsonify({
                'success': False,
                'message': '올바른 이메일 형식이 아닙니다'
            }), 400
            
        # Validate password length
        if len(password) < 6:
            return jsonify({
                'success': False,
                'message': '비밀번호는 최소 6자 이상이어야 합니다'
            }), 400

        conn = sqlite3.connect('creator_tool.db')
        c = conn.cursor()
        
        # Check if email already exists
        c.execute('SELECT * FROM users WHERE email = ?', (email,))
        if c.fetchone() is not None:
            return jsonify({
                'success': False,
                'message': '이미 사용 중인 이메일입니다'
            }), 400

        # Hash password before storing
        hashed_password = generate_password_hash(password, method='sha256')
        
        # Insert new user
        try:
            c.execute(
                'INSERT INTO users (username, email, password) VALUES (?, ?, ?)',
                (username, email, hashed_password)
            )
            conn.commit()
            user_id = c.lastrowid
        except sqlite3.IntegrityError:
            return jsonify({
                'success': False,
                'message': '이미 사용 중인 이메일입니다'
            }), 400
        
        # Generate JWT token
        token = jwt.encode({
            'user_id': user_id,
            'exp': datetime.utcnow() + timedelta(hours=JWT_EXPIRATION_HOURS)
        }, JWT_SECRET_KEY, algorithm='HS256')
        
        return jsonify({
            'success': True,
            'message': '회원가입이 완료되었습니다',
            'token': token,
            'user': {
                'id': user_id,
                'username': username,
                'email': email
            }
        })
    except Exception as e:
        print('Registration error:', str(e))
        if conn:
            conn.rollback()
        return jsonify({
            'success': False,
            'message': '회원가입 중 오류가 발생했습니다'
        }), 500
    finally:
        if conn:
            conn.close()

@app.route('/auth/login', methods=['POST'])
def login():
    try:
        data = request.get_json()
        email = data.get('email')
        password = data.get('password')
        
        if not all([email, password]):
            return jsonify({
                'success': False,
                'message': '이메일과 비밀번호를 입력해주세요'
            }), 400

        conn = sqlite3.connect('creator_tool.db')
        c = conn.cursor()
        
        # Find user by email
        c.execute('SELECT * FROM users WHERE email = ?', (email,))
        user = c.fetchone()
        
        if user is None:
            return jsonify({
                'success': False,
                'message': '이메일 또는 비밀번호가 일치하지 않습니다'
            }), 401
            
        # Verify password
        if not check_password_hash(user[3], password):
            return jsonify({
                'success': False,
                'message': '이메일 또는 비밀번호가 일치하지 않습니다'
            }), 401

        # Generate JWT token
        token = jwt.encode({
            'user_id': user[0],
            'exp': datetime.utcnow() + timedelta(hours=JWT_EXPIRATION_HOURS)
        }, JWT_SECRET_KEY, algorithm='HS256')
        
        return jsonify({
            'success': True,
            'message': '로그인이 완료되었습니다',
            'token': token,
            'user': {
                'id': user[0],
                'username': user[1],
                'email': user[2]
            }
        })
    except Exception as e:
        print('Login error:', str(e))
        return jsonify({
            'success': False,
            'message': '로그인 중 오류가 발생했습니다'
        }), 500
    finally:
        conn.close()

# Initialize services
youtube_analyzer = YoutubeAnalyzer()
ai_toolkit = AIToolkit()
community_manager = CommunityManager()
trend_service = TrendService(os.getenv('TWITTER_BEARER_TOKEN'))
tool_service = ToolRecommendationService('backend/data/ai_tools_db.json')
api_service = APIIntegrationService()

# 임시 디렉토리 생성
TEMP_DIR = "temp_files"
os.makedirs(TEMP_DIR, exist_ok=True)

def init_db():
    conn = None
    try:
        conn = sqlite3.connect('creator_tool.db')
        c = conn.cursor()
        
        # Users table
        c.execute('''CREATE TABLE IF NOT EXISTS users
            (id INTEGER PRIMARY KEY,
            username TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP)''')
        
        # AI Tools table
        c.execute('''CREATE TABLE IF NOT EXISTS ai_tools
            (id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            category TEXT NOT NULL,
            description TEXT,
            pricing_type TEXT,
            base_price REAL,
            api_available BOOLEAN,
            website_url TEXT,
            features TEXT,
            use_cases TEXT,
            tutorials TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP)''')
        
        # Tool Combinations table
        c.execute('''CREATE TABLE IF NOT EXISTS tool_combinations
            (id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            description TEXT,
            tools JSON NOT NULL,
            workflow JSON NOT NULL,
            content_type TEXT NOT NULL,
            user_id INTEGER NOT NULL,
            usage_count INTEGER DEFAULT 0,
            rating REAL DEFAULT 0,
            review_count INTEGER DEFAULT 0,
            is_public BOOLEAN DEFAULT FALSE,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users (id))''')
        
        # Saved Combinations table
        c.execute('''CREATE TABLE IF NOT EXISTS saved_combinations
            (id INTEGER PRIMARY KEY,
            user_id INTEGER NOT NULL,
            combination_id INTEGER NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users (id),
            FOREIGN KEY (combination_id) REFERENCES tool_combinations (id),
            UNIQUE(user_id, combination_id))''')
        
        # Tool Reviews table
        c.execute('''CREATE TABLE IF NOT EXISTS tool_reviews
            (id INTEGER PRIMARY KEY,
            tool_id INTEGER NOT NULL,
            user_id INTEGER NOT NULL,
            rating FLOAT NOT NULL,
            review_text TEXT,
            pros TEXT,
            cons TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (tool_id) REFERENCES ai_tools (id),
            FOREIGN KEY (user_id) REFERENCES users (id))''')
        
        # YouTube Channels table
        c.execute('''CREATE TABLE IF NOT EXISTS youtube_channels
            (id INTEGER PRIMARY KEY,
            channel_id TEXT UNIQUE,
            title TEXT,
            subscriber_count INTEGER,
            video_count INTEGER,
            avg_views INTEGER,
            last_analyzed TIMESTAMP)''')
        
        conn.commit()
        print('Database initialized successfully')
    except Exception as e:
        print('Database initialization error:', str(e))
        if conn:
            conn.rollback()
        raise e
    finally:
        if conn:
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





# 서버 종료 시 임시 파일 정리
def cleanup_temp_files(error=None):
    if os.path.exists(TEMP_DIR):
        shutil.rmtree(TEMP_DIR)
    return error

# 도구 조합 관련 엔드포인트
@app.route('/api/tools/combinations', methods=['GET'])
def get_tool_combinations():
    try:
        conn = sqlite3.connect('creator_tool.db')
        c = conn.cursor()
        
        # 기본적으로 공개된 조합만 반환
        query = "SELECT * FROM tool_combinations WHERE is_public = 1"
        
        # 사용자 ID가 제공된 경우 해당 사용자의 비공개 조합도 포함
        user_id = request.args.get('user_id')
        params = []
        if user_id:
            query = "SELECT * FROM tool_combinations WHERE is_public = 1 OR user_id = ?"
            params.append(user_id)
            
        c.execute(query, params)
        combinations = c.fetchall()
        
        result = []
        for combo in combinations:
            combo_data = {
                'id': combo[0],
                'name': combo[1],
                'description': combo[2],
                'tools': json.loads(combo[3]),
                'workflow': json.loads(combo[4]),
                'user_id': combo[5],
                'created_at': combo[6],
                'updated_at': combo[7],
                'is_public': bool(combo[8])
            }
            result.append(combo_data)
            
        return jsonify({'success': True, 'combinations': result})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/tools/combinations/<int:combo_id>', methods=['GET'])
def get_tool_combination(combo_id):
    try:
        conn = sqlite3.connect('creator_tool.db')
        c = conn.cursor()
        
        c.execute("SELECT * FROM tool_combinations WHERE id = ?", (combo_id,))
        combo = c.fetchone()
        
        if not combo:
            return jsonify({'success': False, 'error': 'Combination not found'}), 404
            
        combo_data = {
            'id': combo[0],
            'name': combo[1],
            'description': combo[2],
            'tools': json.loads(combo[3]),
            'workflow': json.loads(combo[4]),
            'user_id': combo[5],
            'created_at': combo[6],
            'updated_at': combo[7],
            'is_public': bool(combo[8])
        }
            
        return jsonify({'success': True, 'combination': combo_data})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/tools/combinations', methods=['POST'])
def create_tool_combination():
    try:
        data = request.get_json()
        
        if not all(k in data for k in ['name', 'description', 'tools', 'workflow', 'user_id']):
            return jsonify({'success': False, 'error': 'Missing required fields'}), 400
            
        now = datetime.utcnow().isoformat()
        
        conn = sqlite3.connect('creator_tool.db')
        c = conn.cursor()
        
        c.execute('''
            INSERT INTO tool_combinations 
            (name, description, tools, workflow, user_id, created_at, updated_at, is_public)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            data['name'],
            data['description'],
            json.dumps(data['tools']),
            json.dumps(data['workflow']),
            data['user_id'],
            now,
            now,
            data.get('is_public', False)
        ))
        
        combo_id = c.lastrowid
        conn.commit()
        
        return jsonify({
            'success': True,
            'id': combo_id,
            'message': 'Tool combination created successfully'
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/tools/combinations/<int:combo_id>', methods=['PUT'])
def update_tool_combination(combo_id):
    try:
        data = request.get_json()
        
        conn = sqlite3.connect('creator_tool.db')
        c = conn.cursor()
        
        # 먼저 조합이 존재하는지 확인
        c.execute("SELECT user_id FROM tool_combinations WHERE id = ?", (combo_id,))
        existing = c.fetchone()
        
        if not existing:
            return jsonify({'success': False, 'error': 'Combination not found'}), 404
            
        # 사용자가 이 조합의 소유자인지 확인
        if existing[0] != data.get('user_id'):
            return jsonify({'success': False, 'error': 'Unauthorized'}), 403
            
        update_fields = []
        params = []
        
        if 'name' in data:
            update_fields.append('name = ?')
            params.append(data['name'])
        if 'description' in data:
            update_fields.append('description = ?')
            params.append(data['description'])
        if 'tools' in data:
            update_fields.append('tools = ?')
            params.append(json.dumps(data['tools']))
        if 'workflow' in data:
            update_fields.append('workflow = ?')
            params.append(json.dumps(data['workflow']))
        if 'is_public' in data:
            update_fields.append('is_public = ?')
            params.append(data['is_public'])
            
        update_fields.append('updated_at = ?')
        params.append(datetime.utcnow().isoformat())
        
        params.append(combo_id)  # WHERE 절을 위한 파라미터
        
        query = f"UPDATE tool_combinations SET {', '.join(update_fields)} WHERE id = ?"
        c.execute(query, params)
        conn.commit()
        
        return jsonify({
            'success': True,
            'message': 'Tool combination updated successfully'
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/tools/combinations/<int:combo_id>', methods=['DELETE'])
def delete_tool_combination(combo_id):
    try:
        user_id = request.args.get('user_id')
        if not user_id:
            return jsonify({'success': False, 'error': 'User ID required'}), 400
            
        conn = sqlite3.connect('creator_tool.db')
        c = conn.cursor()
        
        # 먼저 조합이 존재하는지 확인
        c.execute("SELECT user_id FROM tool_combinations WHERE id = ?", (combo_id,))
        existing = c.fetchone()
        
        if not existing:
            return jsonify({'success': False, 'error': 'Combination not found'}), 404
            
        # 사용자가 이 조합의 소유자인지 확인
        if existing[0] != user_id:
            return jsonify({'success': False, 'error': 'Unauthorized'}), 403
            
        c.execute("DELETE FROM tool_combinations WHERE id = ?", (combo_id,))
        conn.commit()
        
        return jsonify({
            'success': True,
            'message': 'Tool combination deleted successfully'
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5003))
    app.run(host='0.0.0.0', port=port)