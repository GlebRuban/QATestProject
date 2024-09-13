import os
import requests
from dotenv import load_dotenv, find_dotenv

# Загружаем переменные окружения из файла .env
load_dotenv(find_dotenv())
GITHUB_API_URL = os.getenv('api_url')
USERNAME = os.getenv('username')
TOKEN = os.getenv('token')
REPO_NAME = os.getenv('repo_name')
# Авторизация для API GitHub
auth = (USERNAME, TOKEN)


def create_repository(repo_name):
    url = f"{GITHUB_API_URL}/user/repos"
    headers = {'Accept': 'application/vnd.github.v3+json'}
    data = {
        "name": repo_name,
        "private": False
    }

    response = requests.post(url, json=data, headers=headers, auth=auth)

    if response.status_code == 201:
        print(f"Репозиторий '{repo_name}' успешно создан.")
    else:
        print(f"Ошибка при создании репозитория: {response.status_code}, {response.json()}")


def check_repository_exists(repo_name):
    url = f"{GITHUB_API_URL}/users/{USERNAME}/repos"
    response = requests.get(url, auth=auth)

    if response.status_code == 200:
        repos = response.json()
        repo_names = [repo['name'] for repo in repos]

        if repo_name in repo_names:
            print(f"Репозиторий '{repo_name}' существует.")
        else:
            print(f"Репозиторий '{repo_name}' не найден.")
    else:
        print(f"Ошибка при получении списка репозиториев: {response.status_code}, {response.json()}")

def delete_repository(repo_name):
    url = f"{GITHUB_API_URL}/repos/{USERNAME}/{repo_name}"
    response = requests.delete(url, auth=auth)
    if response.status_code == 204:
        print(f"Репозиторий '{repo_name}' успешно удален.")
    else:
        print(f"Ошибка при удалении репозитория: {response.status_code}, {response.json()}")

if __name__ == "__main__":
    # Шаг 1: Создание репозитория
    create_repository(REPO_NAME)

    # Шаг 2: Проверка существования репозитория
    check_repository_exists(REPO_NAME)

    # Шаг 3: Удаление репозитория
    delete_repository(REPO_NAME)