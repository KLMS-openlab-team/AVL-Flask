from flask import Blueprint, render_template, abort, session, flash, request
from flask.helpers import flash, url_for
from werkzeug.exceptions import PreconditionFailed
from werkzeug.utils import redirect
import bcrypt
users = Blueprint('users', __name__,template_folder='templates')
db=__import__('db')

@users.route('/manageusers', methods=['GET'])
def manageusers():
    if 'username' not in session or 'role' not in session or session['role']!='admin':
        return redirect(url_for('dashboard'))
    try:
        db.cursor.execute("select * from user where active=1")
        queryresult = db.cursor.fetchall()
    except :
        flash('Error occured while retrieving users')
        return redirect(url_for('dashboard'))
    users=[]
    for i in queryresult:
        users.append(i)
    return render_template('users/manageusers.html',users=users)

@users.route('/addusers',methods=['GET','POST'])
def addusers():
    if 'username' not in session or 'role' not in session or session['role']!='admin':
        return redirect(url_for('dashboard'))
    if request.method=='GET':
        return render_template('users/addusers.html')
    username=request.form.get('username')
    name=request.form.get('name')
    role=request.form.get('role')
    password=request.form.get('password')
    password=bcrypt.hashpw(password.encode(),bcrypt.gensalt(12)).decode()

    try:
        db.cursor.execute("INSERT INTO user VALUES('{}','{}','{}','{}',1,0) ON DUPLICATE KEY UPDATE name='{}', role='{}', password='{}', active=1, due=0".format(username,name,role,password,name,role,password))
        queryresult = db.cursor.fetchall()
    except Exception as e:
        print(e)
        flash('Error adding user')
        return redirect(url_for('users.manageusers'))
    flash('Added {} user Successfully!'.format(username))
    return redirect(url_for('users.manageusers'))

@users.route('/modifyuser/<username>',methods=['GET','POST'])
def modifyuser(username):
    if 'username' not in session or 'role' not in session or session['role']!='admin':
        return redirect(url_for('dashboard'))
    if request.method=='GET':
        try:
            db.cursor.execute("select * from user where username like '{}'".format(username))
            queryresult = db.cursor.fetchall()
        except Exception as e:
            print(e)
            flash('Error occured while retrieving users')
            return redirect(url_for('users.manageusers'))
        if len(queryresult)==0:
            flash('error occured while modifying user')

        return render_template('users/modifyusers.html',qr=queryresult[0])
    name=request.form.get('name')
    role=request.form.get('role')
    due=request.form.get('due')
    try:
        db.cursor.execute("update user set name='{}', role='{}', due='{}' where username like '{}'".format(name,role,due,username))
        queryresult = db.cursor.fetchall()
    except Exception as e:
        print(e)
        flash('Error modifying user')
        return redirect(url_for('users.manageusers'))
    flash('Modified {} user Successfully!'.format(username))
    return redirect(url_for('users.manageusers'))

@users.route('/deleteuser/<username>',methods=['GET'])
def deleteuser(username):
    if 'username' not in session or 'role' not in session or session['role']!='admin':
        return redirect(url_for('dashboard'))
    try:
        db.cursor.execute("update user set active=0 where username like '{}'".format(username))
        queryresult = db.cursor.fetchall()
    except Exception as e:
        flash('Error removing user')
        return redirect(url_for('users.manageusers'))
    flash('Removed {} Successfully!'.format(username))
    return redirect(url_for('users.manageusers'))