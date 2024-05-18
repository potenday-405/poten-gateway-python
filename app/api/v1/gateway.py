# 라우팅

from fastapi import APIRouter, Request, HTTPException
import httpx

router = APIRouter()

SERVICES = {
    "user" : "user 도메인",
    "event" : "event 도메인"
}

@router.api_route("/{service}/{path:path}", methods=["GET", "POST", "PUT", "DELETE"])
async def proxy_request(service:str, path:str, request:Request):
    if service not in SERVICES:
        return {
            "error" : "Service not found"
        }

    url = f"{SERVICES[service]}/{path}"

    async with httpx.AsyncClient() as client:
        try:
            if request.method == "GET":
                response = await client.get(url, params=request.query_params)
            elif request.method == "POST":
                response = await client.post(url, content=await request.body())
            elif request.method == "PUT":
                response = await client.put(url, content=await request.body())
            elif request.method == "DELETE":
                response = await client.delete(url)
            else:
                raise HTTPException(status_code=405, detail="Method not allowed")

            return response.json()
        except httpx.RequestError as exc:
            raise HTTPException(status_code=500, detail=str(exc))