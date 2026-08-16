from fastapi import FastAPI, Query
from pydantic import BaseModel, ConfigDict
from fastapi.testclient import TestClient

app = FastAPI()

class PagParams(BaseModel):
    model_config = ConfigDict(extra="forbid")
    skip: int = 0
    limit: int = 100

@app.get("/items/")
def read_items(params: PagParams = Query(...)):
    return params

client = TestClient(app)

print(client.get("/items/?skip=5").json())
print(client.get("/items/?skip=5&extra=42").status_code)
print(client.get("/items/?skip=5&extra=42").json())
