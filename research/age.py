import statistics
import typing as tp
from datetime import datetime

from vkapi.friends import get_friends


def age_predict(user_id: int) -> tp.Optional[float]:
    """
    Наивный прогноз возраста пользователя по возрасту его друзей.

    Возраст считается как медиана среди возраста всех друзей пользователя

    :param user_id: Идентификатор пользователя.
    :return: Медианный возраст пользователя.
    """
    ages = []

    for friend in get_friends(user_id, fields=["bdate"]).items:
        try:
            ages.append(datetime.strptime(friend["bdate"], "%d.%m.%Y").year)
        except (KeyError, ValueError):
            pass

    if ages:
        return datetime.today().year - statistics.median(ages)
    return None
