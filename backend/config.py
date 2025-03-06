from flask_cors import CORS

def configure_cors(app):
    CORS(app, 
         resources={
             r"/*": {
                 "origins": ["http://localhost:8092"],
                 "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
                 "allow_headers": ["Content-Type", "Authorization", "Accept"],
                 "expose_headers": ["Content-Type", "Authorization"],
                 "supports_credentials": True
             }
         })
