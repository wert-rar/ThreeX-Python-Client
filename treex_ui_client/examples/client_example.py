import logging
import uuid

from example_config import *
from treex_ui_client.treex_ui_client import Client3XUI, CLientPayload
from treex_ui_client.treex_ui_client.PanelResponse import PanelResponse

logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )

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
        logging_enabled=CLIENT_LOGGING_ENABLED
    )

clients  = client.get_clients_in_inbound()

print(clients)

