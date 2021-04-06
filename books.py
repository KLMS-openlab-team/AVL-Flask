from flask import Blueprint, render_template, abort, session, flash, request
from flask.helpers import flash, url_for
from werkzeug.exceptions import PreconditionFailed
from werkzeug.utils import redirect
books = Blueprint('books', __name__,template_folder='templates')
db=__import__('db')
avl_tree=__import__('avl_tree').avl
root = None
@books.route('/managebooks', methods=['GET'])
def managebooks():
    print(session,'username' not in session,'role' not in session,session['role']!='admin')
    if 'username' not in session or 'role' not in session or session['role']!='admin':
        return redirect(url_for('index'))
    try:
        searchResult = []
        avl_tree.Inorder(avl_tree.root,searchResult)
    except :
        flash('Error occured while retrieving books')
        return redirect(url_for('dashboard'))
    
    return render_template('books/managebooks.html',books=searchResult)

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
        avl_tree.root = avl_tree.insert(avl_tree.root,bookname,count,price,1,description)
    except Exception as e:
        flash('Error adding book')
        return redirect(url_for('books.managebooks'))
    flash('Added book Successfully!')
    return redirect(url_for('books.managebooks'))

@books.route('/modifybooks/<bookname>',methods=['GET','POST'])
def modifybooks(bookname):
    print(session,'username' not in session,'role' not in session,session['role']!='admin')
    if 'username' not in session or 'role' not in session or session['role']!='admin':
        return redirect(url_for('index'))
    node = avl_tree.specificSearch(avl_tree.root,bookname)
    print(node.bookname)
    if(node is not None):
        if request.method=='GET':
            return render_template('books/modifybooks.html',node=node)
        node.count=request.form.get('count')
        node.price=request.form.get('price')
        node.description=request.form.get('description')
    else:
        flash('Error updating book')
        return redirect(url_for('books.managebooks'))
    flash('Updated book Successfully!')
    return redirect(url_for('books.managebooks'))

@books.route('/deletebook/<bookname>',methods=['GET'])
def deletebook(bookname):
    # print(session,'username' not in session,'role' not in session,session['role']!='admin')
    if 'username' not in session or 'role' not in session or session['role']!='admin':
        return redirect(url_for('index'))
    try:
        avl_tree.root = avl_tree.delete(avl_tree.root,bookname)
    except Exception as e:
        flash('Error removing book')
        return redirect(url_for('books.managebooks'))
    flash('Removed {} book Successfully!'.format(bookname))
    return redirect(url_for('books.managebooks'))

@books.route('/updatedb',methods=['GET'])
def updatedb():
    if 'username' not in session or 'role' not in session or session['role']!='admin':
        return redirect(url_for('index'))
    try:
        searchResult = []
        avl_tree.Inorder(avl_tree.root,searchResult)
        db.cursor.execute("UPDATE book SET active=0")
        for i in searchResult:
            db.cursor.execute("INSERT INTO book VALUES('{}',{},{},1,'{}') ON DUPLICATE KEY UPDATE count={}, price={}, active=1, description='{}'".format(i[0],i[1],i[2],i[4],i[1],i[2],i[4]))
        queryresult = db.cursor.fetchall()
    except Exception as e:
        flash('Error updating db:{0}'.format(e))
        return redirect(url_for('books.managebooks'))
    flash('Updated db Successfully!')
    return redirect(url_for('books.managebooks'))