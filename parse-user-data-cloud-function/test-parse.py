import jwt

try:
    res = jwt.decode(
        "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJodHRwczovL2hhc3VyYS5pby9qd3QvY2xhaW1zIjp7IngtaGFzdXJhLWFsbG93ZWQtcm9sZXMiOlsidXNlciJdLCJ4LWhhc3VyYS1kZWZhdWx0LXJvbGUiOiJ1c2VyIiwieC1oYXN1cmEtdXNlci1pZCI6IjIifX0.9LfRSxwLmytBqlau1nbzCnp999Y-a0UvCDs-7QYSQvI",
        "eW91IHJlYWxseSB0aGluayBpbSB0aGF0IHN0dXBpZCA/Cg==",
        algorithms=["HS256"],
    )
    print(res)
except:
    print("Error happened")
