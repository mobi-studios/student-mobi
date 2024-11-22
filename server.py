from flask import Flask, request, jsonify, session
from flask_socketio import SocketIO, emit
from werkzeug.security import generate_password_hash, check_password_hash
import json
import os

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # 设置会话秘钥
socketio = SocketIO(app)

class Classroom:
    def __init__(self):
        self.students = []
        self.teachers = []
        self.knowledge_points = []

    def add_student(self, student_id):
        self.students.append(student_id)

    def add_teacher(self, teacher_id):
        self.teachers.append(teacher_id)

    def add_knowledge_point(self, point):
        self.knowledge_points.append(point)

    def get_knowledge_points(self):
        return self.knowledge_points


classroom = Classroom()

# 加载用户数据
def load_users():
    if not os.path.exists('users.json'):
        return {"students": {}, "teachers": {}}
    with open('users.json') as f:
        return json.load(f)

# 保存用户数据
def save_users(data):
    with open('users.json', 'w') as f:
        json.dump(data, f)

users_data = load_users()

@app.route('/register', methods=['POST'])
def register():
    data = request.json
    role = data.get('role')
    id = data.get('id')
    password = data.get('password')

    if role == 'student':
        if id in users_data['students']:
            return jsonify({"message": "Student ID already exists", "status": "error"}), 400
        hashed_password = generate_password_hash(password)
        users_data['students'][id] = hashed_password
        classroom.add_student(id)
    elif role == 'teacher':
        if id in users_data['teachers']:
            return jsonify({"message": "Teacher ID already exists", "status": "error"}), 400
        hashed_password = generate_password_hash(password)
        users_data['teachers'][id] = hashed_password
        classroom.add_teacher(id)

    save_users(users_data)
    return jsonify({"message": "Registered successfully!", "status": "success"})

@app.route('/login', methods=['POST'])
def login():
    data = request.json
    role = data.get('role')
    id = data.get('id')
    password = data.get('password')

    if role == 'student':
        if id in users_data['students'] and check_password_hash(users_data['students'][id], password):
            session['user'] = {'id': id, 'role': 'student'}  # 保存用户会话信息
            return jsonify({"message": "Login successful!", "status": "success"})
    elif role == 'teacher':
        if id in users_data['teachers'] and check_password_hash(users_data['teachers'][id], password):
            session['user'] = {'id': id, 'role': 'teacher'}  # 保存用户会话信息
            return jsonify({"message": "Login successful!", "status": "success"})

    return jsonify({"message": "Invalid credentials", "status": "error"}), 401

@app.route('/logout', methods=['POST'])
def logout():
    session.pop('user', None)  # 清除用户会话
    return jsonify({"message": "Logout successful!", "status": "success"})

@app.route('/knowledge', methods=['POST'])
def send_knowledge():
    data = request.json
    point = data.get('point')
    role = data.get('role')

    if role == 'teacher':
        classroom.add_knowledge_point(point)
        # 通过SocketIO广播新知识点
        socketio.emit('new_knowledge_point', {'point': point}, broadcast=True)
        return jsonify({"message": "Knowledge point added!", "status": "success"})
    
    return jsonify({"message": "Only teachers can add knowledge points.", "status": "error"}), 403

@app.route('/knowledge', methods=['GET'])
def get_knowledge():
    return jsonify({"knowledge_points": classroom.get_knowledge_points(), "status": "success"})

@socketio.on('broadcast_message')
def handle_broadcast_message(data):
    message = data['message']
    emit('receive_message', {'message': message}, broadcast=True)

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=5000)
