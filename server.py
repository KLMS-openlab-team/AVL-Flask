from re import search
import flask
from flask import render_template,request,abort,session,redirect,url_for
from flask.helpers import flash
from flask.signals import request_finished
from jinja2.utils import select_autoescape
import bcrypt
from werkzeug.exceptions import PreconditionRequired
db=__import__('db')
avl_tree=__import__('avl_tree').avl
scrapeinfofn=__import__('book_scrape').scrapeinfo
avl_tree_info=__import__('avltree_scrape').avl_tree_info


app = flask.Flask(__name__)
app.config["DEBUG"] = True
app.config['SECRET_KEY']='secret_key_of_sdf'
login_page='index.html'
app.register_blueprint(__import__('books').books, url_prefix='/books')
app.register_blueprint(__import__('users').users, url_prefix='/users')
app.register_blueprint(__import__('transaction').transaction, url_prefix='/transaction')

@app.route('/', methods=['GET'])
def index():
    if 'username' in session:
        return redirect(url_for('dashboard'))
    return render_template(login_page)

@app.route('/testurl', methods=['GET'])
def asdfasdf():
    return render_template('child.html')
@app.route('/scrapeinfo/<bookname>', methods=['GET'])
def scrapeinfo(bookname):
    print(bookname)
    txt,img=scrapeinfofn(bookname)
    return render_template('books/bookdescription.html',bookname=bookname,txt=txt.strip(),img=img)



@app.route('/login', methods=['POST'])
def login():
    if not request.form or not 'username' in request.form or not 'password' in request.form:
        flash('required parameters not present')
        return render_template(login_page)

    username=request.form['username']
    password=request.form['password']
    try:
        db.cursor.execute("select * from user where username like '{}' and active=1".format(username))
        queryresult = db.cursor.fetchall()
    except:
        flash('error occured while logging in. Try again!')
        return render_template(login_page)
    if len(queryresult)==0 or not bcrypt.checkpw(password.encode(),queryresult[0][3].encode()):
        flash('Invalid Username/password')
        return render_template(login_page)
    session['username']=username
    session['name']=queryresult[0][1]
    session['role']=queryresult[0][2]
    session['due']=queryresult[0][5]
    return redirect(url_for('dashboard'))

@app.route('/logout', methods=['GET'])
def logout():
    session.pop('username',None)
    session.pop('role',None)
    session.pop('name',None)
    session.pop('due',None)
    return redirect(url_for('index'))

@app.route('/dashboard', methods=['GET'])
def dashboard():
    if 'username' not in session:
        return redirect(url_for('index'))
    username=session['username']
    role=session['role']
    if role=='admin':
        return render_template('admin_dashboard.html', username=username,avl_tree_info=avl_tree_info)
    else:
        return render_template('student_dashboard.html', username=username,avl_tree_info=avl_tree_info)

try:
    db.cursor.execute("select * from book where active=1")
    queryresult = db.cursor.fetchall()
    for i in queryresult:
        avl_tree.root = avl_tree.insert(avl_tree.root,i[0],i[1],i[2],i[3],i[4])
except Exception as e:
    print('Error occured while retrieving books'.join(e))
app.run()
