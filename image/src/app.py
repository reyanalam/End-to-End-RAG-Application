from typing import Union
from fastapi import FastAPI
from app.query import query_retrieval
import uvicorn
from pydantic import BaseModel
from mangum import Mangum

app = FastAPI()
handler = Mangum(app)

class QueryRequest(BaseModel):
    query: str

@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.post("/submit_query")
def submit_query_endpoint(request: QueryRequest):
    query_response = query_retrieval(request.query)
    return {"response": query_response}

if __name__ == "__main__":
    print("Starting server")
    uvicorn.run(app, host="0.0.0.0", port=8000)