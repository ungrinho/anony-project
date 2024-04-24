from email_validator import validate_email, EmailNotValidError
from flask import (Flask, 
                   render_template, 
                   url_for, 
                   request, 
                   redirect,
                   flash,)
import logging
import os

# from flask_debugtoolbar import DebugToolbarExtnension

from flask_mail import Mail, Message


# 서버 프로그램 객체를 만든다.
# __name__: 실행중인 모듈의 시스템 상 이름
app = Flask(__name__)

app.config["SECRET_KEY"] = "2KWKWKWKWKWK$ysys"  

app.logger.setLevel(logging.DEBUG)

# # 리다이렉트를 중단하지 않도록 한다.
# app.config["DEBUG_TB_INTERCEPT_REDIRECTS"] = False

# # DebugToolbarExtension에 애플리케이션을 설정한다
# toolbar = DebugToolbarExtnension(app)


# Mail클래스의 config를 추가한다
app.config["MAIL_SERVER"] = os.environ.get("MAIL_SERVER")
app.config["MAIL_PORT"] = os.environ.get("MAIL_PORT")
app.config["MAIL_USE_TLS"] = os.environ.get("MAIL_USE_TLS")
app.config["MAIL_USERNAME"] = os.environ.get("MAIL_USERNAME")
app.config["MAIL_PASSWORD"] = os.environ.get("MAIL_PASSWORD")
app.config["MAIL_DEFAULT_SENDER"] = os.environ.get("MAIL_DEFAULT_SENDER")

# flask-mail 확장을 등록한다.
mail = Mail(app)


# 기본 주소로 요청이 왔을 때 무엇을 할지 정의하기
@app.route("/")
def index():
    return "Hello, Flaskbook!"


# 엔드포인트명을 지정하지 않으면 함수명이 엔드포인트명이 된다.
# 메소드에 따른 처리를 원한다면 구별해서 정의할 수 있다.
@app.route("/hello/<name>", 
           methods=["GET", "POST"],
           endpoint="hello-endpoint")
def hello(name) :
    return f'Hello, {name}!!'


# @app.route("/hello", methods=["GET"],
#            endpoint="hello-endpoint")
# def hello() :
#     return "Hello, World!"

# show_name 엔드포인트를 작성한다.
@app.route("/name/<name>")
def show_name(name):
    #변수를 템플릿 엔진에게 건넨다
    return render_template("index.html", name=name)


with app.test_request_context():
    #/
    print(url_for("index"))
    #/hello/world
    print(url_for("hello-endpoint", name="world"))
    # /name/AK?page=1
    print(url_for("show_name", name="AK", page="1"))    



# 플라스크의 템플릿 문서는 앱 내 templates폴더에 있다고 가정한다.
@app.route("/contact")
def contact():
    return render_template("contact.html")


# view
# post요청이 오면, 필요한 데이터 관련 처리를 하고난서 contact_complete.html 템플릿을 주는 get처리를 하면서 마무리
@app.route("/contact/complete", methods=["GET", "POST"])
def contact_complete():
    if request.method == "POST":
       
        

        # form 속성을 사용해서 폼의 값을 취득한다.
        username = request.form["username"]
        email = request.form["email"]
        description = request.form["description"]


        #입력 체크
        is_valid = True

        if not username:
            flash("사용자명은 필수입니다.")
            is_valid = False

        if not email:
            flash("메일 주소는 필수입니다 ")
            is_valid = False

        try:
            validate_email(email)
        except EmailNotValidError:
            flash("메일 주소의 형식으로 입력해 주세요")
            is_valid = False

        if not description:
            flash("문의 내용은 필수입니다")
            is_valid = False

        if not is_valid:
            return redirect(url_for("contact"))
        
        # 이메일을 보낸다.
        send_email(
            email,
            "문의 감사합니다.",
            "contact_mail",
            username=username,
            description=description,
        )

        #문의 완료 엔드포인트로 리다이렉트한다.
        flash("문의해 주셔서 감사합니다.")

        # contact 엔드포인트로 리다이렉드 한다.
        return redirect(url_for("contact_complete"))
    
    return render_template("contact_complete.html")

def send_email(to, subject, template, **kwargs):
    """메일을 송신하는 함수"""
    msg = Message(subject, recipients=[to])
    msg.body = render_template(template + ".txt", **kwargs)
    msg.html = render_template(template + ".html", **kwargs)
    mail.send(msg)

