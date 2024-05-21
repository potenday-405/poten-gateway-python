# 라우팅
from typing import Annotated
from sqlalchemy.orm import Session
from fastapi import APIRouter, Request, HTTPException, Header, Depends
import httpx
import json

from app.database.settings import SessionLocal, engine, get_test_db
from app.core.db import Engineconn

from app.service.auth import AuthService

router = APIRouter()

SERVICES = {
    # 서버용
    "user" : "10.0.8.7:8000/user", 
    # 로컬용
    # "user" : "http://127.0.0.1:8080/user",
    # 걍진짜 테스트
    # "user" : "http://175.45.203.113:8000/user",
    "invitation" : "10.0.5.6:8080"
}

@router.get("/{service}/{path:path}")
async def get_proxy_request(service:str, path:str, request:Request, version: str = Header("1.0"), access_token: Annotated[str | None, Header()] = None, db:Session = Depends(get_test_db)):

    if not access_token :
        raise HTTPException(status_code=400, detail="No access_token in Header")

    else:
        auth = AuthService(db)
        url = f"{SERVICES[service]}/{path}"

        payload = await auth.verify_and_create_token(
            service,
            path,
            request,
            access_token,
            version
        )

        # payload가 있는 경우,
        email = payload.get("sub")

        if email:
            # user_id값 보내기
            user_id = await auth.get_user_id(email)
            async with httpx.AsyncClient() as client:
                response = await client.get(url, params=request.query_params, headers={"version" : version, "user_id" : str(user_id)})
                return response.json()
        

@router.post("/{service}/{path:path}")
async def post_proxy_request(service:str, path:str, request:Request, version: str = Header("1.0"), access_token: Annotated[str | None, Header()] = None, db:Session = Depends(get_test_db)):

    auth = AuthService(db)
    url = f"{SERVICES[service]}/{path}"

    # 로그인 / 회원가입 로직
    if path == "login" or path == "signup":
        async with httpx.AsyncClient() as client:
            response = await client.post(url, content=await request.body(), headers={"version" : version})
            return response.json()

    # accessToken이 없을 경우, error raise
    elif not access_token :
        raise HTTPException(status_code=400, detail="No access_token in Header")

    # accessToken이 존재할 경우,
    else:
        payload = await auth.verify_and_create_token(
            service,
            path,
            request,
            access_token,
            version
        )

        # payload가 있는 경우,
        email = payload.get("sub")

        if email:
            # user_id값 보내기
            user_id = await auth.get_user_id(email)
            async with httpx.AsyncClient() as client:
                response = await client.post(url, content=await request.body(), headers={"version" : version, "user_id" : str(user_id)})
                return response.json()

@router.put("/{service}/{path:path}")
async def put_proxy_request(service:str, path:str, request:Request, version: str = Header("1.0"), access_token: Annotated[str | None, Header()] = None, db:Session = Depends(get_test_db)):

    if not access_token :
        raise HTTPException(status_code=400, detail="No access_token in Header")

    else:
        auth = AuthService(db)
        url = f"{SERVICES[service]}/{path}"

        payload = await auth.verify_and_create_token(
            service,
            path,
            request,
            access_token,
            version
        )

        # payload가 있는 경우,
        email = payload.get("sub")

        if email:
            # user_id값 보내기
            user_id = await auth.get_user_id(email)
            async with httpx.AsyncClient() as client:
                response = await client.put(url, params=await request.body(), headers={"version" : version, "user_id" : str(user_id)})
                return response.json()

@router.delete("/{service}/{path:path}")
async def put_proxy_request(service:str, path:str, request:Request, version: str = Header("1.0"), access_token: Annotated[str | None, Header()] = None, db:Session = Depends(get_test_db)):

    if not access_token :
        raise HTTPException(status_code=400, detail="No access_token in Header")

    else:
        auth = AuthService(db)
        url = f"{SERVICES[service]}/{path}"

        payload = await auth.verify_and_create_token(
            service,
            path,
            request,
            access_token,
            version
        )

        # payload가 있는 경우,
        email = payload.get("sub")

        if email:
            # user_id값 보내기
            user_id = await auth.get_user_id(email)
            async with httpx.AsyncClient() as client:
                response = await client.delete(url, headers={"version" : version, "user_id" : str(user_id)})
                return response.json()