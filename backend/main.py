import secrets
from flask_cors import CORS
from pymongo import MongoClient
from flask_jwt_extended import JWTManager
from werkzeug.security import generate_password_hash
from flask import Flask, jsonify, request, make_response
from flask_jwt_extended import create_access_token, jwt_required
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
    def __init__(self, author:str, action:str, description:str, time:str, image:list):
        self.author = author
        self.action = action
        self.description = description
        self.time = time
        self.image = image

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
            return jsonify({'user': username, 'access_token': access_token })
    return make_response(jsonify({'error': 'Invalid username or password'}), 401)

@app.route('/activities', methods=['POST'])
def create_activity():
    author = request.json.get('author')
    action = request.json.get('action')
    description = request.json.get('description')
    time = request.json.get('time')
    images = request.json.get('image')
    image_urls = []
    for image in images:
        # 将图片数据保存到服务器，这里假设使用了静态目录下的 upload 文件夹
        # 你可能需要根据具体情况修改保存路径
        save_path = f"static/upload/{image['name']}"
        with open(save_path, 'wb') as f:
            f.write(image['url'])
        image_urls.append(save_path)
    activity = Action(author=author, action=action, description=description, time=time, image=image_urls)
    mongo_db.activities.insert_one({
        'author': activity.author,
        'action': activity.action,
        'description': activity.description,
        'time': activity.time,
        'image': activity.image
    })
    return jsonify({'message': 'Activity created successfully'}), 201

@app.route('/activities', methods=['GET'])
# @jwt_required()
def read_activities():
    activities = mongo_db.activities.find({}, {'_id': False})
    return jsonify(list(activities))

if __name__ == '__main__':
    app.run(host='10.10.20.24', port=8000, debug=True)
