from fastapi import FastAPI, HTTPException, status, Path
from typing import Optional
from pydantic import BaseModel


app = FastAPI()



@app.get("/")
def root():
    return{"Testing the endpoint"}