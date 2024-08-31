# -*- coding: utf-8 -*-
from flask import Flask, request, jsonify
import csv
import os

app = Flask(__name__)

# ѕуть к файлу CSV
CSV_FILE = 'students.csv'

def read_students():
    if not os.path.exists(CSV_FILE):
        return []
    with open(CSV_FILE, mode='r', newline='') as file:
        reader = csv.DictReader(file)
        return list(reader)

def write_students(students):
    with open(CSV_FILE, mode='w', newline='') as file:
        fieldnames = ['id', 'first_name', 'last_name', 'age']
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(students)

def generate_new_id():
    students = read_students()
    if not students:
        return 1
    max_id = max(int(student['id']) for student in students)
    return max_id + 1
@app.route('/')
def index():
    return "Welcome to the Student Management API!"
@app.route('/students', methods=['GET'])
def get_all_students():
    students = read_students()
    return jsonify(students)

@app.route('/students/<int:student_id>', methods=['GET'])
def get_student_by_id(student_id):
    students = read_students()
    student = next((s for s in students if int(s['id']) == student_id), None)
    if student:
        return jsonify(student)
    return jsonify({"error": "Student not found"}), 404

@app.route('/students/lastname/<last_name>', methods=['GET'])
def get_student_by_last_name(last_name):
    students = read_students()
    filtered_students = [s for s in students if s['last_name'].lower() == last_name.lower()]
    if filtered_students:
        return jsonify(filtered_students)
    return jsonify({"error": "No students found with that last name"}), 404

@app.route('/students', methods=['POST'])
def create_student():
    data = request.json
    required_fields = ['first_name', 'last_name', 'age']
    
    if not all(field in data for field in required_fields):
        return jsonify({"error": "Missing fields"}), 400

    new_id = generate_new_id()
    new_student = {
        'id': new_id,
        'first_name': data['first_name'],
        'last_name': data['last_name'],
        'age': data['age']
    }
    
    students = read_students()
    students.append(new_student)
    write_students(students)
    return jsonify(new_student), 201

@app.route('/students/<int:student_id>', methods=['PUT'])
def update_student(student_id):
    data = request.json
    required_fields = ['first_name', 'last_name', 'age']
    
    if not all(field in data for field in required_fields):
        return jsonify({"error": "Missing fields"}), 400

    students = read_students()
    student = next((s for s in students if int(s['id']) == student_id), None)
    if not student:
        return jsonify({"error": "Student not found"}), 404

    student['first_name'] = data['first_name']
    student['last_name'] = data['last_name']
    student['age'] = data['age']
    
    write_students(students)
    return jsonify(student)

@app.route('/students/<int:student_id>', methods=['PATCH'])
def update_student_age(student_id):
    data = request.json
    if 'age' not in data:
        return jsonify({"error": "Missing age field"}), 400

    students = read_students()
    student = next((s for s in students if int(s['id']) == student_id), None)
    if not student:
        return jsonify({"error": "Student not found"}), 404

    student['age'] = data['age']
    write_students(students)
    return jsonify(student)

@app.route('/students/<int:student_id>', methods=['DELETE'])
def delete_student(student_id):
    students = read_students()
    student = next((s for s in students if int(s['id']) == student_id), None)
    if not student:
        return jsonify({"error": "Student not found"}), 404

    students = [s for s in students if int(s['id']) != student_id]
    write_students(students)
    return jsonify({"message": "Student deleted successfully"})

if __name__ == '__main__':
    app.run(debug=True)
