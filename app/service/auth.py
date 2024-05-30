from fastapi import HTTPException, Request
import jwt
import json
import httpx
from datetime import datetime, timedelta
from app.core.config import ACCESS_TOKEN_EXPIRE_MINUTES, SECRET_KEY, ALGORITHM, USER_URL, INVITATION_URL
from app.database import models
from sqlalchemy.orm import Session
from pydantic import BaseModel

SERVICES = {
    "user" : USER_URL,
    "invitation" : INVITATION_URL
}

class UserId(BaseModel):
    user_id : str

class AuthService():
    def __init__(self, header:dict):
        self.header = header
        
    @staticmethod
    def get_url(service:str, path:str):
        return f"{SERVICES[service]}/{path}"

    @staticmethod
    def create_access_token(self, data: dict, expires_delta: timedelta = None):
        """새로운 토큰 발행"""
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
        return encoded_jwt

    @staticmethod
    def verify_jwt(self, token: str):
        """유효한 토큰인지 확인"""
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            return payload
        except jwt.ExpiredSignatureError:
            raise HTTPException(status_code=401, detail="Token has expired")
        except jwt.InvalidTokenError:
            raise HTTPException(status_code=401, detail="Invalid token")


    async def forward_api(
        self, 
        method:str,
        service : str, 
        path:str,
        request: Request,
        user_id: str | None = None
    ):
        """
        서비스 서버로 forwarding 해주는 메소드.

        :params method: API 메소드 종류
        :params service: API 메소드 종류
        :params path: API 메소드 종류
        :params request: API 메소드 종류
        :params user_id: API 메소드 종류

        :returns : 서비스 서버에서 받아온 response 값
        """
        if method == "GET":
            async with httpx.AsyncClient() as client:

                url = self.get_url(service, path)
                response = await client.get(url, params=request.query_params, headers={**self.header, "user_id" : str(user_id)})

                if response.status_code != 200:
                    raise HTTPException(status_code=response.status_code, detail=json.loads(response.content).get("detail"))
                return json.loads(response.content)

        elif method == "POST":
            async with httpx.AsyncClient() as client:

                url = self.get_url(service, path)
                headers = self.header if not user_id else {**self.header, "user_id" : str(user_id)} 

                response = await client.post(url, content=await request.body(), headers=headers)

                if response.status_code != 200:
                    raise HTTPException(status_code=response.status_code, detail=json.loads(response.content).get("detail"))
                return json.loads(response.content)

        elif method == "PUT":
            async with httpx.AsyncClient() as client:

                url = self.get_url(service, path)
                response = await client.put(url, content=await request.body(), params=request.query_params, headers={**self.header, "user_id" : str(user_id), "content-type" : "application/json"})

                if response.status_code != 200:
                    raise HTTPException(status_code=response.status_code, detail=json.loads(response.content).get("detail"))
                return json.loads(response.content)

        elif method == "DELETE":
            async with httpx.AsyncClient() as client:
                url = self.get_url(service, path)
                response = await client.delete(url, params=request.query_params, headers={**self.header, "user_id" : str(user_id)})
                
                if response.status_code != 200:
                    raise HTTPException(status_code=response.status_code, detail=json.loads(response.content).get("detail"))
                return json.loads(response.content)

    async def verify_and_create_token(
        self, 
        service : str, 
        path:str,
        request: Request,
        access_token:str,
        version:str
    ):
        try:
            payload = self.verify_jwt(self, access_token)
            return payload
        except HTTPException as e:
            raise HTTPException(status_code=e.status_code, detail=e.detail)
            # 토큰이 만료된 경우 재발급
            # if e.status_code == 401 and e.detail == "Token has expired":
                # user_id = payload.get("sub")
                # if user_id:
                #     new_token = create_access_token(data={"sub": user_id})
                #     # 헤더에 새 토큰을 추가하고 다시 요청 보냄
                #     request.headers["access_token"] = f"Bearer {new_token}"
                #     return new_token

    async def get_user_id(self, email):
        User = models.User
        user = self.db.query(User).filter(User.email == email).first()
        return UserId(
            user_id=user.user_id
        )