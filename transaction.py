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


@transaction.route('/returnbook', methods=['GET'])
def returnbook():
    if 'username' not in session:
        return redirect(url_for('index'))
    if request.method=='GET':
        try:
            db.cursor.execute("select * from borrow where username like '{}' and returndatetime is null".format(session['username']))
            queryresult = db.cursor.fetchall()
        except Exception as e:
            print(e)
            flash('Error occured while retrieving borrowed books')
            return redirect(url_for('dashboard'))
        books=[]
        for i in queryresult:
            tdict={}
            tdict['bookname']=i[1]
            tmp=datetime.fromisoformat(i[2])
            tdict['issuedate']=tmp.strftime("%x")
            tdict['issuetime']=tmp.strftime("%X")
            tdict['issuedatetime']=i[2]
            books.append(tdict)
        return render_template('transaction/return.html',books=books)

@transaction.route('/return/<bookissue>', methods=['GET'])
def returnborrow(bookissue):
    if 'username' not in session:
        return redirect(url_for('index'))
    if request.method=='GET':
        reqparams=bookissue.split('$')
        if len(reqparams)!=2:
            flash('Incorrect arguments to borrow book')
        else:
            reqparams[1]=datetime.fromisoformat(reqparams[1])
            try:

                presentdate=datetime.now()
                diff=presentdate-reqparams[1]
                extradue=max(int(diff.days)-7,0)*2
                print(extradue)
                book=avl_tree.specificSearch(avl_tree.root,reqparams[0])
                if book==None:
                    flash('book not found. Contact admin!')
                book.count+=1
                print(book.count)
                print(session['due'])
                session['due']=int(session['due'])+extradue
                print(session['due'])
                db.cursor.execute("update borrow set returndatetime='{}' where username like '{}' and issuedatetime like '{}' and bookname like '{}'".format(presentdate.isoformat(),session['username'],reqparams[1].isoformat(),reqparams[0]))
                queryresult = db.cursor.fetchall()
                db.cursor.execute("update user set due=due+{} where username like '{}'".format(extradue,session['username']))
                queryresult = db.cursor.fetchall()

            except Exception as e:
                print(e)
                flash('Error occured while returning book')
                return redirect(url_for('dashboard'))
            flash('returned {} successfully'.format(reqparams[0]))
        return redirect(url_for('transaction.returnbook'))


@transaction.route('/lost/<bookissue>', methods=['GET'])
def lostborrow(bookissue):
    if 'username' not in session:
        return redirect(url_for('index'))
    if request.method=='GET':
        reqparams=bookissue.split('$')
        if len(reqparams)!=2:
            flash('Incorrect arguments to lost book')
        else:
            reqparams[1]=datetime.fromisoformat(reqparams[1])
            try:
                presentdate=datetime.now()
                diff=presentdate-reqparams[1]
                extradue=max(int(diff.days)-7,0)*2
                print(extradue)
                book=avl_tree.specificSearch(avl_tree.root,reqparams[0])
                if book==None:
                    flash('book not found. Contact admin!')
                extradue+=book.price
                print(book.count)
                print(session['due'])
                session['due']=int(session['due'])+extradue
                print(session['due'])
                db.cursor.execute("update borrow set returndatetime='{}' where username like '{}' and issuedatetime like '{}' and bookname like '{}'".format('lost',session['username'],reqparams[1].isoformat(),reqparams[0]))
                queryresult = db.cursor.fetchall()
                db.cursor.execute("update user set due=due+{} where username like '{}'".format(extradue,session['username']))
                queryresult = db.cursor.fetchall()

            except Exception as e:
                print(e)
                flash('Error occured while reporting loss of book')
                return redirect(url_for('dashboard'))
            flash('Book loss reported successfully and price of book {} is added to your due'.format(reqparams[0]))
        return redirect(url_for('transaction.returnbook'))