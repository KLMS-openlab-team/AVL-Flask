from flask import Blueprint, render_template, abort, session, flash, request
from flask.helpers import flash, url_for
from werkzeug.exceptions import PreconditionFailed
from werkzeug.utils import redirect
import bcrypt
transaction = Blueprint('transaction', __name__,template_folder='templates')
db=__import__('db')

@transaction.route('/borrowbook', methods=['GET','POST'])
def borrowbook():
    if 'username' not in session:
        return redirect(url_for('index'))
    if request.method=='GET':
        return render_template('transaction/borrow.html')


@transaction.route('/returnbook', methods=['GET','POST'])
def returnbook():
    if 'username' not in session:
        return redirect(url_for('index'))
    if request.method=='GET':
        return render_template('transaction/return.html')
