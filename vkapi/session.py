import typing as tp

import requests
from requests.adapters import HTTPAdapter, Retry


class TimeoutHTTPAdapter(HTTPAdapter):
    def __init__(self, timeout, *args, **kwargs):
        self.timeout = timeout
        if "timeout" in kwargs:
            self.timeout = kwargs["timeout"]
            del kwargs["timeout"]
        super().__init__(*args, **kwargs)

    def send(self, request, **kwargs):
        timeout = kwargs.get("timeout")
        if timeout is None:
            kwargs["timeout"] = self.timeout
        return super().send(request, **kwargs)


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
        super().__init__()
        self.base_url = base_url

        super().mount(self.base_url, TimeoutHTTPAdapter(timeout=timeout,
                                                        max_retries=Retry(
                                                            total=max_retries,
                                                            status_forcelist=[500, 503],
                                                            backoff_factor=backoff_factor,
                                                        )))

    def get(self, url: str, *args: tp.Any, **kwargs: tp.Any) -> requests.Response:
        return super().get(f'{self.base_url}/{url}', *args, **kwargs)

    def post(self, url: str, *args: tp.Any, **kwargs: tp.Any) -> requests.Response:
        return super().post(f'{self.base_url}/{url}', *args, **kwargs)
