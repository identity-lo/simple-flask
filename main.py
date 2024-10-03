from flask import (
    Flask , 
    render_template , 
    url_for,
    request,
    session,
    redirect,
    flash
)
from models import (
    User,
    Post
)
from authcontroller import Validate
import datetime

app = Flask(__name__)
app.secret_key = "mft-flask"
validate = Validate()

@app.route("/index")
@app.route("/")
def indexPage():
    User.create_table()
    Post.create_table()
    post = Post.select()
    get_session = session.get("username")
    if post:
        return render_template("index.html" , post=post , session=get_session)
    return render_template("index.html" , session=get_session)

@app.route("/login" , methods=["GET" , "POST"])
def loginPage():
    if request.method == "POST":
        username = request.form["username"]
        username_response = validate.username(username)
        password = request.form["password"]
        password_response = validate.password(username=username , password=password)
        get_session = session.get('username')
        print(username_response)
        print(password_response)
        if get_session:
            return redirect(url_for("dashboard"))
        
        if username_response == False and password_response == True:

            session["username"] = username
            session["last-online"] = datetime.datetime.now()
            return redirect(url_for("dashboard"))
        else:
            flash("نام کاربری یا رمز عبور وارد شده اشتباه است")
            return render_template("login.html")
    return render_template("login.html")

@app.route("/register" , methods=["GET" , "POST"])
def registerPage():
    if request.method == "POST":
        username = request.form["username"]
        username_response = validate.username(username)
        print(username_response)
        email = request.form["email"]
        email_response = validate.email(email)
        print(email_response)
        password = request.form["password"]
        confirm_password = request.form["confirm"]
        
        if username_response == True and email_response == True:
            if confirm_password != password:
                erorr = "پسورد شما درست تکرار نشده . دوباره امتحان کنید"
                return render_template("register.html" , erorr=erorr)
            session["username"] = username
            session["last-online"] = datetime.datetime.now()
            User.create(username=username , password=password,email=email) 
            return redirect(url_for("dashboard"))      
    get_session = session.get('username')
    if get_session:
        return redirect(url_for("dashboard"))
    return render_template("register.html")



        

@app.route("/dashboard" , methods=["GET" , "POST"])
def dashboard():
    get_session = session.get('username')

    if not get_session:
        return redirect(url_for("loginPage"))
    
    if request.method == "POST":
        get_title = request.form["title"]
        get_description = request.form["description"]
        Post.create(title = get_title , description=get_description , author=get_session)
        gg = "created post !"
        return render_template("dashboard.html" , gg=gg)
    return render_template("dashboard.html")

@app.route("/showpost/<author>")
def showpost(author):
    get_res = Post.select().where(Post.author == author)

    if not get_res:
        return redirect(url_for("notfound"))
    
    return render_template("showpost.html" , res=get_res)

@app.route("/404")
def notfound():
    return render_template("404.html")

@app.route("/about")
def aboutPage():

    return "سلام امیرعلیم حال نوشتن این صفحه در من وجود نداشت :)"



if __name__ == "__main__":
    app.run(debug=True)
