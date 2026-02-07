import requests

session = "ovhkrmwilaszedqruqtxsb46hvynffs4"

# response = requests.post(
#     "http://127.0.0.1:8000/api/_allauth/app/v1/auth/phone/verify",
#     json={
#         # "phone": "+18005550006",
#         # "password": "haomao.12"
#         "code": "XHH3MD"
#     },
#     headers={
#         "Content-Type": "application/json",
#         "X-Session-Token": session
#     }
# )


# session = "8f217gj1f0nh3wkvq2dvrfhz7qlempy3"
# response = requests.post(
#     "http://127.0.0.1:8000/api/_allauth/app/v1/auth/phone/verify",
#     headers={
#         "Content-Type": "application/json",
#         "X-Session-Token": session
#     },
#     json={
#         "code": "3WRJK9"
#     }
# )

with open("teacher.jpg", "rb") as f:
    avatar = f.read()
response = requests.patch(
    "http://127.0.0.1:8000/api/teachers/me/",
    headers={
        # "Content-Type": "application/json",
        "X-Session-Token": session
    },
    files={"avatar": ("teacher.jpg", avatar)},
)


print("status code: " + str(response.status_code))
with open("index.html", "w", encoding="utf-8") as f:
    f.write(response.text)

try:
    print(response.json())
except Exception:
    print(response.text)
