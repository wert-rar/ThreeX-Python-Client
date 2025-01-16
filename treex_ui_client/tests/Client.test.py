import unittest
from unittest.mock import patch

from treex_ui_client import Client3XUI, ClientError
from test_config import *

class Client3XUITest(unittest.TestCase):

    def setUp(self):
        self.client = Client3XUI(
        login=PANEL_LOGIN,
        password=PANEL_PASSWORD,
        login_key=PANEL_SECRET_KEY,
        panel_host=PANEL_HOST,
        root_url=PANEL_ROOT_URL,
        sub_host=SUB_HOST,
        sub_path=SUB_PATH,
        inbound_id=INBOUND_ID,
        panel_port=PANEL_PORT,
        sub_port=SUB_PORT,
        logging_enabled=CLIENT_LOGGING_ENABLED
    )
    
    def test_client_3xui_initialization(self):
        client = Client3XUI(
        login=PANEL_LOGIN,
        password=PANEL_PASSWORD,
        login_key=PANEL_SECRET_KEY,
        panel_host=PANEL_HOST,
        root_url=PANEL_ROOT_URL,
        sub_host=SUB_HOST,
        sub_path=SUB_PATH,
        inbound_id=INBOUND_ID,
        panel_port=PANEL_PORT,
        sub_port=SUB_PORT,
        logging_enabled=True
        )

        self.assertIsInstance(client, Client3XUI)
        self.assertEqual(client.inbound, INBOUND_ID)
        self.assertEqual(client.base_url, f'https://{PANEL_HOST}:{PANEL_PORT}/{PANEL_ROOT_URL}')
        self.assertEqual(client.sub_url, f'https://{SUB_HOST}:{SUB_PORT}/{SUB_PATH}')
        self.assertIsNotNone(client.logger)
        self.assertIsNotNone(client.session)
        



if __name__ == '__main__':
    unittest.main()
