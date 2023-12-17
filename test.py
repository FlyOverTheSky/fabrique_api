import requests
token = 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJleHAiOjE3MzM1NTk4NDIsImlzcyI6ImZhYnJpcXVlIiwibmFtZSI6Imh0dHBzOi8vdC5tZS9BVkNBTUlEIn0.2uy2JWntNMXZfiIeUK5aOJVu6UwYUeBRRaUwbKIa9rg'


headers = {
    'accept': 'application/json',
    'Authorization': token,
    'Content-Type': 'application/json',
}

json_data = {
    'id': 0,
    'phone': '+79220375280',
    'text': 'string',
}

response = requests.post('https://probe.fbrq.cloud/v1/send/0', headers=headers, json=json_data)
print(response)
# Note: json_data will not be serialized by requests
# exactly as it was in the original request.
#data = '{\n  "id": 0,\n  "phone": 0,\n  "text": "string"\n}'
#response = requests.post('https://probe.fbrq.cloud/v1/send/0', headers=headers, data=data)
