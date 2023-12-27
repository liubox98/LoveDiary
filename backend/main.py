import secrets
from datetime import timedelta
from flask_cors import CORS
from pymongo import MongoClient
from werkzeug.security import generate_password_hash
from flask import Flask, jsonify, request, make_response
from flask_jwt_extended import JWTManager, create_access_token

app = Flask(__name__)
CORS(app, resources={r'/*': {'origins': '*'}})
app.config['JWT_SECRET_KEY'] = secrets.token_urlsafe(32)
jwt = JWTManager(app)

# MongoDB 配置
# client = MongoClient(f"mongodb+srv://liubo:abc123!@cluster1.cbbd34h.mongodb.net/hamburger?retryWrites=true&w=majority") # mongodb云数数据库
client = MongoClient("mongodb://root:123456@127.0.0.1:27017/hamburger?authSource=admin&retryWrites=true&w=majority", connect=False)
mongo_db = client.get_database()

# 模型
class User:
    def __init__(self, username, password):
        self.username = username
        self.password = generate_password_hash(password, method='sha256')

class Action:
    def __init__(self, author:str, action:str, description:str, time:str, image:list):
        self.author = author
        self.action = action
        self.description = description
        self.time = time
        self.image = image

# 路由
@app.route('/token', methods=['POST'])
def login_for_access_token():
    print('token -- POST')
    data = request.json
    username = data.get('username')
    password = data.get('password')
    user = mongo_db.user.find_one({'username': username})
    if user:
        if password == user.get('password', ''):
            access_token = create_access_token(identity=username, expires_delta=timedelta(minutes=30))
            print('user:', username, 'access_token:', access_token)
            return jsonify({'user': username, 'access_token': access_token })
    print('user:', user)
    return make_response(jsonify({'error': 'Invalid username or password'}), 401)

@app.route('/activities', methods=['POST'])
def create_activity():
    print('activities -- POST',)
    data = request.json
    mongo_db.activities.insert_one(data)
    return jsonify({'message': 'Activity created successfully'}), 201

@app.route('/activities', methods=['GET'])
def read_activities():
    print('activities -- GET')
    activities = mongo_db.activities.find({}, {'_id': False})
    return jsonify(list(activities))
