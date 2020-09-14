from settings import *
from models import *

@app.route('/')
def home():
	return render_template('index.html', boards=Board.select())

@app.route('/<tag>')
def board(tag):
	try:
		board = Board.get(Board.tag == tag)
		#threads = Thread.select().where(Thread.board.tag == board.tag)
		return render_template('board.html', board=board, threads=board.threads, len=len)
	except Exception as e:
		print(e)
		flash('Board not found')
		return redirect('/')

@app.route('/<tag>/<int:thread_id>')
def thread(tag, thread_id):
	try:
		thread = Thread.get_by_id(thread_id)
		#replies = Reply.select().where(Reply.thread == thread)
		replies = thread.replies
		return render_template(
			'thread.html', 
			tag=tag, 
			thread_id=thread_id, 
			title=thread.title, 
			body=thread.body, 
			time=thread.time, 
			replies=replies, 
			replies_count=len(replies)
		)
	except Exception as e:
		print(e)
		flash('Thread not found')
		return redirect('/')

@app.route('/<tag>/post', methods=['POST'])
def post(tag):
	title = request.form['title']
	body = request.form['body']

	if 'files[]' in request.files:
		for file in request.files.getlist('files[]'):
			if file and allowed_file(file.filename):
				filename = os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(file.filename))
				file.save(filename)

	try:
		board = Board.get(Board.tag == tag)
		thread = Thread.create(
			board=board, 
			title=title, 
			body=body, 
			time=str(datetime.utcnow())[:19]
		)
		return redirect(f'/{tag}/{thread.id}')
	except Exception as e:
		print(e)
		flash('Thread failed!')
		return redirect('/')

@app.route('/<tag>/<int:thread_id>/reply', methods=['POST'])
def reply(tag, thread_id):
	body = request.form['body']
	files = request.files['files']

	try:
		thread = Thread.get_by_id(thread_id)
		reply = Reply.create(
			thread=thread, 
			body=body, 
			time=str(datetime.utcnow())[:19]
		)
		return redirect(f'/{tag}/{thread.id}')
	except Exception as e:
		print(e)
		flash('Reply failed!')
		return redirect('/')

@app.errorhandler(404)
def not_found(e):
	return render_template('404.html'), 404


if __name__ == '__main__':
	app.run(host='0.0.0.0', debug=True)