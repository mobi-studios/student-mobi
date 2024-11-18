from flask import Flask, request, jsonify
from flask_socketio import SocketIO, emit
import json
import os

app = Flask(__name__)
socketio = SocketIO(app)

class Classroom:
    def __init__(self):
        self.students = []
        self.teachers = []

    def add_student(self, student_id):
        self.students.append(student_id)

    def add_teacher(self, teacher_id):
        self.teachers.append(teacher_id)

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
        users_data['students'][id] = password
    elif role == 'teacher':
        if id in users_data['teachers']:
            return jsonify({"message": "Teacher ID already exists", "status": "error"}), 400
        users_data['teachers'][id] = password

    save_users(users_data)
    classroom.add_student(id) if role == 'student' else classroom.add_teacher(id)
    return jsonify({"message": "Registered successfully!", "status": "success"})

@app.route('/login', methods=['POST'])
def login():
    data = request.json
    role = data.get('role')
    id = data.get('id')
    password = data.get('password')

    if role == 'student':
        if id in users_data['students'] and users_data['students'][id] == password:
            return jsonify({"message": "Login successful!", "status": "success"})
    elif role == 'teacher':
        if id in users_data['teachers'] and users_data['teachers'][id] == password:
            return jsonify({"message": "Login successful!", "status": "success"})

    return jsonify({"message": "Invalid credentials", "status": "error"}), 401


@socketio.on('broadcast_message')
def handle_broadcast_message(message):
    emit('receive_message', message, broadcast=True)

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=22, debug=True)
