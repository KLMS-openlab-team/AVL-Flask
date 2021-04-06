import flask
from flask import render_template,request,abort,session,redirect,url_for
from flask.signals import request_finished
from jinja2.utils import select_autoescape
import bcrypt
db=__import__('db')


app = flask.Flask(__name__)
app.config["DEBUG"] = True
app.config['SECRET_KEY']='secret_key_of_sdf'
books_component=__import__('books').books
books_component=books_component
login_page='index.html'
app.register_blueprint(books_component, url_prefix='/books')

@app.route('/', methods=['GET'])
def index():
    if 'username' in session:
        return redirect(url_for('dashboard'))
    return render_template(login_page,invalidlogin=False,errormsg="")

@app.route('/managebooks', methods=['GET'])
def managebooks():
    print(session,'username' not in session,'role' not in session,session['role']!='admin')
    if 'username' not in session or 'role' not in session or session['role']!='admin':
        return redirect(url_for('index'))
    try:
        db.cursor.execute("select * from book where active=1")
        queryresult = db.cursor.fetchall()
    except :
        return url_for('dashboard')
    books=[]
    for i in queryresult:
        books.append(i)
    return render_template('books/managebooks.html',books=books)


@app.route('/login', methods=['POST'])
def login():
    if not request.form or not 'username' in request.form or not 'password' in request.form:
        return render_template(login_page,invalidlogin=True,errormsg='required parameters not present')

    username=request.form['username']
    password=request.form['password']
    try:
        db.cursor.execute("select * from user where username like '{}' and active=1".format(username))
        queryresult = db.cursor.fetchall()
    except:
        return render_template(login_page,invalidlogin=True,errormsg='error occured while logging in. Try again!')
    if len(queryresult)==0 or not bcrypt.checkpw(password.encode(),queryresult[0][3].encode()):
        return render_template(login_page,invalidlogin=True,errormsg='Invalid Username/password')
    session['username']=username
    session['name']=queryresult[0][1]
    session['role']=queryresult[0][2]
    return redirect(url_for('dashboard'))

@app.route('/logout', methods=['GET'])
def logout():
    session.pop('username',None)
    session.pop('role',None)
    return redirect(url_for('index'))

@app.route('/dashboard', methods=['GET'])
def dashboard():
    if 'username' not in session:
        return redirect(url_for('index'))
    username=session['username']
    role=session['role']
    if role=='admin':
        return render_template('admin_dashboard.html', username=username)
    else:
        return render_template('student_dashboard.html', username=username)
app.run()
