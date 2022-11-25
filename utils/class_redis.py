import redis

import json


class Redis:
    """
    Класс для работы с Redis ключами
    """

    def __init__(self):
        """
        Подключение к Redis
        """
        self.redis_client = redis.StrictRedis(
            host="127.0.0.1",
            port=6379,
            decode_responses=True
        )

    def get_status_code(self):
        """
        Получение статуса html формы
        """
        return json.loads(self.redis_client.get("status_code"))

    def change_status_code_false(self):
        """
        Изменение статуса html формы на False
        """
        self.redis_client.set("status_code", json.dumps(False))

    def change_status_code_true(self):
        """
        Изменение статуса html формы на True
        """
        self.redis_client.set("status_code", json.dumps(True))


r = Redis()
