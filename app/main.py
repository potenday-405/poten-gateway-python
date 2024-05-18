from fastapi import FastAPI
from app.api.v1.gateway import router as v1_router

app = FastAPI(
    title="{서비스이름} gateway 서버",
    description="""
    {서비스이름}의 게이트웨이 서버.

    아래와 같은 기능을 수행하는 서버입니다
    1. 인증 및 인가
    2. 라우팅 
    """
)

app.include_router(v1_router, prefix="/api/v1", tags=["v1"])
