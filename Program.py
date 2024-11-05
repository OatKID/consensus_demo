from typing import Union

from fastapi import FastAPI, Request
from pydantic import BaseModel
import requests

class RequestTransaction(BaseModel):
    idUser: str
    transaction: str

app = FastAPI()

@app.post("/requestTransaction")
def request_transaction(request:RequestTransaction, r:Request):
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
                respone = requests.post(f"http://localhost:{ports[i]}/ans", json=package)
                print(f"Port {ports[i]} is OK.")
            except:
                print(f"Port No.{ports[i]} is not active.")

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