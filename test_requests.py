# -*- coding: utf-8 -*-
import requests

# URL ������ API

base_url = "http://127.0.0.1:5000/students"

def write_results_to_file(response, file):
    status_code = response.status_code
    try:
        json_data = response.json()
        file.write(f"Response: {json_data}\n\n")
    except requests.exceptions.JSONDecodeError:
        file.write(f"Response (not JSON): {response.text}\n\n")
    file.write(f"Status code: {status_code}\n\n")

def get_all_students():
    response = requests.get(base_url)
    return response

def create_student(data):
    response = requests.post(base_url, json=data)
    return response

def patch_student(student_id, data):
    response = requests.patch(f"{base_url}/{student_id}", json=data)
    return response

def put_student(student_id, data):
    response = requests.put(f"{base_url}/{student_id}", json=data)
    return response

def delete_student(student_id):
    response = requests.delete(f"{base_url}/{student_id}")
    return response

# ������ ������������� �������
with open('results.txt', 'w') as file:
    # �������� ���� ���������
    response = get_all_students()
    write_results_to_file(response, file)
    
    # ������� ���������
    student1 = {'first_name': 'John', 'last_name': 'Doe', 'age': 20}
    student2 = {'first_name': 'Jane', 'last_name': 'Smith', 'age': 22}
    student3 = {'first_name': 'Emma', 'last_name': 'Brown', 'age': 24}
    
    response = create_student(student1)
    write_results_to_file(response, file)
    
    response = create_student(student2)
    write_results_to_file(response, file)
    
    response = create_student(student3)
    write_results_to_file(response, file)
    
    # �������� ���� ���������
    response = get_all_students()
    write_results_to_file(response, file)
    
    # �������� ������� ������� ��������
    response = patch_student(2, {'age': 23})
    write_results_to_file(response, file)
    
    # �������� ���������� � ������ ��������
    response = requests.get(f"{base_url}/2")
    write_results_to_file(response, file)
    
    # �������� ��� � ������� �������� ��������
    response = put_student(3, {'first_name': 'Emily', 'last_name': 'Davis', 'age': 25})
    write_results_to_file(response, file)
    
    # �������� ���������� � ������� ��������
    response = requests.get(f"{base_url}/3")
    write_results_to_file(response, file)
    
    # �������� ���� ���������
    response = get_all_students()
    write_results_to_file(response, file)
    
    # ������� ������� ��������
    response = delete_student(1)
    write_results_to_file(response, file)
    
    # �������� ���� ���������
    response = get_all_students()
    write_results_to_file(response, file)
