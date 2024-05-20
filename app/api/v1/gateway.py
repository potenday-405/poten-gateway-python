# 라우팅

from fastapi import APIRouter, Request, HTTPException, Header
import httpx

router = APIRouter()

SERVICES = {
    "user" : "user 도메인",
    "invitation" : "10.0.5.6:8080"
}

# :path -> "/"를 경로 안에 포함할 수 있게끔 처리
@router.api_route("/{service}/{path:path}",methods=["GET", "POST", "PUT", "DELETE"])
async def proxy_request(service:str, path:str, request:Request, version: str = Header("1.0")):
    if service not in SERVICES:
        raise HTTPException(status_code=404, detail="Service not found")

        url = f"{SERVICES[service]}/{path}"

    async with httpx.AsyncClient() as client:
        try:
            if request.method == "GET":
                # response = {
                #     "service" : service, 
                #     "path" : path,
                #     "header" : version
                # }
                response = await client.get(url, params=request.query_params, header=version)
            elif request.method == "POST":
                response = await client.post(url, content=await request.body(), header=version)
            elif request.method == "PUT":
                response = await client.put(url, content=await request.body(), header=version)
            elif request.method == "DELETE":
                response = await client.delete(url, header=version)
            else:
                raise HTTPException(status_code=405, detail="Method not allowed")

            return response.json()
        except httpx.RequestError as exc:
            raise HTTPException(status_code=500, detail=str(exc))