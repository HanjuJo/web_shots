from flask import Flask, jsonify, make_response, request
from flask_cors import CORS

app = Flask(__name__)

# Configure CORS
CORS(app,
     resources={
         r"/*": {
             "origins": ["http://localhost:8092"],
             "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
             "allow_headers": ["Content-Type", "Authorization", "Accept", "X-Requested-With"],
             "supports_credentials": True,
             "expose_headers": ["Content-Type", "Authorization"],
             "max_age": 600
         }
     })

@app.after_request
def after_request(response):
    response.headers['Access-Control-Allow-Origin'] = 'http://localhost:8092'
    response.headers['Access-Control-Allow-Credentials'] = 'true'
    response.headers['Access-Control-Allow-Methods'] = 'GET, POST, PUT, DELETE, OPTIONS'
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type, Authorization, Accept'
    return response

@app.route('/test', methods=['GET'])
def test():
    return jsonify({'message': 'Backend server is working!'})

@app.route('/auth/register', methods=['POST'])
def test_register():
    return jsonify({
        'success': True,
        'message': '회원가입이 완료되었습니다',
        'token': 'test_token',
        'user': {
            'id': 1,
            'username': 'testuser',
            'email': 'test@example.com'
        }
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5003, debug=True)
