from models import Question, User, Answer
from sqlalchemy.orm import Session
from datetime import datetime
from domain.question.question_schema import QuestionCreate, QuestionUpdate

# 리턴하는 유형 : [<Question 객체>, <Question 객체2>, ....]
def get_question_list(db: Session, skip: int = 0, limit: int = 10, keyword: str = ''):
    question_list = db.query(Question)
    if keyword:
        # 쿼리문의 검색어로 사용할 변수
        search = '%%{}%%'.format(keyword)
        # 일일이 다 join하기 힘든 관계로 sub query생성
        # 조회 테이블 : Answer의 question_id, Answer의 content(글 내용), User.username(유저 아이디)
        # outer join : User, Answer.user_id == User.id인 요소들을 outerjoin
        # subquery와 question outerjoin
        sub_query = db.query(Answer.question_id, Answer.content, User.username).outerjoin(User, Answer.user_id == User.id).subquery()
        question_list = question_list.outerjoin(User).outerjoin(sub_query, sub_query.c.question_id == Question.id) \
                    .filter(Question.subject.ilike(search) |
                            Question.content.ilike(search) |
                            User.username.ilike(search) |
                            sub_query.c.content.ilike(search) |
                            sub_query.c.username.ilike(search))

    total = question_list.distinct().count()
    new_question_list = question_list.order_by(Question.create_date.desc()).offset(skip).limit(limit).distinct().all()
    return total, new_question_list

# 리턴하는 유형 : <Question 객체>
def get_question(db: Session, question_id: int):
    question = db.query(Question).get(question_id)
    return question

# 질문을 만들어서 db에 등록하는 함수
def create_question(db:Session, question_create: QuestionCreate, user:User):
    db_question = Question(subject = question_create.subject, 
                           content = question_create.content, 
                           create_date = datetime.now(), user=user)

    db.add(db_question)
    db.commit()

# db에 등재된 질문을 수정. 기존의 값을 업데이트되는 새로운 값으로 할당, 수정 일시는 datetime.now()를 이용
def update_question(db: Session, db_question:Question, question_update:QuestionUpdate):
    db_question.subject = question_update.subject
    db_question.content = question_update.content
    db_question.modify_date = datetime.now()
    db.add(db_question)
    db.commit()

def delete_question(db:Session, db_question:Question):
    db.delete(db_question)
    db.commit()

def vote_question(db:Session, db_question:Question, db_user = User):
    db_question.voter.append(db_user)
    db.commit()