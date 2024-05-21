# 라우팅
from typing import Annotated
from fastapi import APIRouter, Request, HTTPException, Header
import httpx
import json

from app.database.settings import SessionLocal, engine
from app.core.db import Engineconn

from app.service.auth import AuthService

router = APIRouter()

SERVICES = {
    # 서버용
    # "user" : "http://10.0.8.7:8000/user", 
    # 로컬용
    "user" : "http://127.0.0.1:8080/user",
    "invitation" : "10.0.5.6:8080"
}

engine = Engineconn()
session = engine.create_session()

def get_test_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/{service}/{path:path}")
async def get_proxy_request(service:str, path:str, request:Request, version: str = Header("1.0"), access_token: Annotated[str | None, Header()] = None):
    # accessToken이 없는 경우
    # if not access_token and not (path == "login" or path == "signup"):
    #     raise HTTPException(status_code=401, detail="accessToken header missing!")

    # # 토큰이 있을 경우, 유효한 토큰인지 체크
    # auth = AuthService()
    # return await auth.forward_api(request)
    # # verify_jwt(access_token)

    url = f"http://{SERVICES[service]}/{path}"
    async with httpx.AsyncClient() as client:
        response = await client.get(url, params=request.query_params, headers={"version" : version})
        return response.json()
        

@router.post("/{service}/{path:path}")
async def post_proxy_request(service:str, path:str, request:Request, version: str = Header("1.0"), access_token: Annotated[str | None, Header()] = None):

    auth = AuthService()
    url = f"{SERVICES[service]}/{path}"

    if path == "login" or "signup":
        async with httpx.AsyncClient() as client:
            response = await client.post(url, content=await request.body(), headers={"version" : version})
            return response.json()

@router.put("/{service}/{path:path}")
async def put_proxy_request(service:str, path:str, request:Request, version: str = Header("1.0")):
    url = f"{SERVICES[service]}/{path}"
    async with httpx.AsyncClient() as client:
        response = await client.put(url, content=await request.body(), headers={"version" : version})
        return response.json()

@router.delete("/{service}/{path:path}")
async def delete_proxy_request(service:str, path:str, request:Request, version: str = Header("1.0")):
    url = f"{SERVICES[service]}/{path}"
    async with httpx.AsyncClient() as client:
        response = await client.delete(url, headers={"version" : version})
        return response.json()