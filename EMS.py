#importing all the Libraries
from tkinter import *
from tkinter.messagebox import *
from tkinter.scrolledtext import *
import pandas as pd
import matplotlib.pyplot as plt
from sqlite3 import *
import csv
import os

#creating functions 

def f1():
	main_window.withdraw()
	add_window.deiconify()	

def f2():
	add_window.withdraw()
	main_window.deiconify()

def f3():
	main_window.withdraw()
	view_window.deiconify()
	vw_st_data.delete(1.0,END)
	info=""
	con=None
	try:
		con=connect("ems.db")
		cursor=con.cursor()
		sql="select * from employee"
		cursor.execute(sql)
		data=cursor.fetchall()
		con.commit()
		for d in data:
			info= info + "Id= " + str(d[0]) + "\t"+ " Name= " +str(d[1]) + "\t\t"+ " Salary=Rs" + str(d[2]) +  "\n"
		vw_st_data.insert(INSERT,info)
	except Exception as e:
		showerror("Issue",e)
	finally:
		if con is None:
			con.close()
	

def f4():
	view_window.withdraw()
	main_window.deiconify()
	

def f5():
	main_window.withdraw()
	update_window.deiconify()

def f6():
	update_window.withdraw()
	main_window.deiconify()

def f7():
	main_window.withdraw()
	delete_window.deiconify()

def f8():
	delete_window.withdraw()
	main_window.deiconify()

def chart():

	data=pd.read_csv("empdata.csv")		#reading data from csv file
	d1=data.sort_values(by=["salary"],ascending=False)		#sorting the salary in descending order
	d2=d1.head(5)		#displaying only top 5 data
	name=d2["name"].tolist()
	salary=d2["salary"].tolist()
	
	#ploting bar chart using matplotlib.pyplot
	plt.bar(name,salary,width=0.5,color=["red","cyan","purple","gold","silver"])
	plt.xlabel("Names of the Employee")
	plt.ylabel("Salary in Rupees")
	plt.title(" Top 5 Employee by Salary ")
	plt.grid()
	plt.show()

#################################creating main window################
main_window=Tk()
main_window.title(" E.M.S ")
main_window.geometry("500x550+400+100")
main_window.iconbitmap("py.ico")
main_window.configure(bg="PaleGreen1")

#initializing font
f=("Ink Free",12,"bold")

#initializing y axis
y=15

#initializing Buttons

#BTN add
add_btn=Button(main_window,activeforeground="orange",activebackground="pink",text="ADD",font=f,width=9,height=2,command=f1)
add_btn.pack(pady=y)

#btn view
view_btn=Button(main_window,text="VIEW",activeforeground="yellow",activebackground="purple",font=f,width=9,height=2,command=f3)
view_btn.pack(pady=y)

#btn update
update_btn=Button(main_window,activeforeground="cyan",text="UPDATE",height=2,font=f,width=9,command=f5)
update_btn.pack(pady=y)

#btn delete
delete_btn=Button(main_window,activeforeground="yellow",activebackground="silver",text="DELETE",font=f,width=9,height=2,command=f7)
delete_btn.pack(pady=y)

#btn charts
charts_btn=Button(main_window,activeforeground="yellow",activebackground="cyan",text="CHARTS",font=f,width=9,height=2,command=chart)
charts_btn.pack(pady=y)

#Label Quote
fq=("Lucida Calligraphy",12)
quote_lab=Label(main_window,fg="blue",bg="yellow",text="Quote Of The Day:\n When it comes to luck, Make your own\n  -Bruce Springsteen",font=fq,width=48,height=3,)
quote_lab.pack(pady=5)


#####################Add window initialization##########################

add_window=Toplevel(main_window)
add_window.title("ADD EMPLOYEE")
add_window.geometry("500x550+400+100")
add_window.iconbitmap("py.ico")
add_window.configure(bg="LightSkyBlue1")

#Label name
aw_lab_id=Label(add_window,text="Enter ID",font=f,height=2,width=9)
aw_lab_id.pack(pady=y)

#Entry id
aw_ent_id=Entry(add_window,font=f,)
aw_ent_id.pack(pady=y)

#Label Name
aw_lab_name=Label(add_window,text="Enter Name",font=f,height=2)
aw_lab_name.pack(pady=y)

#Entry name
aw_ent_name=Entry(add_window,font=f,)
aw_ent_name.pack(pady=y)

#Label Salary
aw_lab_salary=Label(add_window,text="Enter Salary",font=f,height=2)
aw_lab_salary.pack(pady=y)

#Entry salary
aw_ent_salary=Entry(add_window,font=f,)
aw_ent_salary.pack(pady=y)

def save():
	con=None
	try:
	
		id=aw_ent_id.get()
		if len(id) == 0:
			raise Exception("Id should not be Empty")
		elif  id.isnumeric()==0:
			aw_ent_id.delete(0,END)
			raise Exception("ID Should  Be In In Positive Numbers ")
			
		elif int(id) == 0:
			aw_ent_id.delete(0,END)
			raise Exception("ID Should  Be In In Positive Numbers")
			
		else:
			id1=int(id)
		name=aw_ent_name.get()
		if len(name)==0:
			raise Exception("Name Should not be empty")
		elif name.isalpha()==0:
			aw_ent_name.delete(0,END)
			raise Exception("Only alphabets are allowed in Name")
			
		elif len(name) < 2:
			aw_ent_name.delete(0,END)
			raise Exception("Name too short")
		else:
			name1=name
		salary=(aw_ent_salary.get()) 
		if len(salary)==0:
			aw_ent_salary.delete(0,END)
			raise Exception("Salary Should not be Empty")
		
		elif  salary.isnumeric()==0:
			aw_ent_salary.delete(0,END)
			raise Exception("Salary should be in Positive Numbers")
			
		elif float(salary) < 8000:
			aw_ent_salary.delete(0,END)
			raise Exception("Salary should be greater than RS8000")
			
		else:
			salary1=float(salary)
		con=connect ("ems.db")
		cursor=con.cursor()
		sql="insert into employee values('%d','%s','%f')"
		cursor.execute(sql % (id1,name1,salary1))
		con.commit()
		showinfo("Record","Employee added Successfully")
		
		#Exporting data into csv file
		cursor=con.cursor()
		cursor.execute("select * from employee")
		with open("empdata.csv","w",newline='',encoding='utf-8') as csv_file:					
			csv_writer=csv.writer(csv_file)
			csv_writer.writerow([i[0] for i in cursor.description])
			csv_writer.writerows(cursor)
		
		
	
	except IntegrityError:
		showerror("Record","Employee Id Already present,Try Another One")
	except Exception as e:
		showerror("Issue",e)
	
	finally:
		if con is not None:
			con.close()
			aw_ent_id.delete(0,END)
			aw_ent_name.delete(0,END)
			aw_ent_salary.delete(0,END)



#Button save
aw_btn_save=Button(add_window,text="Save",font=f,height=2,width=6,activeforeground="yellow",activebackground="cyan",command=save)
aw_btn_save.pack()

#Button back
aw_btn_back=Button(add_window,activeforeground="yellow",activebackground="cyan",text="Back",font=f,height=2,width=6,command=f2)
aw_btn_back.pack(pady=y)

#to close add window
add_window.withdraw()

###########################View Emp##############################

view_window=Toplevel(main_window)
view_window.title("View Emp")
view_window.geometry("500x550+400+100")
view_window.iconbitmap("py.ico")
view_window.configure(bg="LightGoldenrod1")

	


#scroll text
vw_st_data=ScrolledText(view_window,width=44,height=19,font=f)
vw_st_data.pack(pady=y)

#btn back
vw_btn_back=Button(view_window,activeforeground="yellow",activebackground="red",text="Back",font=f,width=8,height=2,command=f4)
vw_btn_back.pack(pady=y)


#to close
view_window.withdraw()

###########################Update Window#######################
update_window=Toplevel(main_window)
update_window.title("View Emp")
update_window.geometry("500x550+400+100")
update_window.iconbitmap("py.ico")
update_window.configure(bg="LightPink1")

#Label name
uw_lab_id=Label(update_window,text="Enter ID",font=f,height=2,width=9)
uw_lab_id.pack(pady=y)

#Entry id
uw_ent_id=Entry(update_window,font=f,)
uw_ent_id.pack(pady=y)

#Label Name
uw_lab_name=Label(update_window,text="Enter Name",font=f,height=2)
uw_lab_name.pack(pady=y)

#Entry name
uw_ent_name=Entry(update_window,font=f,)
uw_ent_name.pack(pady=y)

#Label Salary
uw_lab_salary=Label(update_window,text="Enter Salary",font=f,height=2)
uw_lab_salary.pack(pady=y)

#Entry salary
uw_ent_salary=Entry(update_window,font=f,)
uw_ent_salary.pack(pady=y)

def update():
	con=None
	try:
		con=connect("ems.db")
		cursor=con.cursor()
		sql="update employee set name='%s',salary='%f' where id='%d' "
		id=(uw_ent_id.get())
		if len(id) == 0:
			raise Exception("Id should not be Empty")
			uw_ent_id.delete(0,END)
		elif  id.isnumeric()==0:
			raise Exception("ID Should  Be  In Positive Numbers")
			uw_ent_id.delete(0,END)
		elif int(id) == 0:
			raise Exception("ID Should  Be In Positive Numbers")
			uw_ent_id.delete(0,END)
		else:
			id1=int(id)
		name=uw_ent_name.get()
		if len(name)==0:
			raise Exception("Name Should not be empty")
			uw_ent_name.delete(0,END)
		elif name.isalpha()==0:
			raise Exception("Only alphabets are allowed in Name")
			uw_ent_name.delete(0,END)
		elif len(name) < 2:
			raise Exception("Name too short")
			uw_ent_name.delete(0,END)
		else:
			name1=name
		salary=(uw_ent_salary.get())
		if len(salary)==0:
			raise Exception("Salary Should not be Empty")
			uw_ent_salary.delete(0,END)
		elif  salary.isnumeric()==0:
			raise Exception("Salary should be in Numbers")
			uw_ent_salary.delete(0,END)
		elif float(salary) < 8000:
			raise Exception("Salary should be greater than RS8000")
			uw_ent_salary.delete(0,END)
		else:
			salary1=float(salary)
		cursor.execute(sql % (name1,salary1,id1))
		if cursor.rowcount == 1:
			con.commit()
			showinfo("Record","Record Updated Successfully")
		else:
			showerror("Record","Record does not exists")
	
		#Exporting data into csv file
		cursor=con.cursor()
		cursor.execute("select * from employee")
		with open("empdata.csv","w",newline='',encoding='utf-8') as csv_file:					
			csv_writer=csv.writer(csv_file)
			csv_writer.writerow([i[0] for i in cursor.description])
			csv_writer.writerows(cursor)
		dirpath=os.getcwd()+"/empdata.csv"
	except Exception as e:
		showerror("Issue",e)
		con.rollback()
	finally:
		if con is not None:
			con.close()
			uw_ent_id.delete(0,END)
			uw_ent_name.delete(0,END)
			uw_ent_salary.delete(0,END)


#Button save
uw_btn_save=Button(update_window,activeforeground="yellow",activebackground="green",text="Save",font=f,height=2,width=6,command=update)
uw_btn_save.pack()

#Button back
uw_btn_back=Button(update_window,activeforeground="gold",activebackground="red",text="Back",font=f,height=2,width=6,command=f6)
uw_btn_back.pack(pady=y)

#to close add window
update_window.withdraw()

###########################delete window#################

delete_window=Toplevel(main_window)
delete_window.title("Delete Emp")
delete_window.geometry("500x550+400+100")
delete_window.iconbitmap("py.ico")
delete_window.configure(bg="AntiqueWhite2")

#Label name
dw_lab_id=Label(delete_window,text="Enter ID",font=f,height=2,width=9)
dw_lab_id.pack(pady=y)

#Entry id
dw_ent_id=Entry(delete_window,font=f,)
dw_ent_id.pack(pady=y) 

def delete():
	con=None
	try:
		con=connect("ems.db")
		cursor=con.cursor()
		sql="delete from employee where id='%d' "
		id=(dw_ent_id.get() )
		if len(id) == 0:
			raise Exception("Id should not be Empty")
			dw_ent_id.delete(0,END)
		elif  id.isnumeric()==0:
			raise Exception("ID Should  Be In  Numbers only")
			dw_ent_id.delete(0,END)
		elif int(id) == 0:
			raise Exception("Id should be Number")
			dw_ent_id.delete(0,END)
		else:
			id1=int(id)
		cursor.execute(sql % (id1))
		if cursor.rowcount == 1:
			con.commit()
			showinfo("Record","Employee Deleted Successfully")
		else:
			showwarning("Record","Employee-ID does not Exists")
		#Exporting data into csv file
		cursor=con.cursor()
		cursor.execute("select * from employee")
		with open("empdata.csv","w",newline='',encoding='utf-8') as csv_file:					
			csv_writer=csv.writer(csv_file)
			csv_writer.writerow([i[0] for i in cursor.description])
			csv_writer.writerows(cursor)
		dirpath=os.getcwd()+"/empdata.csv"
	except Exception as e:
		showerror("Issue",e)
		con.rollback()
	finally:
		if con is not None:
			con.close()
			dw_ent_id.delete(0,END)




#Button save
dw_btn_save=Button(delete_window,activeforeground="red",activebackground="cyan",text="Delete",font=f,height=2,width=6,command=delete)
dw_btn_save.pack()

#Button back
dw_btn_back = Button(delete_window,activeforeground="red",activebackground="cyan",text="Back",font=f,height=2,width=6,command=f8)
dw_btn_back.pack(pady=y)

#to close window
delete_window.withdraw()



main_window.mainloop()
