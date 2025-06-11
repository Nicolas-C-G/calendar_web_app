import requests

BASE_URL = "http://127.0.0.1:8000"

def test_register_user():
    response = requests.post(f"{BASE_URL}/register", json={
        "username": "external_user",
        "email": "external@example.com",
        "password": "externalpass"
    })
    print("Register:", response.status_code, response.json())

def test_duplicate_user():
    response = requests.post(f"{BASE_URL}/register", json={
        "username": "external_user",
        "email": "another@example.com",
        "password": "pass"
    })
    print("Duplicate Register:", response.status_code, response.json())

def test_login_success():
    response = requests.post(f"{BASE_URL}/login", json={
        "username": "Tester",
        "password": "159753.Tester"
    })
    print("Login:", response.status_code, response.json())
    return response.json().get("token")

def test_login_invalid():
    response = requests.post(f"{BASE_URL}/login", json={
        "username": "fake",
        "password": "fake"
    })
    print("Invalid Login:", response.status_code, response.json())

if __name__ == "__main__":
    print("-----------Register test")
    test_register_user()
    print("-----------Duplicate test")
    test_duplicate_user()
    print("-----------Login test")
    token = test_login_success()
    print("-----------Invalid Login test")
    test_login_invalid()
