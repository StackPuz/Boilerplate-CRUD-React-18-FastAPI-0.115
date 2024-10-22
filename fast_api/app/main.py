import os
import uvicorn
from typing import Callable
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.exceptions import RequestValidationError
from sqlalchemy.exc import IntegrityError
from app.routers import login, system, user_account, product, brand, order_header, order_detail
from app.middlewares import authenticate, authorize
from app.util import get_error

app = FastAPI()

os.makedirs("uploads", exist_ok=True)
app.mount("/uploads", StaticFiles(directory="uploads"))

app.include_router(login.router, prefix="/api")
app.include_router(system.router, prefix="/api")
app.include_router(user_account.router, prefix="/api")
app.include_router(product.router, prefix="/api")
app.include_router(brand.router, prefix="/api")
app.include_router(order_header.router, prefix="/api")
app.include_router(order_detail.router, prefix="/api")

@app.middleware("http")
async def authorize_middleware(request: Request, next: Callable):
    return await authorize(request, next)

@app.middleware("http")
async def authenticate_middleware(request: Request, next: Callable):
    return await authenticate(request, next)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.exception_handler(Exception)
async def exception_handler(request: Request, exc: Exception):
    return await get_error(exc)

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    return await get_error(exc)

@app.exception_handler(IntegrityError)
async def db_exception_handler(request: Request, exc: IntegrityError):
    return await get_error(exc)

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1")