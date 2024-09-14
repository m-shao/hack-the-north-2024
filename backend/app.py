from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
import os
import requests

load_dotenv()

app = FastAPI()

"""
Running backend: fastapi run

https://fastapi.tiangolo.com/tutorial/cors/
"""

origins = ['*']

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/api/location")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}