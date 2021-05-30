import os
import jwt
import bcrypt
import sqlalchemy
from flask import abort


def login(request):
    if request.method == "POST":
        content_type = request.headers["content-type"]
        if content_type == "application/json":
            request_json = request.get_json(silent=True)

            if request_json:
                if "username" not in request_json:
                    return "JSON is invalid, or missing a 'username' property"

                if "password" not in request_json:
                    return "JSON is invalid, or missing a 'password' property"

                if request_json["username"] == os.environ.get(
                    "SU_USERNAME", "-"
                ) and request_json["password"] == os.environ.get("SU_PASSWORD", "-"):
                    JWT_DATA = {
                        "https://hasura.io/jwt/claims": {
                            "x-hasura-allowed-roles": ["user", "editor", "super_admin"],
                            "x-hasura-default-role": "super_admin",
                        }
                    }

                    return jwt.encode(
                        JWT_DATA,
                        os.environ.get("JWT_SECRET", "-"),
                        algorithm="HS256",
                    )

                driver_name = "postgres+pg8000"
                query_string = dict(
                    {
                        "unix_sock": f"/cloudsql/{os.environ.get('DB_CONNECTION_NAME', '-')}/.s.PGSQL.5432"
                    }
                )

                db = sqlalchemy.create_engine(
                    sqlalchemy.engine.url.URL(
                        drivername=driver_name,
                        username=os.environ.get("DB_USERNAME", "-"),
                        password=os.environ.get("DB_PASSWORD", "-"),
                        database=os.environ.get("DB_DATABASE", "-"),
                        query=query_string,
                    ),
                    pool_size=5,
                    max_overflow=2,
                    pool_timeout=30,
                    pool_recycle=1800,
                )

                username = request_json["username"]
                stmt = sqlalchemy.text(
                    "select id, nama, password, write_access from admins where email=:username"
                )

                try:
                    with db.connect() as conn:
                        result = conn.execute(stmt, username=username).fetchone()

                        if result:
                            res_id, _, res_password, res_write_access = result
                            if bcrypt.checkpw(
                                request_json["password"].encode(), res_password.encode()
                            ):
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
                                    os.environ.get("JWT_SECRET", "-"),
                                    algorithm="HS256",
                                )

                                return encoded_jwt
                            else:
                                return "Pass is wrong"
                        else:
                            return "User not found"
                except Exception as e:
                    return "Error: {}".format(str(e))

            else:
                return abort(405)
        else:
            return abort(405)
    else:
        return abort(405)
