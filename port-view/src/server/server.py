from contextlib import asynccontextmanager
from functools import lru_cache
from fastapi import FastAPI
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware

import duckdb
import json
import os
import typing as t



@asynccontextmanager
async def lifespan(app: FastAPI):
    app.state.con = duckdb.connect("db.db")
    app.state.con.sql("CREATE TABLE IF NOT EXISTS a (id int)")

    yield

    app.state.con.close()


app = FastAPI(lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        # "*",
        "http://localhost:3000",
        "http://192.168.1.85:3000"
    ],  # фронт адрес
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@lru_cache()
def load_emps() -> dict[str, t.Any]:
    return json.loads(app.state.con.sql("SELECT * FROM emps").to_df().to_json(orient="records", force_ascii=False))


@app.get("/emps")
def get_emps():
    return load_emps()
