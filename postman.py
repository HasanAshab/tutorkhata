import requests

# phone_number = "+15005550006"
# password = "haomao.12"

# response = requests.post(
#     "http://127.0.0.1:8000/api/_allauth/app/v1/auth/signup",
#     json={
#         "phone": phone_number,
#         "password": password
#     },
#     headers={
#         "Content-Type": "application/json"
#     }
# )
# bearer = "kyyuth6bfpf6bxu52ywy5khszl1zqjtc"
# response = requests.post(
#     "http://127.0.0.1:8000/api/_allauth/app/v1/auth/login",
#     json={
#         "phone": "+15005550006",
#         "password": "haomao.12"
#     },
#     headers={
#         "Content-Type": "application/json"
#     }
# )

session = "cszb7e48nd9spuwy84au7nc3fk1g0ork"
response = requests.get(
    "http://127.0.0.1:8000/api/users/",
    headers={
        "Content-Type": "application/json",
        "X-Session-Token": session
    }
)


print("status code: " + str(response.status_code))
with open("index.html", "w", encoding="utf-8") as f:
    f.write(response.text)

try:
    print(response.json())
except:
    print(response.text)
