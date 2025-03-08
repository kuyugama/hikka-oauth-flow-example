import time
import webbrowser
from urllib.parse import urlencode, urlparse, parse_qs

import config


def open_browser():
    query = urlencode(
        dict(
            reference=config.CLIENT_REFERENCE,
            scope=",".join(["user-details", "read:watchlist"]),
        )
    )

    webbrowser.open(f"https://hikka.io/oauth?" + query, )
    # Виклик верхньої функції виконує логування з іншого потоку/процесу,
    # тому потрібно почекати, поки вона це зробить, щоб не зламати вивід подальших функцій
    time.sleep(0.2)


def get_request_reference():
    while True:
        url = input("Введіть посилання на яке вас переспрямував hikka.io: ")

        result = urlparse(url)

        if result.query == "":
            return url

        query = parse_qs(result.query)

        if "reference" not in query:
            print("Посилання переспрямування не містить reference")
            continue

        if not query["reference"]:
            print("Посилання переспрямування містить порожній reference")
            continue

        return query["reference"][0]
