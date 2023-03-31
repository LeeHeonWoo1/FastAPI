from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from starlette import status
from starlette.responses import RedirectResponse
from database import get_db
from domain.answer import answer_schema, answer_crud
from domain.question import question_crud
from domain.user.user_router import get_current_user
from models import User

router = APIRouter(
    prefix = "/api/answer",
)

# 답변 등록 라우터 함수
@router.post("/create/{question_id}", status_code = status.HTTP_204_NO_CONTENT)
def answer_create(question_id:int, _answer_create:answer_schema.AnswerCreate, db: Session=Depends(get_db), current_user:User = Depends(get_current_user)):
    # 우선 답변을 등록하기 전에 답변을 등록할 질문을 하나 가져와야 한다.
    question = question_crud.get_question(db, question_id = question_id)
    # 질문을 가져오지 않으면 아래의 에러가 발생
    if not question:
        raise HTTPException(status_code = 404, detail="Question not found")
    # 답변 등록
    answer_crud.create_answer(db, question=question, answer_create=_answer_create, user=current_user)

    # redirect
    from domain.question.question_router import router as question_router
    url = question_router.url_path_for('question_detail',
                                       question_id=question_id)
    return RedirectResponse(url, status_code=303)

@router.get("/detail/{answer_id}", response_model=answer_schema.Answer)
def answer_detail(answer_id: int, db:Session=Depends(get_db)):
    answer = answer_crud.get_answer(db, answer_id=answer_id)
    return answer

@router.put("/update", status_code=status.HTTP_204_NO_CONTENT)
def answer_update(_answer_update: answer_schema.AnswerUpdate, db:Session = Depends(get_db), current_user:User = Depends(get_current_user)):
    db_answer = answer_crud.get_answer(db, answer_id=_answer_update.answer_id)
    if not db_answer:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail="데이터를 찾을수 없습니다.")
    if current_user.id != db_answer.user.id:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="수정 권한이 없습니다.")
    answer_crud.update_answer(db=db, db_answer=db_answer, answer_update=_answer_update)

@router.delete("/delete", status_code=status.HTTP_204_NO_CONTENT)
def answer_delete(_answer_delete: answer_schema.AnswerDelete, db:Session = Depends(get_db), current_user:User = Depends(get_current_user)):
    db_answer = answer_crud.get_answer(db, answer_id=_answer_delete.answer_id)
    if not db_answer:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="답변을 찾을 수 없습니다.")
    if current_user.id != db_answer.user.id:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="삭제 권한이 없습니다.")
    answer_crud.delete_answer(db=db, db_answer=db_answer)

@router.post("/vote", status_code=status.HTTP_204_NO_CONTENT)
def answer_vote(_answer_vote: answer_schema.AnswerVote,
                db: Session = Depends(get_db),
                current_user: User = Depends(get_current_user)):
    db_answer = answer_crud.get_answer(db, answer_id=_answer_vote.answer_id)
    if not db_answer:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="데이터를 찾을수 없습니다.")
    answer_crud.vote_answer(db, db_answer=db_answer, db_user=current_user)