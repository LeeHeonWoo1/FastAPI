from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, Table
from sqlalchemy.orm import relationship
from database import Base

question_voter = Table(
    'question_voter',
    Base.metadata,
    # 원래 한 테이블에는 하나의 id만 들어가지만, 추천 테이블의 경우 user의 id와 question의 id를 동시에 가진다.
    # 한 명의 사용자가 여러개의 질문을 추천할 수 있고 반대로 한 개의 질문을 여러명의 유저가 추천할 수 있는 구조이다.
    # 하지만 어디까지나 primary키로 지정된 값이기에 모두 다 동일한 값을 가지게 되면 오류가 발생한다.
    Column('user_id', Integer, ForeignKey('user.id'), primary_key=True),
    Column('question_id', Integer, ForeignKey('question.id'), primary_key=True)
)

answer_voter = Table(
    'answer_voter',
    Base.metadata,
    Column('user_id', Integer, ForeignKey('user.id'), primary_key = True),
    Column('answer_id', Integer, ForeignKey('answer.id'), primary_key = True),
)

class Question(Base):
    # 테이블 이름 지정
    __tablename__ = "question"

    # id : 원시키(중복값 불허), 정수
    id = Column(Integer, primary_key=True)
    # sub : 공백 불허, 문자열
    subject = Column(String, nullable=False)
    # content : 공백 불허, 문자
    content = Column(Text, nullable=False)
    # create_date = 공백 불허, 시간
    create_date = Column(DateTime, nullable=False)
    # User <--> Question 연결
    user_id = Column(Integer, ForeignKey("user.id"), nullable=True)
    # Question에서 User를 참조하기 위한 속성.
    user = relationship("User", backref="question_users")
    # 질문 답변 수정 일시 확인용
    modify_date = Column(DateTime, nullable=True)
    # 교차 테이블 생성
    voter = relationship('User', secondary=question_voter, backref='question_voters')

class Answer(Base):
    __tablename__ = "answer"

    # id : 원시키(중복값 불허), 숫자
    id = Column(Integer, primary_key=True)
    # content : 공백 불허, 문자
    content = Column(Text, nullable=False)
    # create_date = 공백 불허, 시간
    create_date = Column(DateTime, nullable=False)
    # ques_id : 외래키(연결), 정수
    question_id = Column(Integer, ForeignKey("question.id"))
    # ques : relationship(참조할 모델명, 역참조설정) => 역참조ex) 이를테면 질문에서 거꾸로 답변을 참조하는 행위
    question = relationship("Question", backref="answers")
    # User <--> Answer 연결
    user_id = Column(Integer, ForeignKey("user.id"), nullable=True)
    # Answer에서 User를 참조하기 위한 속성
    user = relationship("User", backref = "answer_users")
    # 질문 답변 수정 일시 확인용
    modify_date = Column(DateTime, nullable=True)
    # 교차 테이블 생성
    voter = relationship('User', secondary=answer_voter, backref = 'answer_voters')
    
class User(Base):
    __tablename__ = 'user'
    
    id = Column(Integer, primary_key = True)
    username = Column(String, unique=True, nullable = False)
    password = Column(String, nullable = False)
    email = Column(String, unique=True, nullable = False)