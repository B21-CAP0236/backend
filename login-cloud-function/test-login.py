import sqlalchemy, bcrypt, jwt

db = sqlalchemy.create_engine(
    sqlalchemy.engine.url.URL(
        drivername="postgresql+pg8000",
        username="postgres",
        password="zOoMH61sw9xEL3Bv",
        host="34.69.66.167",
        port="5432",
        database="postgres",
    ),
    pool_size=5,
    max_overflow=2,
    pool_timeout=30,
    pool_recycle=1800,
)

username = "test@gmail.com"
stmt = sqlalchemy.text(
    "select id, nama, password, write_access from admins where email=:username"
)

try:
    with db.connect() as conn:
        result = conn.execute(stmt, username=username).fetchone()

        if result:
            res_id, res_nama, res_password, res_write_access = result
            if bcrypt.checkpw("secret".encode(), res_password.encode()):
                JWT_DATA = {
                    "https://hasura.io/jwt/claims": {
                        "x-hasura-allowed-roles": ["user", "editor"]
                        if res_write_access
                        else ["user"],
                        "x-hasura-default-role": "editor"
                        if res_write_access
                        else "user",
                        "x-hasura-user-id": str(res_id),
                    }
                }

                encoded_jwt = jwt.encode(
                    JWT_DATA,
                    "eW91IHJlYWxseSB0aGluayBpbSB0aGF0IHN0dXBpZCA/Cg==",
                    algorithm="HS256",
                )

                print(encoded_jwt)
            else:
                print("Pass is wrong")
        else:
            print("User not found")
except Exception as e:
    print("Error: {}".format(str(e)))
