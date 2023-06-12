import typing as tp

import requests


class Session(requests.Session):
    """
    Сессия.

    :param base_url: Базовый адрес, на который будут выполняться запросы.
    :param timeout: Максимальное время ожидания ответа от сервера.
    :param max_retries: Максимальное число повторных запросов.
    :param backoff_factor: Коэффициент экспоненциального нарастания задержки.
    """

    def __init__(
            self,
            base_url: str,
            timeout: float = 5.0,
            max_retries: int = 3,
            backoff_factor: float = 0.3,
    ) -> None:
        pass

    def get(self, url, **kwargs: tp.Any) -> requests.Response:
        pass

    def post(self, url, data=None, json=None, **kwargs: tp.Any) -> requests.Response:
        pass
