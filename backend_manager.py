import json
import urllib.parse
import requests

from scrt import BACKEND_HOST, BACKEND_PORT

backend_url = f'http://{BACKEND_HOST}:{BACKEND_PORT}'
project_id = None

def encode_url_str(url_str: str):
    return urllib.parse.quote(url_str)

def get_request(route):
    response = requests.get(f'{backend_url}/{encode_url_str(route)}')
    if response.status_code == 200:
        try:
            return response.json()
        except requests.exceptions.JSONDecodeError:
            return {"error": "Invalid JSON response"}
    else:
        print(f"Failed {response.status_code}: {response.text}")
        return None

def post_request(route, data=None, params=None):
    response = requests.post(f'{backend_url}/{encode_url_str(route)}', json=data, params=params)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Failed {response.status_code}: {response.text}")
        return None

def delete_request(route):
    response = requests.delete(f'{backend_url}/{encode_url_str(route)}')
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Failed {response.status_code}: {response.text}")
        return None

def put_request(route, data=None):
    response = requests.put(f'{backend_url}/{encode_url_str(route)}', json=data)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Failed {response.status_code}: {response.text}")
        return None


def get_available_projects():
    return get_request('get_project_ids')


def create_project(custom_id: str=None):
    return post_request('create_project', params={'custom_id': custom_id})


def delete_project():
    if project_id:
        return delete_request(f'{project_id}/delete_project')
    else:
        return None

def upload_file(contents, filename: str):
    if project_id:
        return post_request(f'{project_id}/upload_file', data={'contents': contents, 'filename': filename})
    else:
        return None

def get_uploaded_files():
    if project_id:
        return get_request(f'{project_id}/get_uploaded_files')
    else:
        return None

def add_message(chat: str, text: str):
    if project_id:
        return put_request(f'{project_id}/add_message', data={'chat': chat, 'text': text})
    else:
        return None

def get_chat_history(selected_chat: str):
    if project_id:
        return get_request(f'{project_id}/get_chat_history/{selected_chat}')
    else:
        return None

def get_dashboard_payload():
    if project_id:
        return get_request(f'{project_id}/get_dashboard_payload')
    else:
        return None

def get_available_chats():
    if project_id:
        return get_request(f'{project_id}/get_chats')
    else:
        return None

def get_code(code_name: str = "latest"):
    if project_id:
        return get_request(f'{project_id}/get_code/{code_name}')
    else:
        return None

def get_code_names():
    if project_id:
        return get_request(f'{project_id}/get_code_names')
    else:
        return None