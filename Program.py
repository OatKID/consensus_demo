from typing import Union

from fastapi import FastAPI, Request
from pydantic import BaseModel
import requests
import httpx

class RequestTransaction(BaseModel):
    idUser: str
    transaction: str

app = FastAPI()

async def fetch(url:str, package):
    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(url, json=package)
            return response
        except httpx.RequestError:
            raise httpx.RequestError(f"{url} is not active.")

@app.post("/requestTransaction")
async def request_transaction(request:RequestTransaction, r:Request):
    ports = [8001, 8002, 8003, 8004]
    current_port = r.url.port
    package = {
        "idUser" : request.idUser,
        "transaction": request.transaction
    }
    print(f"Port {current_port} receives a request from the client.")
    for i in range(len(ports)):
        if current_port != ports[i]:
            try:
                respone = await fetch(f"http://localhost:{ports[i]}/ans", package)
                print(respone.text)
            except httpx.RequestError:
                print(f"http://localhost:{ports[i]}/ans is not active.")
    
    print("Complete")

    return {
        "idUser" : request.idUser,
        "transaction": request.transaction,
        "verify": "OK"
    }

@app.post("/ans")
def ans(request:RequestTransaction):
    print(request)
    return "OK"