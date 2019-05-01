from models import *
from datetime import date



def add_category(category_name):
	Category.create(category_name=category_name)


def add_expense(amount,category_id):
	current_date = date.today()
	Expenses.create(date=current_date, amount=amount,category_id=category_id, description="My description")


def categorize_by_month(x):
	expenses = []
	all_expenses = Expenses.select().where(Expenses.date==x)
	
	for expense in all_expenses:
		expenses.append([expense.date,expense.amount])
	
	return expenses
	

def categorize_by_category(y):
	# print(y)
	
	category=Category.select().where(Category.category_name==y)
	x = 0
	for i in category:
		x = i.id

	print(x)
	expenses=[]
	all_expenses=Expenses.select().where(Expenses.category_id==1)
	print(all_expenses)

	for expense in all_expenses:
		print(expense.amount, expense.category_id)
		expenses.append([expense.amount,expense.category_id])

	print(expenses)
	return expenses


def categorize_by_amount(amount,category):

	if category=='lesser':
		amounts=[]

		all_amount=Expenses.select().where(Expenses.amount<amount)
		print(all_amount)

		for amount in all_amount:
			print(amount.category_id,amount.date,amount.description)
			amounts.append([amount.category_id,amount.date,amount.description])

	if category=='equal':
		amounts=[]

		all_amount=Expenses.select().where(Expenses.amount==amount)
		print(all_amount)

		for amount in all_amount:
			print(amount.category_id,amount.date,amount.description)
			amounts.append([amount.category_id,amount.date,amount.description])

	return amounts

def see_all():
	pass

					
if __name__=="__main__":
	# add_expense(amount=20, category_id=1)
	check()




