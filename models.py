from peewee import *

db = SqliteDatabase('data.db', pragmas={
	'journal_mode': 'wal',
	'cache_size': -1024 * 32,
	'foreign_keys': 1,
	'ignore_check_constraints': 0
})
db.connect()

class BaseModel(Model):
	class Meta:
		database = db


class Board(BaseModel):
	tag = CharField(unique=True)
	name = CharField(unique=True)
	description = TextField()

class Thread(BaseModel):
	board = ForeignKeyField(Board, backref='threads')
	title = CharField()
	body = TextField()
	time = CharField()

class Reply(BaseModel):
	thread = ForeignKeyField(Thread, backref='replies')
	body = TextField()
	time = CharField()

class File(BaseModel):
	thread = ForeignKeyField(Thread, backref='files')
	reply = ForeignKeyField(Reply, backref='files', null=True)
	extension = CharField()
	uuid = TextField(unique=True)


try:
	db.create_tables([Board, Thread, Reply, File])
	Board.create(tag='g', name='Technology', description='A board for tech bois')
	Board.create(tag='x', name='Paranormal', description='A board for ghosts')
except Exception as e:
	print('Error: ', e)
	db.close()