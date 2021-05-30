import os
import jwt
from flask import abort


def parse(request):
    if request.method == "POST":
        content_type = request.headers["content-type"]
        if content_type == "application/json":
            request_json = request.get_json(silent=True)

            if request_json:
                if "jwt_token" not in request_json:
                    return "JSON is invalid, or missing a 'jwt_token' property"

                return jwt.decode(
                    request_json["jwt_token"],
                    os.environ.get("JWT_SECRET", "-"),
                    algorithm="HS256",
                )
            else:
                return abort(405)
        else:
            return abort(405)
    else:
        return abort(405)
