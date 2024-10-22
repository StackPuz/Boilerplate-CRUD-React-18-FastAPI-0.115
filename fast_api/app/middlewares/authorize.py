from fastapi import Request, Response
from typing import Callable
from app.config import config

async def authorize(request: Request, next: Callable):
    if request.url.path.startswith("/uploads"):
        return await next(request)
    path = request.url.path.split("/")[2]
    roles = ""
    for menu in config["menu"]:
        if menu.get("api") == path and menu.get("roles"):
            roles = menu["roles"]
            break
    if not roles:
        return await next(request)
    if hasattr(request.state, "user"):
        user_roles = request.state.user["roles"]
        menu_roles = roles.split(",")
        if any(role in menu_roles for role in user_roles):
            return await next(request)
    return Response(status_code=403)