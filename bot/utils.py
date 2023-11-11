import requests

from config import HTTP_URL

bagcheck = False


def auth_signin(login, password):
    url = f"{HTTP_URL}auth/signin"
    payload = {"username": str(login), "password": str(password)}
    files = []
    headers = {}
    response = requests.request("POST", url, headers=headers, data=payload, files=files)
    if bagcheck:
        print(response.text)

    return response


def auth_refresh_token(temp_token):
    url = f"{HTTP_URL}auth/refresh_token"
    headers = {"Authorization": f"Bearer {temp_token}"}

    response = requests.post(url, headers=headers)
    if bagcheck:
        print(response.text)

    return response


def users_profile(curr_token):
    url = f"{HTTP_URL}users/profile"
    headers = {"Authorization": f"Bearer {curr_token}"}

    response = requests.get(url, headers=headers)
    if bagcheck:
        print(response.text)

    return response


def users(firstname, lastname, patronymic, curr_token):
    url = f"{HTTP_URL}users/"

    payload = {"firstname": firstname, "lastname": lastname, "patronymic": patronymic}

    headers = {"Authorization": f"Bearer {curr_token}"}
    response = requests.put(url, headers=headers, json=payload)
    if bagcheck:
        print(response.text)
        print(response)

    return response


def users_employees_all(curr_token):
    url = f"{HTTP_URL}users/employees/all"
    headers = {"Authorization": f"Bearer {curr_token}"}

    response = requests.get(url, headers=headers)
    if bagcheck:
        print(response.text)

    return response


def offices_all(curr_token):
    url = f"{HTTP_URL}offices/all"
    headers = {"Authorization": f"Bearer {curr_token}"}

    response = requests.get(url, headers=headers)
    if bagcheck:
        print(response.text)

    return response


def tasks():
    url = f"{HTTP_URL}tasks/"

    response = requests.get(url)
    if bagcheck:
        print(response.text)

    return response


def tasks_id(id):
    url = f"{HTTP_URL}tasks/?employee_id={id}"

    response = requests.get(url)
    if bagcheck:
        print(response.text)

    return response


def accept_task(id, token):
    url = f"{HTTP_URL}tasks/accept_task/?task_id={id}"

    headers = {"Authorization": f"Bearer {token}"}

    response = requests.put(url, headers=headers)
    if bagcheck:
        print(response.text)

    return response


def complete_task(id, token):
    url = f"{HTTP_URL}tasks/completed"
    mark = 0
    review = ""
    payload = {"id": id, "feedback_value": mark, "feedback_description": review}
    headers = {"Authorization": f"Bearer {token}"}

    response = requests.post(url, headers=headers, json=payload)
    if bagcheck:
        print(response.text)

    return response


def tasks_history():
    url = f"{HTTP_URL}tasks/history"

    response = requests.get(url)
    if bagcheck:
        print(response.text)

    return response


def tasks_history_id(id):
    url = f"{HTTP_URL}tasks/history/?employee_id={id}"

    response = requests.get(url)
    if bagcheck:
        print(response.text)

    return response


def cancelled(text, token, id):
    url = f"{HTTP_URL}tasks/cancelled"

    payload = {"id": id, "feedback_description": text}
    headers = {"Authorization": f"Bearer {token}"}

    response = requests.post(url, headers=headers, json=payload)
    if bagcheck:
        print(response.text)

    return response
