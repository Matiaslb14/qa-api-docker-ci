import os

BASE_URL = os.getenv("BASE_URL", "https://jsonplaceholder.typicode.com")
TIMEOUT_SECONDS = float(os.getenv("TIMEOUT_SECONDS", "5"))
RETRIES = int(os.getenv("RETRIES", "1"))  # 1 retry suave => 2 intentos total
