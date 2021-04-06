from flask import Blueprint, render_template, abort
from flask.helpers import url_for
from werkzeug.utils import redirect
books = Blueprint('books', __name__,template_folder='templates')

@books.route('/books')
def google():
	return redirect('http://www.google.com')
