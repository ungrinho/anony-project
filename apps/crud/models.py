from datetime import datetime

from apps.app import db
from werkzeug.security import generate_password_hash

# db.Model을 상속한 User 클래스를 작성한다
class User(db.Model):

    # 테이블명을 지정한다
    __tablename__ = "users"

    # 컬럼을 정의한다
    # primary_key : 이 데이터를 상징하는 식별값
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, index=True)
    email = db.Column(db.String, unique=True, index=True)
    password_hash = db.Column(db.String)
    created_at = db.Column(db.DateTime, default=datetime.now)
    updated_at = db.Column(
        db.DateTime, default=datetime.now, onupdate=datetime.now
    )

    # 비밀번호를 설정하기 위한 프로퍼티
    # 속성값 getter
    @property
    def password(self):
        raise AttributeError("읽어 들일 수 없음")
    
    # 비밀번호를 설정하기 위해 setter 함수로 해시화한 비밀번호를 설정한다
    # 속성값 setter
    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)