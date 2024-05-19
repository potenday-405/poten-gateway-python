from fastapi import FastAPI
from app.api.v1.gateway import router as v1_router

app = FastAPI(
    title="{서비스이름} gateway 서버",
    description="""
    서비스 서버
        1. user (회원)
        2. invitation (초대)

    아래와 같은 기능을 수행
        1. 인증 및 인가
        2. 각 서비스를 담당하는 서버에 라우팅 
    """
)

app.include_router(v1_router, tags=["gateway"])