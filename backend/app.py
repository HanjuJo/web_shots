from flask import Flask, jsonify
from flask_cors import CORS
import os

app = Flask(__name__)
CORS(app)

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

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5001))
    app.run(host='0.0.0.0', port=port, debug=True)