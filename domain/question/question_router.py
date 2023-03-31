from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from domain.question import question_schema, question_crud
from domain.user.user_router import get_current_user
from models import User
from starlette import status

# /api/question의 형태로 전달되는 url의 경우 이 파일이 모두 처리한다.
router = APIRouter(
    prefix='/api/question',
)

# /api/question/list : db에 올라간 데이터 리스트를 반환
@router.get('/list', response_model=question_schema.QuestionList)
def question_list(db: Session = Depends(get_db), page: int = 0, size: int = 10, keyword: str = ''):
    total, _question_list = question_crud.get_question_list(db, skip=page*size, limit=size, keyword=keyword)
    return {
        "total": total, 
        "question_list": _question_list
    }

# /api/question/detail/:question_id : db에 올라간 데이터 하나를 반환
@router.get('/detail/{question_id}', response_model = question_schema.Question)
def question_detail(question_id: int, db: Session=Depends(get_db)):
    question = question_crud.get_question(db, question_id)
    return question

# /create = db에 새로운 질문을 등록하는 url
@router.post('/create', status_code = status.HTTP_204_NO_CONTENT)
def question_create(_question_create: question_schema.QuestionCreate, db:Session = Depends(get_db), current_user:User = Depends(get_current_user)):
    question_crud.create_question(db=db, question_create=_question_create, user=current_user)

# 질문 수정 라우터
@router.put('/update', status_code=status.HTTP_204_NO_CONTENT)
def question_update(_question_update: question_schema.QuestionUpdate, db:Session = Depends(get_db), current_user:User = Depends(get_current_user)):
    # db안의 질문 한 건을 조회해서
    db_question = question_crud.get_question(db, question_id=_question_update.question_id)
    if not db_question:
        # 질문이 없으면 오류 발생
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='질문을 찾을 수 없습니다.')
    
    if current_user.id != db_question.user.id:
        # 접속해있는 user의 id값과 질문의 user id값이 다르면 오류 발생
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='수정 권한이 없습니다.')
    
    # 질문 수정
    question_crud.update_question(db = db, db_question = db_question, question_update = _question_update)

# 질문 삭제 라우터   
@router.delete('/delete', status_code=status.HTTP_204_NO_CONTENT)
def question_delete(_question_delete: question_schema.QuestionDelete, db:Session = Depends(get_db), current_user:User = Depends(get_current_user)):
    # db안의 질문 한 건을 조회해서
    db_question = question_crud.get_question(db, question_id=_question_delete.question_id)
    if not db_question:
        # 질문이 없으면 오류 발생
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='질문을 찾을 수 없습니다.')
    
    if current_user.id != db_question.user.id:
        # 접속해있는 user의 id값과 질문의 user id값이 다르면 오류 발생
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='수정 권한이 없습니다.')
    
    # 질문 삭제
    question_crud.delete_question(db = db, db_question = db_question)

@router.post("/vote", status_code=status.HTTP_204_NO_CONTENT)
def question_vote(_question_vote:question_schema.QuestionVote, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    db_question = question_crud.get_question(db, question_id=_question_vote.question_id)
    if not db_question:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="데이터를 찾을 수 없습니다.")
    question_crud.vote_question(db, db_question=db_question, db_user=current_user)