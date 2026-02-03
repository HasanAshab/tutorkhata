import requests

response = requests.post(
    "http://127.0.0.1:8000/api/_allauth/app/v1/auth/login",
    json={
        "phone": "+15005550006",
        "password": "haomao.12"
    },
    headers={
        "Content-Type": "application/json"
    }
)


# session = "8f217gj1f0nh3wkvq2dvrfhz7qlempy3"
# response = requests.post(
#     "http://127.0.0.1:8000/api/_allauth/app/v1/auth/phone/verify",
#     headers={
#         "Content-Type": "application/json",
#         "X-Session-Token": session
#     },
#     json={
#         "code": "57RWHP"
#     }
# )

# session = "cszb7e48nd9spuwy84au7nc3fk1g0ork"
# response = requests.get(
#     "http://127.0.0.1:8000/api/account/",
#     headers={
#         "Content-Type": "application/json",
#         "X-Session-Token": session
#     }
# )


print("status code: " + str(response.status_code))
with open("index.html", "w", encoding="utf-8") as f:
    f.write(response.text)

try:
    print(response.json())
except:
    print(response.text)
