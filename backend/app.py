from flask import Flask, jsonify, request
from flask_cors import CORS
import os
import sqlite3

app = Flask(__name__)
CORS(app)

def init_db():
    conn = sqlite3.connect('emails.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS emails (id INTEGER PRIMARY KEY, email TEXT)''')
    conn.commit()
    conn.close()

init_db()

@app.route('/')
def hello():
    return "Hello from Heroku!"

@app.route('/api/features')
def get_features():
    features = [
        "유튜브 트렌드 분석",
        "AI 기반 영상 편집",
        "자동 자막 생성",
        "썸네일 자동 생성"
    ]
    return jsonify(features)

@app.route('/api/trends')
def get_trends():
    trends = [
        {"title": "짧은 쇼츠 영상", "views": "1.2M"},
        {"title": "AI 튜토리얼", "views": "850K"},
        {"title": "DIY 공예", "views": "600K"}
    ]
    return jsonify(trends)

@app.route('/api/analyze', methods=['POST'])
def analyze_channel():
    url = request.json.get('url')
    if url:
        # 나중에 YouTube API로 대체
        analysis = {
            "keywords": ["트렌드", "숏츠", "AI"],
            "hashtags": ["#Shorts", "#YouTube", "#Trend"],
            "predicted_views": "500K"
        }
        return jsonify(analysis), 200
    return jsonify({"message": "URL 필요!"}), 400

@app.route('/api/emails', methods=['POST'])
def save_email():
    email = request.json.get('email')
    if email:
        conn = sqlite3.connect('emails.db')
        c = conn.cursor()
        c.execute("INSERT INTO emails (email) VALUES (?)", (email,))
        conn.commit()
        conn.close()
        return jsonify({"message": "이메일 저장 성공!"}), 200
    return jsonify({"message": "이메일 필요!"}), 400

@app.route('/api/emails', methods=['GET'])
def get_emails():
    conn = sqlite3.connect('emails.db')
    c = conn.cursor()
    c.execute("SELECT email FROM emails")
    emails = [row[0] for row in c.fetchall()]
    conn.close()
    return jsonify(emails)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5001))
    app.run(host='0.0.0.0', port=port, debug=True)