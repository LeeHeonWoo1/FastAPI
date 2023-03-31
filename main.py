from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from starlette.responses import FileResponse
from starlette.staticfiles import StaticFiles

from domain.question import question_router
from domain.answer import answer_router
from domain.user import user_router

app = FastAPI()

origins = ["http://127.0.0.1:5173"]

# Block CORS Error
app.add_middleware(
    CORSMiddleware,
    allow_origins = origins,
    allow_credentials = True,
    allow_methods = ["*"],
    allow_headers=["*"]
)

# http://127.0.0.1:8000/docs에서 api테스팅도 가능하다. 실행가능한 문서 대신 읽기만 가능한 문서를 보고싶다면 http://127.0.0.1:8000/redoc으로 !
# 이 함수는 svelte에서 호출 할 예정인데, CORS 정책에 의해 프론트에서 백엔드 서버로 호출이 불가하다. (CORS 란? - https://developer.mozilla.org/ko/docs/Web/HTTP/CORS)
# 따라서 starlette을 import 하고, 예외처리를 진행한다.
# @app.get('/hello')
# def hello():
#     return {"message":"start project about pybo!"}

app.include_router(user_router.router)
app.include_router(question_router.router)
app.include_router(answer_router.router)
app.mount("/assets", StaticFiles(directory="frontend/dist/assets"))

@app.get("/")
def index():
    return FileResponse("frontend/dist/index.html")