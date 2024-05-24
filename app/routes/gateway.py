# 라우팅
from typing import Annotated
from sqlalchemy.orm import Session
from fastapi import APIRouter, Request, HTTPException, Header, Depends
import httpx
import json

from app.database.settings import SessionLocal, engine, get_test_db
from app.core.db import Engineconn
from app.core.config import USER_URL, INVITATION_URL

from app.service.auth import AuthService

router = APIRouter()

SERVICES = {
    "user" : USER_URL,
    "invitation" : INVITATION_URL
}

#TODO PROXY_REQUEST 로직 분리하기 -> 중복코드 너무 많음 🚨🚨🚨🚨🚨🚨

@router.get("/{service}/{path:path}")
async def get_proxy_request(service:str, path:str, request:Request, version: str = Header("1.0"), access_token: Annotated[str | None, Header()] = None):

    if not access_token :
        raise HTTPException(status_code=400, detail="No access_token in Header")

    else:
        auth = AuthService()
        url = f"{SERVICES[service]}/{path}"

        payload = await auth.verify_and_create_token(
            service,
            path,
            request,
            access_token,
            version
        )

        # payload가 있는 경우,
        user_id = payload.get("sub")

        async with httpx.AsyncClient() as client:
            response = await client.get(url, params=request.query_params, headers={"version" : version, "user_id" : str(user_id)})
            if response.status_code != 200:
                raise HTTPException(status_code=response.status_code, detail=json.loads(response.content).get("detail"))
            return json.loads(response.content)
        

@router.post("/{service}/{path:path}")
async def post_proxy_request(service:str, path:str, request:Request, version: str = Header("1.0"), access_token: Annotated[str | None, Header()] = None):

    auth = AuthService()
    url = f"{SERVICES[service]}/{path}"

    # 로그인 / 회원가입 로직
    if path == "login" or path == "signup":
        async with httpx.AsyncClient() as client:
            response = await client.post(url, content=await request.body(), headers={"version" : version})
            if response.status_code != 200:
                raise HTTPException(status_code=response.status_code, detail=json.loads(response.content).get("detail"))
            return json.loads(response.content)

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
        user_id = payload.get("sub")

        async with httpx.AsyncClient() as client:
            response = await client.post(url, content=await request.body(), headers={"version" : version, "user_id" : str(user_id), "content-type" : "application/json"})
            if response.status_code != 200:
                raise HTTPException(status_code=response.status_code, detail=json.loads(response.content).get("detail"))
            return json.loads(response.content)


@router.put("/{service}/{path:path}")
async def put_proxy_request(service:str, path:str, request:Request, version: str = Header("1.0"), access_token: Annotated[str | None, Header()] = None):
    

    if not access_token :
        raise HTTPException(status_code=400, detail="No access_token in Header")

    else:
        auth = AuthService()
        url = f"{SERVICES[service]}/{path}"

        payload = await auth.verify_and_create_token(
            service,
            path,
            request,
            access_token,
            version
        )

        # payload가 있는 경우,
        user_id = payload.get("sub")

        async with httpx.AsyncClient() as client:
            response = await client.put(url, content=await request.body(), headers={"version" : version, "user_id" : str(user_id)})
            if response.status_code != 200:
                raise HTTPException(status_code=response.status_code, detail=json.loads(response.content).get("detail"))
            return json.loads(response.content)

@router.delete("/{service}/{path:path}")
async def put_proxy_request(service:str, path:str, request:Request, version: str = Header("1.0"), access_token: Annotated[str | None, Header()] = None):

    if not access_token :
        raise HTTPException(status_code=400, detail="No access_token in Header")

    else:
        auth = AuthService()
        url = f"{SERVICES[service]}/{path}"

        payload = await auth.verify_and_create_token(
            service,
            path,
            request,
            access_token,
            version
        )

        # payload가 있는 경우,
        user_id = payload.get("sub")

        async with httpx.AsyncClient() as client:
            response = await client.delete(url, params=request.query_params, headers={"version" : version, "user_id" : str(user_id)})
            if response.status_code != 200:
                raise HTTPException(status_code=response.status_code, detail=json.loads(response.content).get("detail"))
            return json.loads(response.content)