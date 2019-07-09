from tkinter import *
import sqlite3
import hashlib

root = Tk()

root.title("Login")

width = 400
height = 300

screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

x = (screen_width/2) - (width/2)
y = (screen_height/2) - (height/2)

root.geometry("%dx%d+%d+%d" % (width, height, x, y))
root.resizable(0, 0)

USERNAME = StringVar()
PASSWORD = StringVar()
USERNAME1 = StringVar()
PASSWORD1 = StringVar()
pws = StringVar()
pws1 = StringVar()

Top = Frame(root, bd=2,  relief=RIDGE)
Top.pack(side=TOP, fill=X)
Form = Frame(root, height=200)
Form.pack(side=TOP, pady=20)

lb_title = Label(Top, text = "Enter account Data", font = ('arial', 15))
lb_title.pack(fill=X)
lb_username = Label(Form, text='Username: ', font=('arial', 14), bd=15)
lb_username.grid(row=0, sticky="e")
lb_password = Label(Form, text='Password: ', font=('arial', 14), bd=15)
lb_password.grid(row=1, sticky="e")
lb_text = Label(Form)
lb_text.grid(row=2, columnspan=2)

username = Entry(Form, textvariable=USERNAME, font=(14))
username.grid(row=0, column=1)
password = Entry(Form, textvariable=PASSWORD, font=(14))
password.grid(row=1, column=1)

def Login(event=None):
	Database()
	if USERNAME.get() == "" or PASSWORD.get() == "":
		lb_text.config(text="Please try again", fg="red")
	else:
		pw = hashlib.sha256(bytes(PASSWORD.get(),"utf-8"))
		cursor.execute("SELECT * FROM `member` WHERE `username` = ? AND `password` = ? ", (USERNAME.get(), pw.hexdigest()))
		if cursor.fetchone() is not None:
			HomeWindow()
			USERNAME.set("")
			PASSWORD.set("")
			lb_text.config(text="")
		else:
			lb_text.config(text="Invalid Password or Username", fg="red")
			USERNAME.set("")
			PASSWORD.set("")
	cursor.close()
	con.close()

bt_login = Button(Form, text="Login", width=45, command=Login)
bt_login.grid(pady=25, row=3, columnspan=2)
bt_login.bind('<Return>', Login)

def Database():
	global con,cursor
	pwa = hashlib.sha256(b"admin")
	pws = pwa.hexdigest()
	con = sqlite3.connect("accdata.db")
	cursor = con.cursor()
	cursor.execute("CREATE TABLE IF NOT EXISTS `member` (mem_id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT, username TEXT, password TEXT)")
	cursor.execute("SELECT * FROM `member` WHERE `username` = 'admin' AND `password` = 'a8c6976e5b5410415bde908bd4dee15dfb167a9c873fc4bb8a81f6f2ab448a918' ")
	if cursor.fetchone() is None:
		cursor.execute("INSERT INTO `member`(username, password) VALUES('admin', '8c6976e5b5410415bde908bd4dee15dfb167a9c873fc4bb8a81f6f2ab448a918') ")
		con.commit()
		


def Back():
	Home.destroy()
	root.deiconify()

def HomeWindow():
	global Home
	root.withdraw()
	Home = Toplevel()
	Home.title("test Application")
	width = 500
	height = 500
	screen_width = root.winfo_screenwidth()
	screen_height = root.winfo_screenheight()
	x = (screen_width/2) - (width/2)
	y = (screen_height/2) - (height/2)
	root.resizable(0, 0)
	Top1 = Frame(Home, bd=2,  relief=RIDGE)
	Top1.pack(side=TOP, fill=X)
	Form1 = Frame(Home, height=200)
	Form1.pack(side=TOP, pady=20)
	Home.geometry("%dx%d+%d+%d" % (width, height, x, y))
	lb_home = Label(Top1, text="Successfully Login!", font=('times new roman', 20)).pack()
	
	lb_username1 = Label(Form1, text='Username: ', font=('arial', 14), bd=15)
	lb_username1.grid(row=1, sticky="e")
	lb_password1 = Label(Form1, text='Password: ', font=('arial', 14), bd=15)
	lb_password1.grid(row=2, sticky="e")
	lb_text1 = Label(Form1)
	lb_text1.grid(row=5, columnspan=2)

	username1 = Entry(Form1, textvariable=USERNAME1, font=(14))
	username1.grid(row=1, column=1)
	password1 = Entry(Form1, textvariable=PASSWORD1, font=(14))
	password1.grid(row=2, column=1)
	
	def Create():
		Database()

		if USERNAME1.get() == "" or PASSWORD1.get() == "":
			lb_text1.config(text="can't be empty", fg="red")
		else:
			pwc = hashlib.sha256(bytes(PASSWORD1.get(),"utf-8"))	
			cursor.execute("SELECT * FROM `member` WHERE `username` = ? OR `password` = ?", (USERNAME1.get(),pwc.hexdigest()))
			if cursor.fetchone() is None:
				cursor.execute("INSERT INTO `member`(username, password) VALUES(?, ?) ", (USERNAME1.get(), pwc.hexdigest()))
				con.commit()
				USERNAME1.set("")
				PASSWORD1.set("")
				lb_text1.config(text="User added", fg="green")
			else:
				lb_text1.config(text="User already exists", fg="red")
				USERNAME1.set("")
				PASSWORD1.set("")	

	bt_create = Button(Form1, text="Create User", width=45, command=Create)
	bt_create.grid(pady=25, row=3, columnspan=2)
	bt_back = Button(Form1, text="Back", command=Back)
	bt_back.grid(pady=25, row=4,columnspan=1)

	




if __name__ == '__main__':
    root.mainloop()

