from tkinter import *
from tkinter.ttk import *
from tkinter import messagebox
from views import *
from PIL import Image, ImageTk
import matplotlib.pyplot as plt
from models import *

LARGE_FONT = ("Verdana", 36)
BUTTON_FONT = ("Verdana", 14)


class ExpenseTracker(Tk):
	
	def __init__(self, *args, **kwargs):
		Tk.__init__(self, *args, **kwargs)
		Tk.configure(self)

		self.container = Frame(self)
		self.container.grid()
		self.container.grid_rowconfigure(0,weight=1)
		self.container.grid_columnconfigure(0,weight=1)

		self.geometry("750x480")
		self.show_frame(Main)

	
	def show_frame(self, cont):
		frame = cont(parent=self.container, controller=self)
		frame.grid(row=0,column=0,sticky="nsew")
		frame.tkraise()


class Main(Frame):

	def __init__(self, parent, controller):
		Frame.__init__(self, parent)
		self.controller = controller

		heading_label = Label(self, text='WiseX', font=LARGE_FONT)
		add_expense_button = Button(self, text="Add Expense", command=lambda:controller.show_frame(AddExpense))
		add_category_button = Button(self, text="Add Category", command=lambda:controller.show_frame(AddCategory))
		see_all_button = Button(self, text="See All", command=lambda:controller.show_frame(SeeAll))
		by_month_button = Button(self, text="Categorize by Date", command=lambda:controller.show_frame(CategorizeByMonth))
		by_category_button = Button(self, text="Categorize by Category", command=lambda:controller.show_frame(CategorizeByCategory))
		by_amount_button = Button(self, text="Categorize by Amount", command=lambda:controller.show_frame(CategorizeByAmount))

		heading_label.grid(row=1, column=1, padx=320, pady=10)
		add_expense_button.grid(row=2, column=1, padx=320, pady=10)
		add_category_button.grid(row=3, column=1, padx=320, pady=10)
		see_all_button.grid(row=4, column=1, padx=320, pady=10)
		by_month_button.grid(row=5, column=1, padx=320, pady=10)
		by_category_button.grid(row=6, column=1, padx=320, pady=10)
		by_amount_button.grid(row=7, column=1, padx=320, pady=10)



class AddExpense(Frame):
	def __init__(self, parent, controller):
		Frame.__init__(self, parent)
		self.controller = controller

		self.heading=Label(self,text="ADD EXPENSE",font=20)
		self.heading.grid(row=3,column=2,padx=10,pady=5)


		self.tkvar = StringVar(self)

		categories = Category.select()	
		choices = [category.category_name for category in categories]
		self.tkvar.set(categories[0].category_name)
		popupMenu = OptionMenu(self, self.tkvar, *choices)
		addcategory_label=Label(self, text="Categoy name",font=11)
		addexpense_label=Label(self, text="Amount",font=11)
		self.amount=Entry(self)
		add_expense_btn = Button(self,text="Add Amount", command=self.addexpense)
		back_btn = Button(self,text="Back")
		back_btn = Button(self,text="Back",command=lambda:controller.show_frame(Main))

		popupMenu.grid(row=5, column=2)
		addcategory_label.grid(row=5, column=1, padx=10, pady=10)
		addexpense_label.grid(row=6, column=1, padx=10, pady=10)
		self.amount.grid(row=6, column=2, padx=10, pady=10)
		add_expense_btn.grid(row=8, column=2, padx=60, pady=15)
		back_btn.grid(row=8, column=1, padx=20, pady=20)


	def addexpense(self):
		amt=self.amount.get()
		category=self.tkvar.get()
		cat_id = Category.select().where(Category.category_name==category)[0].id
		add_expense(category_id=cat_id,amount=amt)


class AddCategory(Frame):
	
	def __init__(self, parent, controller):
		Frame.__init__(self, parent)
		self.controller = controller

		self.heading=Label(self,text="ADD CATEGORY",font=20)
		self.heading.grid(row=3, column=2, padx=15,pady=15)	

		addcategory_label=Label(self, text="List of exisisting category",font=11)

		self.tkvar = StringVar(self)

		categories = Category.select()	
		choices = [category.category_name for category in categories]

		popupMenu = OptionMenu(self, self.tkvar, *choices)
		popupMenu.grid(row=6, column=2)

		addcategory_label.grid(row=6, column=1, padx=10, pady=10)

		addnew_label=Label(self, text="Add New Category",font=11)
		self.category=Entry(self)

		addnew_label.grid(row=7, column=1, padx=10, pady=10)
		self.category.grid(row=7, column=2, padx=10, pady=10)

		add_category_btn = Button(self,text="Add Category")
		back_btn = Button(self,text="Back")

		add_category_btn = Button(self,text="Add Category",command=self.add_category_value)
		back_btn = Button(self,text="Back",command=lambda:controller.show_frame(Main))

		add_category_btn.grid(row=8, column=2, padx=60, pady=15)
		back_btn.grid(row=8, column=1, padx=20, pady=20)

	def add_category_value(self):
		category=self.category.get()
		add_category(category_name=category)


class SeeAll(Frame):
	def __init__(self, parent, controller):
		Frame.__init__(self, parent)
		self.controller = controller
		
		categories = Category.select()
		labels = []
		totals = []

		for category in categories:
			print(category.id)

			expenses = Expenses.select().where(Expenses.category_id==category)
			total = 0
			for expense in expenses:
				total += expense.amount

			totals.append(total)
			labels.append(category.category_name)

		for i in range(len(totals)):
			totals[i] /= sum(totals)
			totals[i] *= 100

		plt.pie(totals, labels=labels)
		plt.savefig("mychart.jpg")

		image = Image.open("mychart.jpg")
		chart = ImageTk.PhotoImage(image)
		
		back_btn = Button(self,text="Back",command=lambda:controller.show_frame(Main))
		back_btn.pack()

		label = Label(self, image=chart)
		label.image = chart 
		label.pack()


class CategorizeByMonth(Frame):
	
	def __init__(self, parent, controller):
		Frame.__init__(self, parent)
		self.controller = controller

		addmonth_label=Label(self, text="Choose Date",font=11)
		self.choose_month=Text(self, height=1, width=30)

		ok_btn=Button(self, text="OK",command=self.get_month)
		ok_btn.grid(row=3, column=3, padx=5, pady=5)

		addmonth_label.grid(row=3, column=1, padx=10, pady=10)
		self.choose_month.grid(row=3, column=2, padx=10, pady=10)

		add_month_btn = Button(self,text="OK")

		add_month_btn.grid(row=5, column=2, padx=60, pady=15)
		back_btn = Button(self,text="Back",command=lambda:controller.show_frame(Main))
		back_btn.grid(row=5, column=3, padx=20, pady=20)

		self.tree=Treeview(self,columns=('#1','#2'))
		self.tree.heading( '#1',text='Date')
		self.tree.heading('#2',text='expense')

		self.tree.column('#1',stretch=YES,anchor=CENTER)
		self.tree.column('#2',stretch=YES,anchor=CENTER)

		self.tree.grid(row=5,column=2,padx=10,pady=10,sticky='nsew')
		self.tree['show']='headings'

	def get_month(self):

		month = self.choose_month.get('1.0','end-1c')
		print(month)
		exp = categorize_by_month(month)
		
		for i in exp:
			
			self.tree.insert('','end',values=(i[0],i[1]))


class CategorizeByCategory(Frame):
	def __init__(self, parent, controller):
		Frame.__init__(self, parent)
		self.controller = controller

		addcategory_label=Label(self, text="Choose Category",font=11)
		self.ChooseCategory=Text(self, height=1, width=30)

		addcategory_label.grid(row=3, column=1, padx=10, pady=10)
		self.ChooseCategory.grid(row=3, column=2, padx=10, pady=10)

		add_category_btn = Button(self,text="OK",command=self.get_category)
		back_btn = Button(self,text="Back",command=lambda:controller.show_frame(Main))

		add_category_btn.grid(row=8, column=2, padx=60, pady=15)
		back_btn.grid(row=8, column=1, padx=20, pady=20)


		self.tree=Treeview(self,columns=('#1','#2'))
		self.tree.heading( '#1',text='Category')
		self.tree.heading('#2',text='expense')

		self.tree.column('#1',stretch=YES,anchor=CENTER)
		self.tree.column('#2',stretch=YES,anchor=CENTER)

		self.tree.grid(row=5,column=2,padx=10,pady=10,sticky='nsew')
		self.tree['show']='headings'

	def get_category(self):
		cat=self.ChooseCategory.get('1.0','end-1c')
		category_exp=categorize_by_category(cat)	

		for i in category_exp:
			
			self.tree.insert('','end',values=(i[0],i[1]))
		

class CategorizeByAmount(Frame):
	
	def __init__(self, parent, controller):
		Frame.__init__(self, parent)
		self.controller = controller

		addamount_label=Label(self, text="Choose Amount",font=11)
		self.ChooseAmount=Text(self, height=1, width=30)


		addamount_label.grid(row=6, column=1, padx=10, pady=10)
		self.ChooseAmount.grid(row=6, column=2, padx=10, pady=10)

		add_amount_btn = Button(self,text="OK",command=self.get_amount)
		back_btn = Button(self,text="Back",command=lambda:controller.show_frame(Main))

		add_amount_btn.grid(row=8, column=2, padx=60, pady=15)
		back_btn.grid(row=8, column=1, padx=20, pady=20)

		option=[0,'lesser','equal']

		options = list(set(option))		#to obtain only unique events 
		self.variable = StringVar(self)
		self.variable.set(0)		#Setting the default event
		self.select = OptionMenu(self, self.variable,*options,command=self.get_value).grid(row =6,column =3,padx=10,pady=10)

		self.tree=Treeview(self,columns=('#1','#2','#3'))
		self.tree.heading( '#1',text='Category ID')
		self.tree.heading('#2',text='DATE')
		self.tree.heading('#3',text='DESCRIPTION')

		self.tree.column('#1',stretch=YES,anchor=CENTER)
		self.tree.column('#2',stretch=YES,anchor=CENTER)
		self.tree.column('#3',stretch=YES,anchor=CENTER)

		self.tree.grid(row=5,column=2,padx=10,pady=10,sticky='nsew')
		self.tree['show']='headings'		
	
	def get_value(self,value):

		self.id=value
		print(self.id)


	def get_amount(self):

		self.amount=self.ChooseAmount.get('1.0','end-1c')
		self.ChooseAmount.delete('1.0','end-1c')

		categorize_amount=categorize_by_amount(self.amount,self.id)
		

		for i in categorize_amount:
			self.tree.insert('','end',values=(i[0],i[1],i[2]))


app = ExpenseTracker()
app.mainloop()