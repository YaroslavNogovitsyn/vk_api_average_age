import unittest

import responses

from vkapi.friends import FriendsResponse, get_friends


class FriendsTestCase(unittest.TestCase):
    @responses.activate
    def test_get_friends(self):
        expected_fids = [1, 2, 3, 4, 5]
        responses.add(
            responses.GET,
            "https://api.vk.com/method/friends.get",
            json={"response": {"count": len(expected_fids), "items": expected_fids}},
            status=200,
        )
        fids = get_friends(user_id=1)
        expected_response = FriendsResponse(count=len(expected_fids), items=expected_fids)
        self.assertEqual(expected_response, fids)
