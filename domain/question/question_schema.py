import datetime
from pydantic import BaseModel, validator
from domain.answer.answer_schema import Answer
from domain.user.user_schema import User
from typing import Union

class Question(BaseModel):
    id: int
    subject: str
    content: str
    create_date: datetime.datetime
    answers: list[Answer] = []
    # Question 모델을 Question스키마에 매핑 시 자동으로 값이 채워질것이다.(orm_mode = True)
    user: Union[User, None]
    modify_date: Union[datetime.datetime, None]
    voter: list[User] = []

    class Config:
        orm_mode = True

class QuestionCreate(BaseModel):
    subject: str
    content: str

    @validator('subject', 'content')
    def not_empty(cls, v):
        # subject와 content에는 기본값이 부여되지 않아 필수항목이다.
        # 그에 따른 예외처리를 할 구문
        if not v or not v.strip():
            raise ValueError('빈 값은 허용되지 않습니다')
        return v
    
class QuestionList(BaseModel):
    total: int = 0
    question_list: list[Question] = []

# 질문 수정
# QuestionCreate를 상속함으로 빈값허용불가, subject, content속성에 question_id가 추가된 셈이다.
class QuestionUpdate(QuestionCreate):
    question_id: int

class QuestionDelete(BaseModel):
    question_id: int

class QuestionVote(BaseModel):
    question_id: int