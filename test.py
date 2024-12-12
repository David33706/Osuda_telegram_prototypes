import requests

# Настройка прокси
proxies = {
    "http": "95.216.36.231:8889",
    "https": "95.216.36.231:8889"
}

# Тестовый URL (например, Google)
url = "https://www.youtube.com/"

# Заголовки для запросов (при необходимости)
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
}

try:
    # Отправка запроса через прокси
    response = requests.get(url, headers=headers, proxies=proxies, timeout=10)

    # Проверка статуса ответа
    if response.status_code == 200:
        print("Запрос успешно выполнен через прокси.")
        print(response.text[:500])  # Вывод первых 500 символов ответа для проверки
    else:
        print(f"Ошибка запроса: {response.status_code}")

except requests.exceptions.ProxyError:
    print("Ошибка подключения к прокси.")

except requests.exceptions.Timeout:
    print("Превышено время ожидания ответа.")

except Exception as e:
    print(f"Произошла ошибка: {e}")
