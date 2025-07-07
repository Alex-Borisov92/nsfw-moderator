import requests

api_key = "a3e45867-3479-4856-8eca-3a848225ea5e"
url = "https://api.deepai.org/api/nsfw-detector"

headers = {"api-key": api_key}
files = {"image": open("/home/aborisov/code/test_cases/nsfw-moderator/cat.jpg", "rb")}

response = requests.post(url, headers=headers, files=files)
print(response.json())