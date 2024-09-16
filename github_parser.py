import random
from time import sleep

import requests
import os

# GitHub API URL для поиска репозиториев
GITHUB_API_URL = "https://api.github.com/search/repositories"


# Функция для поиска репозиториев по ключевым словам с поддержкой пагинации
def search_repositories(query, sort_by="stars", order="desc", per_page=100, max_results=1000):
    repositories = []
    page = 1
    while len(repositories) < max_results:
        params = {
            "q": query,
            "sort": sort_by,
            "order": order,
            "per_page": per_page,
            "page": page
        }

        headers = {
            "Accept": "application/vnd.github.v3+json",
            "Authorization": f"token {os.getenv('GITHUB_TOKEN')}"
        }

        response = requests.get(GITHUB_API_URL, params=params, headers=headers)
        if response.status_code == 200:
            items = response.json().get("items", [])
            if not items:
                # Если больше нет результатов, выходим из цикла
                break
            repositories.extend(items)
            print(f"Страница {page} обработана")
            page += 1
            sleep(random.randint(5, 8))
        else:
            print(f"Ошибка: {response.status_code}")
            break

    return repositories[:max_results]  # Возвращаем не более max_results репозиториев


# Функция для записи результатов в README.md в формате Markdown с указанием кодировки UTF-8
def write_to_readme(keywords, repositories, filename="README"):
    with open(filename+"." + keywords + ".md", "w", encoding="utf-8") as f:
        f.write("# Awesome Repositories: " + keywords + "\n | Repository | Stars | Forks | Description |\n---|---|---|----------------|\n")
        for repo in repositories:
            f.write(f"| [{repo['full_name']}]({repo['html_url']}) |")
            f.write(f" {repo['stargazers_count']} |")
            f.write(f" {repo['forks_count']} |")
            f.write(f" 📝: {repo['description'] or 'No description'} |\n")


# Основная функция
def main():
    # Задайте свои ключевые слова
    keywords = input("Введите ключевые слова для поиска репозиториев: ")

    # Поиск репозиториев (максимум 300)
    repositories = search_repositories(query=keywords, max_results=1000)

    # Запись в README.md
    if repositories:
        write_to_readme(keywords.replace(":","_"),repositories)
        print(f"Файл README.{keywords}.md обновлен с {len(repositories)} репозиториями.")
    else:
        print("Не удалось найти репозитории по данному запросу.")


if __name__ == "__main__":
    main()
