from fastapi import APIRouter

from routers import business, passbook, transaction, user

# Get reference from here
# https://github.com/theprincemohit/full-stack-fastapi-template/blob/master/backend/app/api/main.py
api_router = APIRouter()

api_router.include_router(business.router)
api_router.include_router(passbook.router)
api_router.include_router(transaction.router)
api_router.include_router(user.router)
