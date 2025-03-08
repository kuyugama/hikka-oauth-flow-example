from requests import get, post, Response

import config
import common

def handle_response_error(resp: Response, message: str, status: int = 0):
    if resp.status_code == 200:
        return

    print(message)
    print("Status code:", response.status_code)
    if response.status_code < 500:
        print("Error response", response.json())

    exit(status)

# Спрямовую користувача на https://hikka.io/oauth?reference=CLIENT_REFERENCE&scope=SCOPE
common.open_browser()

# Витягую ідентифікатор запиту на токен з посилання переспрямування
reference = common.get_request_reference()

# Отримую токен доступу
response = post(
    "https://api.hikka.io/auth/token",
    json=dict(request_reference=reference, client_secret=config.CLIENT_SECRET),
)
handle_response_error(response, "Не вдалось отримати токен доступу", 1)

token = response.json()

headers = dict(
    Auth=token["secret"]
)

# Отримую інформацію про токен
response = get("https://api.hikka.io/auth/token/info", headers=headers)
handle_response_error(response, "Не вдалось отримати інформацію про токен", 2)

client = response.json()["client"]

# Отримую дані користувача і подовжую дію токену доступу
response = get("https://api.hikka.io/user/me", headers=headers)
handle_response_error(response, "Не вдалось отримати дані користувача", 3)

user = response.json()
print("Успішно авторизовано користувача", user["username"], "в клієнті", client["name"])
