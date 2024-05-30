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
async def get_proxy_request(
    service:str, 
    path:str, 
    request:Request, 
    version: str = Header("1.0"), 
    access_token: Annotated[str | None, Header()] = None,
    refresh_token: Annotated[str | None, Header()] = None
):
    auth = AuthService(header={"version" : version})

    # AT, RT 둘 다 없는 경우 
    if not access_token and not refresh_token:
        raise HTTPException(status_code=400, detail="No token in header")

    # RT만 있을 경우, 
    elif refresh_token and not access_token :
        payload = await auth.verify_token(refresh_token, "R")
        return await auth.forward_api("GET", service, path, request, payload.get("sub"))

    # AT가 존재할 경우,
    else:
        payload = await auth.verify_token(access_token, "A")
        return await auth.forward_api("GET", service, path, request, payload.get("sub"))

@router.post("/{service}/{path:path}")
async def post_proxy_request(
    service:str, 
    path:str, 
    request:Request, 
    version: str = Header("1.0"), 
    access_token: Annotated[str | None, Header()] = None, 
    refresh_token: Annotated[str | None, Header()] = None
):

    auth = AuthService(header={"version" : version})

    # 로그인 / 회원가입 로직
    if path == "login" or path == "signup":
        return await auth.forward_api("POST", service, path, request)

    # AT, RT 둘 다 없는 경우 
    elif not access_token and not refresh_token:
        raise HTTPException(status_code=400, detail="No token in header")

    # RT만 있을 경우, 
    elif not access_token and refresh_token :
        payload = await auth.verify_token(refresh_token, "R")
        return await auth.forward_api("POST", service, path, request, payload.get("sub"))

    # AT가 존재할 경우,
    else :
        payload = await auth.verify_token(access_token, "A")
        return await auth.forward_api("POST", service, path, request, payload.get("sub"))

@router.put("/{service}/{path:path}")
async def put_proxy_request(
    service:str, 
    path:str, 
    request:Request, 
    version: str = Header("1.0"), 
    access_token: Annotated[str | None, Header()] = None,
    refresh_token: Annotated[str | None, Header()] = None
):
    
    auth = AuthService(header={"version" : version})

    # AT, RT 둘 다 없는 경우 
    if not access_token and not refresh_token:
        raise HTTPException(status_code=400, detail="No token in header")

    # RT만 있을 경우, 
    elif not access_token and refresh_token :
        payload = await auth.verify_token(refresh_token, "R")
        return await auth.forward_api("PUT", service, path, request, payload.get("sub"))

    # AT가 존재할 경우,
    else:
        payload = await auth.verify_token(access_token, "A")
        return await auth.forward_api("PUT", service, path, request, payload.get("sub"))

@router.delete("/{service}/{path:path}")
async def put_proxy_request(
    service:str, 
    path:str, 
    request:Request, 
    version: str = Header("1.0"), 
    access_token: Annotated[str | None, Header()] = None,
    refresh_token: Annotated[str | None, Header()] = None
):
    auth = AuthService(header={"version" : version})

    # AT, RT 둘 다 없는 경우 
    if not access_token and not refresh_token:
        raise HTTPException(status_code=400, detail="No token in header")

    # RT만 있을 경우, 
    elif not access_token and refresh_token :
        payload = await auth.verify_token(refresh_token, "R")
        return await auth.forward_api("DELETE", service, path, request, payload.get("sub"))
        
    # AT가 존재할 경우,
    else:
        payload = await auth.verify_token(access_token, "A")
        return await auth.forward_api("DELETE", service, path, request, payload.get("sub"))