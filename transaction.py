from flask import Blueprint, render_template, abort, session, flash, request
from flask.helpers import flash, url_for
from werkzeug.exceptions import PreconditionFailed
from werkzeug.utils import redirect
import bcrypt
from datetime import datetime
transaction = Blueprint('transaction', __name__,template_folder='templates')
db=__import__('db')
avl_tree=__import__('avl_tree').avl

@transaction.route('/borrowbook', methods=['GET','POST'])
def borrowbook():
    if 'username' not in session:
        return redirect(url_for('index'))
    if request.method=='GET':
        books=[]
        searchtext=request.args.get('search')
        if searchtext is None:
            searchtext=''
        books=avl_tree.searchSubString(avl_tree.root, searchtext)
        if searchtext!='':
            flash('showing books starting with "{}"'.format(searchtext))
        return render_template('transaction/borrow.html',books=books)

@transaction.route('/borrow/<bookname>', methods=['GET'])
def borrow(bookname):
    if 'username' not in session:
        return redirect(url_for('index'))
    if request.method=='GET':
        book=avl_tree.specificSearch(avl_tree.root,bookname)
        if book==None:
            flash('book not found')
        elif book.count<=0:
            flash('Cannot borrow {} since count is 0!'.format(bookname))
        else:
            try:
                db.cursor.execute("insert into borrow values('{}','{}','{}',null)".format(session['username'],bookname,datetime.now().isoformat()))
                queryresult = db.cursor.fetchall()
            except :
                flash('Error occured while borrowing book')
                return redirect(url_for('borrowbook'))
            book.count-=1
            flash('Borrowed {} successfully!'.format(bookname))
        return redirect(url_for('transaction.borrowbook'))


@transaction.route('/returnbook', methods=['GET','POST'])
def returnbook():
    if 'username' not in session:
        return redirect(url_for('index'))
    if request.method=='GET':
        # retrieve from borrow table where return_date is null
        return render_template('transaction/return.html')

@transaction.route('/return/<bookissue>', methods=['GET'])
def returnborrow(bookissue):
    if 'username' not in session:
        return redirect(url_for('index'))
    if request.method=='GET':
        reqparams=bookissue.split('#')
        if len(reqparams)!=2:
            flash('Incorrect arguments to borrow book')
        else:
            # update return_date, book count, due(in db and session)
            flash('returned {} successfully'.format(reqparams[0]))
        return redirect(url_for(returnbook))

# lost book route- update return_date to "lost", change due