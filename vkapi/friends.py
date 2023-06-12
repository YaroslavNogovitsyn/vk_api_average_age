import dataclasses
import math
import typing as tp

from vkapi import session, config
from vkapi.exceptions import APIError


@dataclasses.dataclass(frozen=True)
class FriendsResponse:
    count: int
    items: tp.Union[tp.List[int], tp.List[tp.Dict[str, tp.Any]]]


def get_friends(
        user_id: int, count: int = 5000, offset: int = 0, fields: tp.Optional[tp.List[str]] = None
) -> FriendsResponse:
    """
    Получить список идентификаторов друзей пользователя или расширенную информацию
    о друзьях пользователя (при использовании параметра fields).

    :param user_id: Идентификатор пользователя, список друзей для которого нужно получить.
    :param count: Количество друзей, которое нужно вернуть.
    :param offset: Смещение, необходимое для выборки определенного подмножества друзей.
    :param fields: Список полей, которые нужно получить для каждого пользователя.
    :return: Список идентификаторов друзей пользователя или список пользователей.
    """
    response = session.get(
        "friends.get",
        params={
            "access_token": config.VK_CONFIG["access_token"],
            "v": config.VK_CONFIG["version"],
            "user_id": user_id,
            "count": count,
            "offset": offset,
            "fields": ",".join(fields) if fields else "",
        },
    )
    result = response.json()
    if not response.ok or "error" in result:
        raise APIError(result["error"]["error_msg"])
    return FriendsResponse(count=result["response"]["count"], items=result["response"]["items"])


class MutualFriends(tp.TypedDict):
    id: int
    common_friends: tp.List[int]
    common_count: int


def get_mutual(
        source_uid: tp.Optional[int] = None,
        target_uid: tp.Optional[int] = None,
        target_uids: tp.Optional[tp.List[int]] = None,
        order: str = "",
        count: tp.Optional[int] = None,
        offset: int = 0,
        progress=None,
) -> tp.Union[tp.List[int], tp.List[MutualFriends]]:
    """
    Получить список идентификаторов общих друзей между парой пользователей.

    :param source_uid: Идентификатор пользователя, чьи друзья пересекаются с друзьями пользователя с идентификатором target_uid.
    :param target_uid: Идентификатор пользователя, с которым необходимо искать общих друзей.
    :param target_uids: Cписок идентификаторов пользователей, с которыми необходимо искать общих друзей.
    :param order: Порядок, в котором нужно вернуть список общих друзей.
    :param count: Количество общих друзей, которое нужно вернуть.
    :param offset: Смещение, необходимое для выборки определенного подмножества общих друзей.
    :param progress: Callback для отображения прогресса.
    """
    if target_uid:
        response = session.get(
            "friends.getMutual",
            params={
                "access_token": config.VK_CONFIG["access_token"],
                "v": config.VK_CONFIG["version"],
                "source_uid": source_uid,
                "target_uid": target_uid,
                "order": order,
                "count": count,
                "offset": offset,
            },
        )
        result = response.json()
        if not response.ok or "error" in result:
            raise APIError(result["error"]["error_msg"])
        return result["response"]

    responses = []

    for i in progress(range(math.ceil(len(target_uids) / 100))):
        response = session.get(
            "friends.getMutual",
            params={
                "access_token": config.VK_CONFIG["access_token"],
                "v": config.VK_CONFIG["version"],
                "source_uid": source_uid,
                "target_uids": ",".join(map(str, target_uids)),
                "order": order,
                "count": count if count is not None else "",
                "offset": offset + i * 100,
            },
        )

        result = response.json()
        if not response.ok or "error" in result:
            raise APIError(result["error"]["error_msg"])

        for elem in result['response']:
            responses.append(
                MutualFriends(
                    id=elem["id"],
                    common_friends=elem["common_friends"],
                    common_count=elem["common_count"],
                )
            )
    return responses


if __name__ == '__main__':
    from tqdm import tqdm

    friends_response = get_friends(user_id=150968391, fields=["nickname"])
    active_users = [user["id"] for user in friends_response.items if not user.get("deactivated")]
    print(len(active_users))
    mutual_friends = get_mutual(source_uid=817934, target_uids=active_users, progress=tqdm)
