import os
import jwt
from flask import abort


def parse(request):

    # Set CORS headers for the main request
    headers = {
        'Access-Control-Allow-Origin': '*'
    }

    if request.method == 'OPTIONS':
        # Allows GET requests from any origin with the Content-Type
        # header and caches preflight response for an 3600s
        headers = {
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': 'GET',
            'Access-Control-Allow-Headers': 'Content-Type',
            'Access-Control-Max-Age': '3600'
        }

        return ('', 204, headers)
        
    elif request.method == "POST":
        content_type = request.headers["content-type"]
        if content_type == "application/json":
            request_json = request.get_json(silent=True)

            if request_json:
                if "jwt_token" not in request_json:
                    return "JSON is invalid, or missing a 'jwt_token' property"

                try:
                    res = jwt.decode(
                        request_json["jwt_token"],
                        os.environ.get("JWT_SECRET", "-"),
                        algorithms=["HS256"],
                    )

                    return str(res)
                except:
                    return "Error happened"
            else:
                return abort(405)
        else:
            return abort(405)
    else:
        return abort(405)
