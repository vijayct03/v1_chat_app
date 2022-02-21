import requests
import json


def get_token(username, password):
    app_url = "http://localhost:8000/api-token-auth/"
    data = {"username": username, "password": password}
    response = requests.post(app_url, data)
    return response


def test_login():
    response = get_token("User3", "Test3@123")
    assert response.status_code == 200
    assert response.text is not None
    print("\tUser successfully logged in.")


def test_create_user_by_normal_user():
    """
    Create a new user by using normal user.
    """
    token_res = get_token("User3", "Test3@123")
    app_url = "http://localhost:8000/group_chat/users"
    payload = {"username": "Test1", "password": "Sample@123", "email": "Test1@gmail.com"}
    headers = {
        'Authorization': f'Bearer {token_res.json()["token"]}',
        'Content-Type': 'application/json'
    }
    response = requests.request("POST", app_url, headers=headers, data=payload)
    assert response.status_code == 401
    print("User doesn't have permission.")


def test_create_user_by_admin():
    token_res = get_token("admin", "Admin@123")
    app_url = "http://localhost:8000/group_chat/users"
    payload = json.dumps({
        "username": "Test1",
        "password": "Sample@123",
        "email": "Test1@gmail.com"
    })
    headers = {
        'Authorization': f'Bearer {token_res.json()["token"]}',
        'Content-Type': 'application/json'
    }
    response = requests.post(app_url, data=payload, headers=headers)
    assert response.status_code == 200


def test_edit_user_by_admin():
    token_res = get_token("admin", "Admin@123")
    app_url = "http://localhost:8000/group_chat/users?user_name=Test1"
    payload = json.dumps({
        "username": "Test11",
        "password": "Sample@123",
        "email": "Test11@gmail.com"
    })
    headers = {
        'Authorization': f'Bearer {token_res.json()["token"]}',
        'Content-Type': 'application/json'
    }
    response = requests.put(app_url, data=payload, headers=headers)
    assert response.status_code == 200
    print("User edited successfully.")


def test_create_group():
    token_res = get_token("User3", "Test3@123")
    url = "http://localhost:8000/group_chat/groups"
    payload = json.dumps({
        "group_name": "Test1"
    })
    headers = {
        'Authorization': f'Bearer {token_res.json()["token"]}',
        'Content-Type': 'application/json'
    }
    response = requests.request("POST", url, headers=headers, data=payload)
    assert response.status_code == 200


def test_add_users_to_group():
    token_res = get_token("User3", "Test3@123")
    url = "http://localhost:8000/group_chat/group_users/Test1?user=Test11"

    payload = ""
    headers = {
        'Authorization': f'Bearer {token_res.json()["token"]}',
        'Content-Type': 'application/json'
    }

    response = requests.request("POST", url, headers=headers, data=payload)
    assert response.status_code == 200


def test_send_msg():
    token_res = get_token("User3", "Test3@123")
    url = "http://localhost:8000/group_chat/message/send?group_name=Test1"

    payload = json.dumps({"text": "Hi, This is Testing API."})
    headers = {
        'Authorization': f'Bearer {token_res.json()["token"]}',
        'Content-Type': 'application/json'
    }

    response = requests.request("POST", url, headers=headers, data=payload)
    assert response.status_code == 200


def test_like_msg():
    token_res = get_token("Test11", "Sample@123")
    msg_url = "http://localhost:8000/group_chat/message/send?group_name=Test1"
    payload = json.dumps({"text": "Hi, This is Testing API."})
    headers = {
        'Authorization': f'Bearer {token_res.json()["token"]}',
        'Content-Type': 'application/json'
    }
    response = requests.request("POST", msg_url, headers=headers, data=payload)

    url = f"http://localhost:8000/group_chat/messages/emotion?msg_id={response.json().get('id')}"
    payload = json.dumps({"emotions": "LIKED"})
    response = requests.request("POST", url, headers=headers, data=payload)
    assert response.status_code == 200

def test_delete_group():
    token_res = get_token("User3", "Test3@123")
    url = "http://localhost:8000/group_chat/groups/Test1"

    headers = {
        'Authorization': f'Bearer {token_res.json()["token"]}',
        'Content-Type': 'application/json'
    }
    response = requests.request("DELETE", url, headers=headers)
    assert response.status_code == 200