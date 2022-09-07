from tkinter import *
from PIL import ImageTk,Image
from tkinter import messagebox
import mysql.connector
import ctypes as ct
import csv
from tkinter import ttk
import os
from tkinter import filedialog
import webbrowser as wb
from PIL import ImageTk,Image
import pandas as pd
import pathlib
import sqlite3


mydb = sqlite3.connect('customer.db')
#Create a cursor
my_cursor = mydb.cursor()
#Create a Table
my_cursor.execute("""CREATE TABLE IF NOT EXISTS customers(
    tour_id int,
    driver_name text,
    driver_last_name text,
    truck_ID int,
    tour_price real,
    mileage real,
    confirmation real,
    delivery_order real,
    inc_num INTEGER PRIMARY KEY AUTOINCREMENT 
    )""")


mainPage=Tk()
mainPage.title("Lava Freight Data Centar")
#mainPage.iconbitmap('C:/Users/VladimirP1984/Documents/SQLITE/Projects/python/truck_b.ico')
mainPage.state("zoomed")



def dark_title_bar(window):
    """
    MORE INFO:
    https://docs.microsoft.com/en-us/windows/win32/api/dwmapi/ne-dwmapi-dwmwindowattribute
    """
    window.update()
    DWMWA_USE_IMMERSIVE_DARK_MODE = 20
    set_window_attribute = ct.windll.dwmapi.DwmSetWindowAttribute
    get_parent = ct.windll.user32.GetParent
    hwnd = get_parent(window.winfo_id())
    rendering_policy = DWMWA_USE_IMMERSIVE_DARK_MODE
    value = 2
    value = ct.c_int(value)
    set_window_attribute(hwnd, rendering_policy, ct.byref(value),
                         ct.sizeof(value))

def insert_values():
    #Insert values in database
    TOID=tourID_entry.get()
    name=dname_entry.get().replace(" ","")
    last_name=dlname_entry.get().replace(" ","")
    TID=truckID_entry.get()
    TOP=tourP_entry.get()
    MIL=mil_entry.get()
    z="SELECT * FROM customers"
    my_cursor.execute(z)
    items=my_cursor.fetchall()
    if TID=='':
        TID=None
    if TOP=='':
        TOP=None
    if MIL=='':
        MIL=None
    approval=0
    for item in items:
        if item[0]==int(TOID):
            messagebox.showwarning('Warning','Tour ID'+' '+ TOID +' '+'already exists in the database')
            approval=1

    if approval==0:
        if TOID!="" and name !="" and last_name!="":
            responseC=messagebox.askyesno('','Do you want to upload tour confirmation document')
            if responseC==1:
                confirmation=upload_doc()
                if confirmation=="":
                    confirmation='No tour confirmation document'
            else:
                confirmation='No tour confirmation document'
            responseD=messagebox.askyesno('','Do you want to upload delivery order document')
            if responseD==1:
                delivery=[""]
                for s in range(4):
                    delivery[s]=upload_doc()
                    if delivery[s]!="" and s<3:
                        responseN=messagebox.askyesno('','Do you want to upload one more delivery order document')
                        if responseN==1:
                            delivery.append("")
                        else:
                            break
                    else:
                        break

            
                if delivery==[""]:
                    delivery='No delivery order document'
            else:
                delivery='No delivery order document'
            if delivery=='No delivery order document':
                x=str(delivery)
            else:
                if delivery[len(delivery)-1]=="":
                    delivery.pop()
                x=",".join(delivery)
                #n=(x[1:-1])
                #print(n)
            
            sql_command="INSERT INTO customers (tour_id,driver_name,driver_last_name,truck_id,tour_price,mileage,confirmation,delivery_order) VALUES ('{}','{}','{}','{}','{}','{}','{}','{}')".format(TOID,name,last_name,TID,TOP,MIL,confirmation,x)
            #values=(TOID,name,last_name,TID,TOP,MIL,confirmation,x)
            my_cursor.execute(sql_command)
            tourID_entry.delete(0,END)
            dname_entry.delete(0,END)
            dlname_entry.delete(0,END)
            truckID_entry.delete(0,END)
            tourP_entry.delete(0,END)
            mil_entry.delete(0,END)
            
            
            mydb.commit()
        else:
            messagebox.showwarning('Warning','Tour ID,Driver Name and Driver Last name are mandatory field')



def upload_doc():
 
    file_path_string = filedialog.askopenfilename()
    return file_path_string

def delete_record():

    selected=my_tree.focus()
    values = my_tree.item(selected, 'values')

    if not selected:
        messagebox.showwarning('Warning','Please select the record')
    else:
        response=messagebox.askyesno('','Are you sure you want to delete record')
        if response==1:
            selected=my_tree.focus()
            values = my_tree.item(selected, 'values')
            x="DELETE from customers WHERE inc_num = '{}'".format(values[8])
            my_cursor.execute(x)
            mydb.commit()
            show_all()

def update_values():

    selected=my_tree.focus()
    values = my_tree.item(selected, 'values')
    if not selected:
            messagebox.showwarning('Warning','Please select the record')

    TOID=tourID_entry.get()
    name=dname_entry.get()
    last_name=dlname_entry.get()
    TID=truckID_entry.get()
    TOP=tourP_entry.get()
    MIL=mil_entry.get()

    if TOID=="":
        tourID_entry.insert(END,values[0])
    if name=="":
        dname_entry.insert(END,values[1])
    if last_name=="":
        dlname_entry.insert(END,values[2])
    if TID=="":
        truckID_entry.insert(END,values[3])
    if TOP=="":
        tourP_entry.insert(END,values[4])
    if MIL=="":
        mil_entry.insert(END,values[5])

    TOID=tourID_entry.get()
    name=dname_entry.get()
    last_name=dlname_entry.get()
    TID=truckID_entry.get()
    TOP=tourP_entry.get()
    MIL=mil_entry.get()
    
    z="SELECT * FROM customers"
    my_cursor.execute(z)
    items=my_cursor.fetchall()

    approval=0
    for item in items:
        if item[0]==int(TOID) and item[0]!=int(values[0]):
            messagebox.showwarning('Warning','Tour ID'+' '+ TOID +' '+'already exists in the database')
            approval=1

    if approval==0:
        #if TOID!="" and name !="" and last_name!="":
        responseC=messagebox.askyesno('','Do you want to upload tour confirmation document')
        if responseC==1:
            confirmation=upload_doc()
            if confirmation=="":
                confirmation=values[6]#'No tour confirmation document'
        else:
            confirmation=values[6]
        responseD=messagebox.askyesno('','Do you want to upload delivery order document')
        if responseD==1:
            delivery=[""]
            for s in range(4):
                delivery[s]=upload_doc()
                if delivery[s]!="" and s<3:
                    responseN=messagebox.askyesno('','Do you want to upload one more delivery order document')
                    if responseN==1:
                        delivery.append("")
                    else:
                        break
                else:
                    break

        
            if delivery==[""]:
                delivery=values[7]
        else:
            delivery=values[7]
        if delivery==values[7]:
            x=str(delivery)
        else:
            if delivery[len(delivery)-1]=="":
                delivery.pop()
            x=",".join(delivery)
            

        c="UPDATE customers SET tour_id = {},driver_name='{}',driver_last_name ='{}',truck_id ={},tour_price ={},confirmation ='{}',delivery_order='{}' WHERE inc_num = {}".format(tourID_entry.get(),dname_entry.get().replace(" ",""),dlname_entry.get().replace(" ",""),truckID_entry.get(),tourP_entry.get(),confirmation,x,values[8])
        my_cursor.execute(c)
        #my.fetchall()
        

        mydb.commit()

    tourID_entry.delete(0,END)
    dname_entry.delete(0,END)
    dlname_entry.delete(0,END)
    truckID_entry.delete(0,END)
    tourP_entry.delete(0,END)
    mil_entry.delete(0,END)
   

    show_all()
   
 
dark_title_bar(mainPage)


#Add some style
style=ttk.Style()

#Pick a theme
style.theme_use("default")

#Configure a style
style.configure("Treeview",
        background="#D3D3D3",
        foreground="black",
        rowheight=25,
        fieldbackground="#D3D3D3")

#Change selected color
style.map("Treeview",
    backround=[('selected','#347083')])

#Create treeview frame 
tree_frame=Frame(mainPage).pack(pady=10)

#Create treevies scrollbar
tree_scroll=Scrollbar(tree_frame)
tree_scroll.pack(side=RIGHT,fill=Y)

#Create treeview

my_tree=ttk.Treeview(tree_frame,yscrollcommand=tree_scroll.set,selectmode="extended")
my_tree.pack()

#Configure scrollcommand

tree_scroll.config(command=my_tree.yview)

#Define column

my_tree["columns"]=("tour_id","driver_name","driver_last_name","truck_id","tour_price","mileage","confirmation","delivery_order","inc_num")

#Format columms


my_tree.column("#0",width=0,stretch=NO)
my_tree.column("tour_id",anchor=W,width=140)
my_tree.column("driver_name",anchor=CENTER,width=140)
my_tree.column("driver_last_name",anchor=CENTER,width=140)
my_tree.column("truck_id",anchor=CENTER,width=140)
my_tree.column("tour_price",anchor=CENTER,width=140)
my_tree.column("mileage",anchor=CENTER,width=140)
my_tree.column("confirmation",anchor=CENTER,width=200)
my_tree.column("delivery_order",anchor=CENTER,width=200)
my_tree.column("inc_num",anchor=CENTER,width=140)


#Create headings

my_tree.heading('#0', text="", anchor=W)
my_tree.heading('tour_id', text="Tour ID", anchor=W)
my_tree.heading('driver_name', text="Driver Name", anchor=CENTER)
my_tree.heading('driver_last_name', text="Driver Last Name", anchor=CENTER)
my_tree.heading('truck_id', text="Truck ID", anchor=CENTER)
my_tree.heading('tour_price', text="Tour Price", anchor=CENTER)
my_tree.heading('mileage', text="Mileage", anchor=CENTER)
my_tree.heading('confirmation', text="Confirmation", anchor=CENTER)
my_tree.heading('delivery_order', text="Delivery Order", anchor=CENTER)
my_tree.heading('inc_num', text="ID", anchor=CENTER)


def delete_database():
    response=messagebox.askyesno('','Are you sure you want to delete all records')
    if response==1:
        messagebox.showwarning('Warning','Application will shut down')
        sql_command="DROP TABLE customers"
        my_cursor.execute(sql_command)
        exit()


def show_all():
    #Query the database
    x="SELECT * FROM customers"
    my_cursor.execute(x)
    items = my_cursor.fetchall()
    print(items)
    
    #Create Striped Row Tags

    my_tree.tag_configure("oddrow",background="white")
    my_tree.tag_configure("evenrow",background="lightblue")

    #Add our data to the screen

    global count
    count=0
    for i in my_tree.get_children():
        my_tree.delete(i)

    for record in items:
        if count % 2==0:
            my_tree.insert(parent='',index='end',iid=count,text="",values=(record[0],record[1],record[2],record[3],record[4],record[5],record[6],record[7],record[8]),tags=('evenrow',))
        else:
            my_tree.insert(parent='',index='end',iid=count,text="",values=(record[0],record[1],record[2],record[3],record[4],record[5],record[6],record[7],record[8]),tags=('oddrow',))
        count+=1


show_all()


def add_and_refresh():
    insert_values()
    show_all()

def extension_checker(doc):


    def file_selection():
        selected=my_tree.focus()
        values = my_tree.item(selected, 'values')
        x=values[doc].split(',')
        if len(x)>1:
            selectedDrop=drop.get()
            pp=""
            if selectedDrop=="file1":
                pp=x[0]
            if selectedDrop=="file2":
                pp=x[1]
            if selectedDrop=="file3":
                pp=x[2]
            if selectedDrop=="file4":
                pp=x[3]
        else:
            pp=x[0]
        t=pathlib.Path(pp).suffix
        if t=="jpg":
            open_jpg(pp)
        else:
            open_pdf(pp)

    selected=my_tree.focus()
    values = my_tree.item(selected, 'values')
    if not selected:
            messagebox.showwarning('Warning','Please select the record')
    else:
        x=values[doc].split(',')
        if len(x)>1:
            filePage=Toplevel()
            filePage.title("Select file")
            #filePage.iconbitmap('C:/Users/VladimirP1984/Documents/SQLITE/Projects/python/truck_b.ico')
            filePage.geometry("400x100")
            tt=["Select file..."]
            for i in range(len(x)):
                rr="file{}".format(i+1)
                tt.append(rr)
            drop=ttk.Combobox(filePage,value=tt)
            drop.current(0)
            drop.grid(row=2,column=2,padx=10)
            open_file_button=Button(filePage,text="Open file",command=file_selection).grid(row=2,column=0,padx=10)
        else:
            file_selection()

def open_pdf(p):
    wb.open_new(p)

def open_jpg(self):
    my_image=Image.open(self)
    my_image.show()


def search_table():
    searchPage=Tk()
    searchPage.title("Search table")
    #searchPage.iconbitmap('C:/Users/VladimirP1984/Documents/SQLITE/Projects/python/truck_b.ico')
    searchPage.geometry("400x100")
    label3=Label(searchPage,text="Insert search").grid(row=1,column=0,padx=10,sticky=W)
    entryLN=Entry(searchPage)
    entryLN.grid(row=1,column=1,pady=5)
    def show_search():
        selected=drop.get()
        entry_field=entryLN.get()
        if selected =="Search by..." and entry_field!=None:
            items='Select your search'
        else:

            if selected=="driver name":
                x="SELECT * FROM customers WHERE driver_name = '{}'".format(entry_field)
            if selected=="driver last name":
                x="SELECT * FROM customers WHERE driver_last_name = '{}'".format(entry_field)
            if selected=="tour id":
                x="SELECT * FROM customers WHERE tour_id = '{}'".format(entry_field)
            my_cursor.execute(x)
            items=my_cursor.fetchall()
            print(items)
            if not items:
                items="Record Not Found"
            else:
                searchPage.destroy()
                global count
                count=0
                for i in my_tree.get_children():
                    my_tree.delete(i)

                for record in items:
                    if count % 2==0:
                        my_tree.insert(parent='',index='end',iid=count,text="",values=(record[0],record[1],record[2],record[3],record[4],record[5],record[6],record[7],record[8]),tags=('evenrow',))
                    else:
                        my_tree.insert(parent='',index='end',iid=count,text="",values=(record[0],record[1],record[2],record[3],record[4],record[5],record[6],record[7],record[8]),tags=('oddrow',))
                    count+=1

        searchLabel=Label(searchPage,text=items)
        searchLabel.grid(row=3,column=1)

        
    button_show_search=Button(searchPage,text="show search",command=show_search).grid(row=2,column=0,padx=10)
    drop=ttk.Combobox(searchPage,value=["Search by...","driver name","driver last name","tour id"])
    drop.current(0)
    drop.grid(row=1,column=2,padx=10)


#Add entry box

data_frame=LabelFrame(mainPage,text="Record")
data_frame.pack(fill="x",expand="yes",padx=20)

tourID_label=Label(data_frame,text="Tour ID")
tourID_label.grid(row=0,column=0,padx=10,pady=10)
tourID_entry=Entry(data_frame)
tourID_entry.grid(row=0,column=1,padx=10,pady=10)

dname_label=Label(data_frame,text="Driver Name")
dname_label.grid(row=0,column=2,padx=10,pady=10)
dname_entry=Entry(data_frame)
dname_entry.grid(row=0,column=3,padx=10,pady=10)

dlname_label=Label(data_frame,text="Driver Last Name")
dlname_label.grid(row=0,column=4,padx=10,pady=10)
dlname_entry=Entry(data_frame)
dlname_entry.grid(row=0,column=5,padx=10,pady=10)

truckID_label=Label(data_frame,text="Truck ID")
truckID_label.grid(row=1,column=0,padx=10,pady=10)
truckID_entry=Entry(data_frame)
truckID_entry.grid(row=1,column=1,padx=10,pady=10)

tourP_label=Label(data_frame,text="Tour Price")
tourP_label.grid(row=1,column=2,padx=10,pady=10)
tourP_entry=Entry(data_frame)
tourP_entry.grid(row=1,column=3,padx=10,pady=10)

mil_label=Label(data_frame,text="Mileage")
mil_label.grid(row=1,column=4,padx=10,pady=10)
mil_entry=Entry(data_frame)
mil_entry.grid(row=1,column=5,padx=10,pady=10)



#Add buttons

button_frame=LabelFrame(mainPage,text="Commands")
button_frame.pack(fill="x",expand="yes",padx=20)

LavaF=Label(button_frame,text="Lava Freight Data Base Centar",font=('Fixedsys',26),fg='Green')
LavaF.grid(row=0,column=2,padx=10,pady=10)
LavaFdamy=Label(button_frame,text="                                      ",font=('Fixedsys',26),fg='Green')
LavaFdamy.grid(row=1,column=2,padx=10,pady=10)

update_button=Button(button_frame,text="Update Records",width=20,command=update_values)
update_button.grid(row=0,column=1,padx=10,pady=10)

add_button=Button(button_frame,text="Add Records",command=add_and_refresh,width=20)
add_button.grid(row=0,column=0,padx=10,pady=10)

removeall_button=Button(button_frame,text="Remove All Records",command=delete_database,width=20)
removeall_button.grid(row=0,column=3,padx=10,pady=10)

remove_selected_button=Button(button_frame,text="Remove Selected Record",command=delete_record,width=20)
remove_selected_button.grid(row=1,column=3,padx=10,pady=10)

search_button=Button(button_frame,text="Search",command=search_table,width=20)
search_button.grid(row=1,column=0,padx=10,pady=10)


show_button=Button(button_frame,text="Show Table",command=show_all,width=20)
show_button.grid(row=1,column=1,padx=10,pady=10)

show_conf_button=Button(button_frame,text="Show Confirmation",command= lambda :extension_checker(6),width=20)   
show_conf_button.grid(row=0,column=4,padx=10,pady=10)

show_order_button=Button(button_frame,text="Show delivery Order",command=lambda :extension_checker(7),width=20)    #my_album 
show_order_button.grid(row=1,column=4,padx=10,pady=10)





mainPage.mainloop()