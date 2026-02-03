import requests

session = "2tqp9wyq0jldur88iwrs6n3jquoujalk"

# response = requests.post(
#     "http://127.0.0.1:8000/api/_allauth/app/v1/account/phone",
#     json={
#         "phone": "+18005550006",
#         # "password": "haomao.12"
#     },
#     headers={
#         "Content-Type": "application/json",
#         "X-Session-Token": session
#     }
# )


# session = "8f217gj1f0nh3wkvq2dvrfhz7qlempy3"
response = requests.post(
    "http://127.0.0.1:8000/api/_allauth/app/v1/auth/phone/verify",
    headers={
        "Content-Type": "application/json",
        "X-Session-Token": session
    },
    json={
        "code": "3WRJK9"
    }
)

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
