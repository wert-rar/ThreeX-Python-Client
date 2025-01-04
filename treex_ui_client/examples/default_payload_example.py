from treex_ui_client.treex_ui_client import DefaultPayload

payload = DefaultPayload(12345, "aaaa-aaaa-aaaa-aaaa",
                        "john.doe@example.com", 3,
                         17000000000,"1234567890")
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