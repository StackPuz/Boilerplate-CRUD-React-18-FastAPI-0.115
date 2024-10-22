import jwt
from fastapi import Request, Response
from typing import Callable
from app.config import config

allows = [ "/api/login", "/api/logout", "/api/stack", "/api/resetPassword", "/api/changePassword", "/uploads" ]
jwt_secret = config["jwtSecret"]

async def authenticate(request: Request, next: Callable):
    if request.url.path in allows or request.url.path.startswith(allows[4]) or request.url.path.startswith(allows[5]):
        response = await next(request)
    else:
        header = request.headers.get("Authorization")
        if not header or not header.startswith("Bearer "):
            return Response(status_code=401)
        token = header[7:]
        try:
            request.state.user = jwt.decode(token, jwt_secret, algorithms=["HS256"])
        except jwt.InvalidTokenError:
            return Response(status_code=401)
        response = await next(request)
    return response