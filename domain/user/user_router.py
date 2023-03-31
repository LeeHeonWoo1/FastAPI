from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from jose import jwt, JWTError
from sqlalchemy.orm import Session
from starlette import status
from database import get_db
from starlette.config import Config

from domain.user import user_crud, user_schema
from domain.user.user_crud import pwd_context

from datetime import timedelta, datetime

config = Config('.env')
ACCESS_TOKEN_EXPIRE_MINUTES = int(config('ACCESS_TOKEN_EXPIRE_MINUTES'))
SECRET_KEY = config('SECRET_KEY')
ALGORITHM = "HS256"
oauth2_schema = OAuth2PasswordBearer(tokenUrl="/api/user/login")

router = APIRouter(
  prefix='/api/user',
)

@router.post('/create', status_code=status.HTTP_204_NO_CONTENT)
def user_create(_user_create: user_schema.UserCreate, db:Session = Depends(get_db)):
  user = user_crud.get_existing_user(db, user_create=_user_create)
  if user:
    raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail='이미 존재하는 사용자입니다.')
  user_crud.create_user(db=db, user_create=_user_create)

@router.post("/login", response_model=user_schema.Token)
def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(),
                           db: Session = Depends(get_db)):

    # check user and password
    user = user_crud.get_user(db, form_data.username)
    if not user or not pwd_context.verify(form_data.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # make access token
    data = {
        "sub": user.username,
        "exp": datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    }
    access_token = jwt.encode(data, SECRET_KEY, algorithm=ALGORITHM)

    return {"access_token":access_token, "token_type": "bearer", "username": user.username}

# token : FastAPI의 security패키지에 있는 OAuth2PasswordBearer에 의해 자동으로 매핑
def get_current_user(token: str = Depends(oauth2_schema), db:Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        # 토큰을 복호화하여 토큰에 담겨있는 사용자명을 얻어낼 수 있다. 만약 사용자명이 없거나 해당 사용자 명으로 사용자 데이터 조회에 실패할 경우에는 credential_exceptions를 발생시킨다.
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    else:
        user = user_crud.get_user(db, username=username)
        if user is None:
            raise credentials_exception
        return user
