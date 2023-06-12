# https://hackernoon.com/4-ways-to-manage-the-configuration-in-python-4623049e841b
import os.path

from dotenv import load_dotenv

path = os.path.join(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')), '.env')
if os.path.exists(path):
    load_dotenv(path)
    token = os.environ.get("token")
else:
    raise FileNotFoundError

VK_CONFIG = {
    "domain": "https://api.vk.com/method",
    "access_token": token,
    "version": "5.126",
}
