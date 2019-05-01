import peewee as pw

db = pw.SqliteDatabase('Expense_tracker_app.db')


class Category(pw.Model):
	category_name = pw.TextField()

	class Meta:
		database = db



class Expenses(pw.Model):
	date=pw.DateField()
	amount=pw.IntegerField()
	category_id=pw.ForeignKeyField(Category)
	description=pw.TextField()


	class Meta:
		database = db


db.connect()
db.create_tables([Category,Expenses])
		


