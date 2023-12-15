import secrets
from flask_cors import CORS
from pymongo import MongoClient
from flask_jwt_extended import JWTManager
from flask import Flask, jsonify, request, make_response
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from werkzeug.security import generate_password_hash
from datetime import timedelta

app = Flask(__name__)
CORS(app, resources={r'/*': {'origins': '*'}})
app.config['JWT_SECRET_KEY'] = secrets.token_urlsafe(32)
jwt = JWTManager(app)

# MongoDB 配置
client = MongoClient(f"mongodb+srv://liubo:abc123!@cluster1.cbbd34h.mongodb.net/hamburger?retryWrites=true&w=majority")
mongo_db = client.get_database()

# 模型
class User:
    def __init__(self, username, password):
        self.username = username
        self.password = generate_password_hash(password, method='sha256')

class Action:
    def __init__(self, action, description):
        self.action = action
        self.description = description

# 路由
@app.route('/token', methods=['POST'])
def login_for_access_token():
    data = request.json
    username = data.get('username')
    password = data.get('password')
    user = mongo_db.user.find_one({'username': username})
    if user:
        if password == user.get('password', ''):
            access_token = create_access_token(identity=username, expires_delta=timedelta(minutes=30))
            return jsonify({'access_token': access_token, 'token_type': 'bearer'})
    return make_response(jsonify({'error': 'Invalid username or password'}), 401)


@app.route('/users/me', methods=['GET'])
@jwt_required()
def read_users_me():
    current_user = get_jwt_identity()
    user = mongo_db.user.find_one({'username': current_user}, {'_id': False, 'password': False})
    return jsonify(user)

@app.route('/activities', methods=['POST'])
@jwt_required()
def create_activity():
    data = request.json
    activity = Action(**data)
    mongo_db.activities.insert_one({'action': activity.action, 'description': activity.description})
    return jsonify({'message': 'Activity created successfully'}), 201

@app.route('/activities', methods=['GET'])
@jwt_required()
def read_activities():
    activities = mongo_db.activities.find({}, {'_id': False})
    return jsonify(list(activities))

if __name__ == '__main__':
    app.run(host='10.10.20.24', port=8000)
