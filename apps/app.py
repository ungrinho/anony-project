from pathlib import Path    # 경로 처리를 위한 기본 라이브러리
from flask import Flask
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_wtf.csrf import CSRFProtect
from apps.config import config



db = SQLAlchemy()

csrf = CSRFProtect()

# LoginManager를 인스턴스화한다
login_manager = LoginManager()
# login_view 속성에 미로그인 시 리다이렉트하는 엔드포인트를 지정한다
login_manager.login_view = "auth.signup"    # 로그인 안했을 때 리다이렉트
# login_message 속성에 로그인 후에 표시할 메시지를 지정한다
# 여기에서는 아무것도 표시하지 않도록 공백을 지정한다
login_manager.login_message = ""


# create_app 함수를 작성한다
# config의 키를 전달한다
def create_app(config_key):
    # 플라스크 인스턴스 생성
    app = Flask(__name__)

    # 기존의 app.config.from_mapping을 삭제하고, app.config.from_object를 사용하여 config_key에 매치하는 환경의 config클래스를 읽어들인다
    app.config.from_object(config[config_key])

    # # 앱의 config 설정을 한다
    # app.config.from_mapping(
    #     SECRET_KEY="rkskekfk",
    #     SQLALCHEMY_DATABASE_URI=
    #     f"sqlite:///{Path(__file__).parent.parent / 'local.sqlite'}",
    #     SQLALCHEMY_TRACK_MODIFICATIONS=False,
    #     # SQL을 콘솔 로그에 출력하는 설정
    #     SQLALCHEMY_ECHO=True,
    #     WTF_CSRF_SECRET_KEY="dkdmejdnjswnrrpTsp",
    # )

    csrf.init_app(app)

    # SQLALCHEMY와 앱을 연계한다
    db.init_app(app)

    # Migrate와 앱을 연계한다
    Migrate(app, db)

    # login_manager를 애플리케이션과 연계한다
    login_manager.init_app(app)

    # crud 패키지로부터 views를 import한다
    from apps.crud import views as crud_views

    # register_blueprint를 사용해 view의 crud를 앱에 등록한다 / 앱의 기능 분할(blueprint)
    app.register_blueprint(crud_views.crud, url_prefix="/crud")

    # 이제부터 작성하는 auth 패키지로부터 views를 import한다
    from apps.auth import views as auth_views

    # register_blueprint를 사용해 views의 auth를 앱에 등록한다
    app.register_blueprint(auth_views.auth, url_prefix="/auth")


    return app