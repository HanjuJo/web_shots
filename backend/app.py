from flask import Flask, jsonify, request
from flask_cors import CORS
import os
import sqlite3

app = Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": ["https://creatortool.netlify.app", "http://localhost:8081"]}})

# DB 초기화는 남기되, emails 테이블 삭제는 생략
def init_db():
    conn = sqlite3.connect('emails.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS emails (id INTEGER PRIMARY KEY, email TEXT)''')
    conn.commit()
    conn.close()

init_db()  # 기존 데이터 남아있어도 문제없음

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

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5001))
    app.run(host='0.0.0.0', port=port, debug=True)