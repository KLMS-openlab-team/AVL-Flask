# to be modified according to user

from flask import Blueprint, render_template, abort, session, flash, request
from flask.helpers import flash, url_for
from werkzeug.exceptions import PreconditionFailed
from werkzeug.utils import redirect
books = Blueprint('books', __name__,template_folder='templates')
db=__import__('db')

@books.route('/managebooks', methods=['GET'])
def managebooks():
    print(session,'username' not in session,'role' not in session,session['role']!='admin')
    if 'username' not in session or 'role' not in session or session['role']!='admin':
        return redirect(url_for('index'))
    try:
        db.cursor.execute("select * from book where active=1")
        queryresult = db.cursor.fetchall()
    except :
        flash('Error occured while retrieving books')
        return redirect(url_for('dashboard'))
    books=[]
    for i in queryresult:
        books.append(i)
    return render_template('books/managebooks.html',books=books)

@books.route('/addbooks',methods=['GET','POST'])
def addbooks():
    print(session,'username' not in session,'role' not in session,session['role']!='admin')
    if 'username' not in session or 'role' not in session or session['role']!='admin':
        return redirect(url_for('index'))
    if request.method=='GET':
        return render_template('books/addbooks.html')
    bookname=request.form.get('bookname')
    count=request.form.get('count')
    price=request.form.get('price')
    description=request.form.get('description')
    try:
        db.cursor.execute("INSERT INTO book VALUES('harrypotter-1',3,100,1,'good book') ON DUPLICATE KEY UPDATE active=1, count=3, price=400".format(bookname))
        queryresult = db.cursor.fetchall()
    except Exception as e:
        flash('Error removing book')
        return redirect(url_for('books.managebooks'))
    flash('Removed {} book Successfully!'.format(bookname))
    return redirect(url_for('books.managebooks'))

@books.route('/deletebook/<bookname>',methods=['GET'])
def deletebook(bookname):
    # print(session,'username' not in session,'role' not in session,session['role']!='admin')
    if 'username' not in session or 'role' not in session or session['role']!='admin':
        return redirect(url_for('index'))
    try:
        db.cursor.execute("update book set active=0 where bookname like '{}'".format(bookname))
        queryresult = db.cursor.fetchall()
    except Exception as e:
        flash('Error removing book')
        return redirect(url_for('books.managebooks'))
    flash('Removed {} book Successfully!'.format(bookname))
    return redirect(url_for('books.managebooks'))