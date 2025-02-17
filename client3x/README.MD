# *3X-UI API Client*

## *Overview*

*This project provides a Python* client for interacting with the **[3X-UI](https://github.com/MHSanaei/3x-ui) API**.

It supports both synchronous and asynchronous operations,
making it suitable for various use cases and performance requirements.

## Features

- **Synchronous Client:** For straightforward and blocking API calls.
- **Asynchronous Client:** For non-blocking operations to improve performance and scalability.
- **Payload Class:** Simplifies payload creation and formatting for API requests.

---

## Installation

```bash
pip install client3x
```

---
## Requirements

- Python 3.6 or higher
- requests library
- aiohttp library 
---

## Usage

Here are examples of working with synchronous and asynchronous clients and working with the default payload class.
For further information, you can refer to [Documentation](https://github.com/wert-rar/ThreeX-Python-Client/blob/master/treex_ui_client/docs/Documentation.md) or look at usage [examples](https://github.com/wert-rar/ThreeX-Python-Client/tree/master/treex_ui_client/examples)

To see what the methods return, it is recommended to visit this [link](https://www.postman.com/hsanaei/3x-ui/collection/q1l5l0u/3x-ui) .

### Synchronous Client Example

```python
from client3x import Client3XUI
from config import *

# Initialize the client
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

# Get info about all connections
info = client.info_about_all_clients()   
```

### Asynchronous Client Example

```python
import asyncio
from client3x import AsyncClient3XUI
from config import *


async def main():
    # Initialize the client
    client = AsyncClient3XUI(
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
    client.start()
    # Get info about all connections
    info = await client.info_about_all_clients()


asyncio.run(main())
```

### DefaultPayload Example

```python
from client3x import CLientPayload

payload = ClientPayload(12345, "aaaa-aaaa-aaaa-aaaa",
                        "john.doe@example.com", 3,
                        17000000000, "1234567890")
print(str(payload))

# Inbound: 12345,
# Settings: {'clients': [{'email': 'john.doe@example.com',
#               'enable': True,
#               'expiryTime': 17000000000,
#               'flow': 'xtls-rprx-vision',
#               'id': 'aaaa-aaaa-aaaa-aaaa',
#               'limitIp': 3,
#               'reset': 0,
#               'subId': '1234567890',
#               'totalGB': 0}]}


```
---



## Contributing

Contributions are welcome! Please fork this repository and submit pull requests.

---

## License

This project is licensed under the MIT License. See the LICENSE file for details.

---

## Contact

For any issues or inquiries, please open an issue on the [GitHub repository](https://github.com/wert-rar/ThreeX-Python-Client.git).

