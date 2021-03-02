from flask import *
from datetime import datetime
from werkzeug.utils import secure_filename
from jinja2 import evalcontextfilter, Markup, escape
from uuid import uuid4
import re
import os

with open('SECRET_KEY', encoding='utf-8') as f:
	SECRET_KEY = f.read()

UPLOAD_FOLDER = 'static/uploads'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'bmp', 'gif'}
# session['refresh_time'] = 60
paragraph_re = re.compile(r'(?:\r\n|\r|\n){2,}')
pointer_re = re.compile(r'(&gt;&gt;[0-9]+)\w+')

if not os.path.isdir(UPLOAD_FOLDER):
	os.mkdir(UPLOAD_FOLDER)

app = Flask(__name__)
app.config['SECRET_KEY'] = SECRET_KEY
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 2 * 1024 * 1024

@app.template_filter()
@evalcontextfilter
def nl2br(eval_ctx, value):
	nl = '\n'
	result = '\n\n'.join(f"<p>{p.replace(nl, '<br>nl')}</p>" for p in paragraph_re.split(escape(value)))
	if eval_ctx.autoescape:
		result = Markup(result)
	return result

@app.template_filter()
@evalcontextfilter
def pointer(eval_ctx, value):
	result = '\n\n'.join(f"<a href='#{p.strip('>>')}'>{p}</a>" for p in pointer_re.split(escape(value)))
	print(result)
	if eval_ctx.autoescape:
		result = Markup(result)
	return result

def allowed_file(filename):
	return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def get_ext(filename):
	return filename.rsplit('.', 1)[1].lower()
