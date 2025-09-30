from contextlib import asynccontextmanager
from datetime import timedelta
from hashlib import md5
from secrets import compare_digest
from functools import lru_cache
from fastapi import FastAPI, Request, Response, Depends, status
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from fastapi.encoders import jsonable_encoder
from fastapi.responses import RedirectResponse
from fastapi.middleware.cors import CORSMiddleware

from fastapi_login import LoginManager
from fastapi_login.exceptions import InvalidCredentialsException
from fastapi.security import OAuth2PasswordRequestForm

import duckdb
import json
import os
import typing as t

from starlette.responses import HTMLResponse


SECRET = "SECRET"


@asynccontextmanager
async def lifespan(app: FastAPI):
    app.state.con = duckdb.connect("db.db")
    app.state.con.sql("CREATE TABLE IF NOT EXISTS a (id int)")

    yield

    app.state.con.close()


app = FastAPI(lifespan=lifespan)

def compare_pass(password: str, password_hash: str) -> bool:
    """ Сверка хэшей паролей

    Параметры:
        password (str): пароль в незашифрованном виде
        password_hash (str): хэш пароля для сверки

    Возвращает:
        bool: булевый флаг совпадения или несовпадения
    """
    password_hash_ = md5(f'{password} + {SECRET}'.encode('utf-8')).hexdigest()
    print(password_hash_)
    return compare_digest(
        password_hash_, password_hash
    ) if password and password_hash else False


class NAE(Exception): pass

login_manager = LoginManager(
    SECRET,
    token_url="/login",
    use_cookie=True,
    not_authenticated_exception=NAE
)

@login_manager.user_loader()
async def load_user(user: str) -> dict[str, tuple[str]]:
    app.state.con.execute("select * from users where username = '%s'" % user)
    data: dict[str, tuple[str]] = {user: app.state.con.fetchone()}
    print(data)
    return data or {}

    # return {'user': user, **data} if (data := get_users().get(user, {})) else {}

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


from pathlib import Path
build = (Path(__file__).parent.parent / "client/build").resolve()

app.mount(
    "/static",
    StaticFiles(directory=build / "static", check_dir=False),
    name="static"
)

@app.get("/login")
async def login(request: Request):
    try:
        user = await login_manager.get_current_user(await login_manager._get_token(request))
        return RedirectResponse('/')
    except:
        pass
    return HTMLResponse(content=open(build / "login.html", "r").read())

@app.post("/login", response_class=HTMLResponse)
async def login_post(
    data: OAuth2PasswordRequestForm = Depends(),
):
    print(data.username)
    user_data: dict = await load_user(data.username) # type: ignore
    user, password_hash = [*user_data.get(data.username, {}), None, None][:2]
    if not user_data or not compare_pass(data.password, password_hash):
        raise InvalidCredentialsException

    response = RedirectResponse('/', status.HTTP_302_FOUND)
    access_token = login_manager.create_access_token(
        data=dict(sub=data.username), expires=timedelta(minutes=300)
    )
    login_manager.set_cookie(response, access_token)

    return response


@app.get('/logout')
async def logout():
    response = RedirectResponse(url="/login")
    for x in ('access-token',):
        response.delete_cookie(x)
    return response


@app.get("/api/emps")
async def get_emps(user = Depends(login_manager)):
    return load_emps()


@app.get("/")
async def get(request: Request):
    # If user has no access-token cookie redirect to login
    if not (token := request.cookies.get("access-token")):
        return RedirectResponse('/login')
    # Is users provided cookie is fake or invalid redirect to logout to reset it
    try:
        if (not (user := await login_manager.get_current_user(token))):
            raise InvalidCredentialsException
    except:
        return RedirectResponse('/logout')
    print(user)
    return HTMLResponse((build / "index.html").read_text())
