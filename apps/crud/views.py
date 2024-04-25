from flask import Blueprint, render_template, redirect, url_for

from apps.crud.forms import UserForm

# db를 import한다
from apps.app import db

# User 클래스를 import한다
from apps.crud.models import User



# Blueprint로 crud앱을 생성한다
crud = Blueprint(
    "crud",
    __name__,
    template_folder="templates",
    static_folder="static",
)


# index 엔드포인트를 작성하고 index.html을 반환한다
@crud.route("/")
def index():
    return render_template("crud/index.html")

@crud.route("/sql")
def sql():
    # # db.session.query(User).all()        # 모델 객체를 이용하는 경우에는 User.query.all()   # 모든 데이터 가져오기

    # # db.session.query(User).first()         # 레코드 1건 가져오기

    # # db.session.query(User).get(2)   # 레코드 2건 가져오기

    # # db.session.query(User).count()  # 레코드 개수 가져오기

    # # paginate(page=None, per_page=None, error_out=True, max_per_page=None)   #페이지네이션 객체가져오기
    # # db.session.query(User).paginate(2, 10, False)   # 한 페이지에 10건 표시하고 두번째 페이지 표시하기
    # # db.session.query(User).filter_by(id=2, username="admin").all()    # id가 2이고 username이 admin인 레코드 가져오기
    # # db.session.query(User).filter(User.id==2, User.username=="admin").all()   # id가 2이고 username 레코드 가져오기
    # # db.session.query(User).limit(1).all() # 가져올 레코드의 개수를 1건으로 지정하기
    # # db.session.query(User).limit(1).offset(2).all() # 3번의 레코드로부터 1건 가져오기
    # # db.session.query(User).order_by("username").all()   # username을 정렬
    # # db.session.query(User).group_by("username").all()   # username을 그룹화


    # # INSERT하기
    # # 사용자 모델 객체를 작성한다

    # user = User(
    # username="사용자명",
    # email="flaskbook@example.com",
    # password="비밀번호"
    # )
    # # # 사용자를 추가한다
    # # db.session.add(user)
    # # # 커밋한다
    # # db.session.commit()

    # # # UPDATE하기
    # # user = db.session.query(User).filter_by(id=1).first()
    # # user.username = "사용자명2"
    # # user.email = "flashbook2@example.com"
    # # user.password = "비밀번호2"
    # # db.session.add(user)
    # # db.session.commit()

    # # DELETE하기
    # user = db.session.query(User).filter_by(id=1).delete()
    # db.session.commit


    return "콘솔 로그를 확인해 주세요"

    
@crud.route("/users/new", methods=["GET", "POST"])
def create_user():

    # UserForm을 인스턴스화한다
    form = UserForm()
    # 폼의 값을 검증한다
    if form.validate_on_submit():
        # 사용자를 작성한다
        user = User(
            username=form.username.data,
            email=form.email.data,
            password=form.password.data,
        )
        # 사용자를 추가하고 커밋한다
        db.session.add(user)
        db.session.commit()
        # 사용자의 일람 화면으로 리다이렉트한다
        return redirect(url_for("crud.users"))
    return render_template("crud/create.html", form=form)

@crud.route("/users")
def users():
    """사용자의 일람을 취득한다"""
    users = User.query.all()
    return render_template("crud/index.html", users=users)


# methods에 GET과 POST를 지정한다
@crud.route("/users/<user_id>", methods=["GET", "POST"])
def edit_user(user_id):
    form = UserForm()

    # User 모델을 이용하여 사용자를 취득한다
    user = User.query.filter_by(id=user_id).first()

    # form으로부터 제출된 경우는 사용자를 갱신하여 사용자의 일람 화면으로 리다이렉트한다
    if form.validate_on_submit():
        user.username = form.username.data
        user.email = form.email.data
        user.password = form.password.data
        db.session.add(user)
        db.session.commit()
        return redirect(url_for("crud.users"))
    
    # GET의 경우는 HTML을 반환한다
    return render_template("crud/edit.html", user=user, form=form)

@crud.route("/users/<user_id>/delete", methods=["POST"])
def delete_user(user_id):
    user=User.query.filter_by(id=user_id).first()
    db.session.delete(user)
    db.session.commit ( )
    return redirect(url_for("crud.users"))