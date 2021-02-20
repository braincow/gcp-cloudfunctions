#!python3
import json
import requests
import google.auth.transport.requests
from google.oauth2.service_account import IDTokenCredentials

credentials = IDTokenCredentials.from_service_account_file(
    'sa.json',
    target_audience='https://ruuvitag-api-gateway-6bd8cwuy.ew.gateway.dev')

request = google.auth.transport.requests.Request()
credentials.refresh(request)

headers = {'Authorization': 'Bearer ' + credentials.token}
print(headers)

r = requests.get(
    'https://ruuvitag-api-gateway-6bd8cwuy.ew.gateway.dev/ruuvitags',
    headers=headers)

print(json.dumps(r.json()))
#
# eof
