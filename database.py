from sqlalchemy import create_engine, MetaData
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from starlette.config import Config

config = Config('.env')
# sqlite3데이터베이스의 파일을 프로젝트 루트 디렉토리에 저장하겠다 !
SQLALCHEMY_DATABASE_URL = config('SQLALCHEMY_DATABASE_URL')

# 커넥션 풀을 생성
# 커넥션 풀? : 데이터베이스에 접속하는 객체를 일정 갯수만큼 만들어 놓고 돌려가며 사용하는 것을 말한다.
# 주로 DB에 접속하는 세션 수를 제어하고, 세션 접속에 소요되는 시간을 줄이고자 하는 용도로 사용한다.
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args = {"check_same_thread":False}
)

# 데이터베이스에 접속하기 위해 아래의 객체를 생성한다.
# 여기서 autocommit의 경우 True로 설정하게 되면 rollback으로 실수했던 사항을 수정할 수 없을 뿐더러 commit이라는 사인을 주지 않아도 자동으로 저장되기에 주의해야 한다.
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

# MetaData 클래스를 이요한 DB의 원시키, 유일키, 인덱스키 등의 이름 규칙을 새롭게 정의.
# migrations 디렉터리의 env.py파일도 수정해야함
naming_convention = {
    "ix": 'ix_%(column_0_label)s',
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(column_0_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s"
}
Base.metadata = MetaData(naming_convention=naming_convention)

# domain/question/question_router 파일을 살펴보면 db를 조회하고난 후 db.close()를 호출한다. 이는 SQLAlchemy가 사용하는
# 컨넥션 풀에 db세션이 반환되지 않아 문제가 생기기 때문인데, 이를 자동화하려면 Dependency Injection(의존성 주입)을 사용하면 자동화할 수 있다.
# Dependency Injection? : 필요한 기능을 선언하여 사용할 수 있다. 라는 의미
# yield 구문을 포함하므로 get_db는 제너레이터 객체이다.
def get_db():
    db = SessionLocal()
    # 오류에 상관없이 db.close()를 실행한다.
    try:
        yield db
    finally:
        db.close()