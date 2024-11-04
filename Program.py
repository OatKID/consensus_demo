from typing import Union

from fastapi import FastAPI
from pydantic import BaseModel
import requests

class RequestTransaction(BaseModel):
    idUser: str
    transaction: str

app = FastAPI()

@app.post("/requestTransaction")
def request_transaction(request:RequestTransaction):
    return request