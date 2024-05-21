# 라우팅
from fastapi import APIRouter, Request, HTTPException, Header
import httpx

from app.database.settings import SessionLocal, engine
from app.core.db import Engineconn

router = APIRouter()

SERVICES = {
    "user" : "10.0.8.7:8000/user",
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
async def get_proxy_request(service:str, path:str, request:Request, version: str = Header("1.0")):
    url = f"http://{SERVICES[service]}/{path}"
    print(url)
    async with httpx.AsyncClient() as client:
        response = await client.get(url, params=request.query_params, headers={"version" : version})
        return response.json()
        

@router.post("/{service}/{path:path}")
async def post_proxy_request(service:str, path:str, request:Request, version: str = Header("1.0")):
    url = f"{SERVICES[service]}/{path}"
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