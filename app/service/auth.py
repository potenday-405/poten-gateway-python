from fastapi import HTTPException, Request
import jwt
import json
import httpx
from datetime import datetime, timedelta
from app.core.config import ACCESS_TOKEN_EXPIRE_MINUTES, SECRET_KEY, ALGORITHM, USER_URL, INVITATION_URL
from app.database import models
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import Literal

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
    def verify_jwt(self, token: str, token_type:Literal["A", "R"]):
        """유효한 토큰인지 확인"""
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            return payload
        except jwt.ExpiredSignatureError:
            if token_type == "A":
                raise HTTPException(status_code=401, detail="Token has expired")
            else:
                raise HTTPException(status_code=403, detail="RefreshToken has expired")
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

    async def verify_token(self, token:str, token_type:Literal["A", "R"]):
        """ 토큰 유효성 검사 

        :params token: 토큰값
        :params token_type: A : accessToken, R : refreshToken
        """
        try:
            payload = self.verify_jwt(self, token, token_type)
            return payload
        except HTTPException as e:
            raise HTTPException(status_code=e.status_code, detail=e.detail)

    async def get_user_id(self, email):
        User = models.User
        user = self.db.query(User).filter(User.email == email).first()
        return UserId(
            user_id=user.user_id
        )