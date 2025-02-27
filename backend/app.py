from flask import Flask, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # 모든 출처 허용 (개발용)

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
    app.run(debug=True, port=5001)