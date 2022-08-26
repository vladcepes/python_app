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


mainPage=Tk()
mainPage.title("Lava Freight Data Centar")
mainPage.iconbitmap('images/truck_b.ico')
mainPage.state("zoomed")


mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    passwd ="Automation%2025",
    database = "LavaFreight",
    )
#Create cursor and initialize it
my_cursor=mydb.cursor()

#Create table

my_cursor.execute("CREATE TABLE IF NOT EXISTS customers(tour_id INT(20),\
    driver_name VARCHAR(255),\
    driver_last_name VARCHAR(255),\
    truck_id INT(20),\
    tour_price DECIMAL(20,2),\
    mileage INT(20),\
    confirmation VARCHAR(255),\
    delivery_order VARCHAR(255),\
    inc_num INT AUTO_INCREMENT PRIMARY KEY)")

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
    name=dname_entry.get()
    last_name=dlname_entry.get()
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
            
            sql_command="INSERT INTO customers (tour_id,driver_name,driver_last_name,truck_id,tour_price,mileage,confirmation,delivery_order) VALUES (%s,%s,%s,%s,%s,%s,%s,%s)"
            values=(TOID,name,last_name,TID,TOP,MIL,confirmation,x)
            my_cursor.execute(sql_command,values)
            
            
            mydb.commit()
        else:
            messagebox.showwarning('Warning','Tour ID,Driver Name and Driver Last name are mandatory field')



def upload_doc():
 
    file_path_string = filedialog.askopenfilename()
    return file_path_string

def delete_record():

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
    TOIDU=tourID_entry.get()
    nameU=dname_entry.get()
    last_nameU=dlname_entry.get()
    z="SELECT * FROM customers"
    my_cursor.execute(z)
    items=my_cursor.fetchall()
    approval=0
    for item in items:
        if item[0]==int(TOIDU):
            messagebox.showwarning('Warning','Tour ID'+' '+ TOIDU +' '+'already exists in the database')
            approval=1
    if approval==0:   
        if not selected:
            messagebox.showwarning('Warning','Please select the record you want tu update')
        else:
            if TOIDU!="" and nameU !="" and last_nameU!="":
                responseC=messagebox.askyesno('','Do you want to upload different tour confirmation document')
                if responseC==1:
                    confirmationU=upload_doc()
                    if confirmationU=="":
                        confirmationU=values[6]
                else:
                    confirmationU=values[6]
                responseD=messagebox.askyesno('','Do you want to upload different delivery order document')
                if responseD==1:
                    deliveryU=upload_doc()
                    if deliveryU=="":
                        deliveryU=values[7]
                else:
                    deliveryU=values[7] 
                x="UPDATE customers SET tour_id = {},driver_name='{}',driver_last_name ='{}',truck_id ={},tour_price ={},confirmation ='{}',delivery_order='{}' WHERE inc_num = {}".format(tourID_entry.get(),dname_entry.get(),dlname_entry.get(),truckID_entry.get(),tourP_entry.get(),confirmationU,deliveryU,values[8])
                my_cursor.execute(x)
                #my.fetchall()
                mydb.commit()
            else:
                messagebox.showwarning('Warning','Tour ID,Driver Name and Driver Last Name are mandatory field')
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
    sql_command="DROP TABLE customers"
    my_cursor.execute(sql_command)


def show_all():
    #Query the database
    x="SELECT * FROM customers"
    my_cursor.execute(x)
    items = my_cursor.fetchall()
    
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
#Creating album 
def my_album():
    album=Toplevel()
    album.title("lava freight")
    album.iconbitmap('images/truck_b.ico')



    selected=my_tree.focus()
    values = my_tree.item(selected, 'values')
    x=values[7].split(",")

    my_image1=Image.open(x[0])
    new_image1=my_image1.resize((400,400))
    new_image1.save('truck1.jpg')
    my_image2=ImageTk.PhotoImage(Image.open(x[1]))
    my_image3=ImageTk.PhotoImage(Image.open(x[2]))
    my_image4=ImageTk.PhotoImage(Image.open(x[3]))
    
    image_list=[my_image1,my_image2,my_image3,my_image4]

    my_Label=Label(album,image=my_image1)
    my_Label.grid(row=0,column=0,columnspan=3)
    #my_Label.grid_forget()


    def forward(image_number):
        if image_number<len(image_list):
            global my_Label
            my_Label.grid_forget()
            my_Label=Label(album,image=image_list[image_number])
            my_Label.grid(row=0,column=0,columnspan=3)
            global button_forward
            button_forward=Button(album, text='>>', command=lambda: forward(image_number+1))
            button_forward.grid(row=1,column=2)
            global button_back
            button_back=Button(album, text='<<', command=lambda: back(image_number-1))
            button_back.grid(row=1,column=0)


    def back(image_number):
        if image_number>=0:
            global my_Label
            my_Label.grid_forget()
            my_Label=Label(album,image=image_list[image_number])
            my_Label.grid(row=0,column=0,columnspan=3)
            global button_back
            button_back=Button(album, text='<<', command=lambda: back(image_number-1))
            button_back.grid(row=1,column=0)
            global button_forward
            button_forward=Button(album, text='>>', command=lambda: forward(image_number+1))
            button_forward.grid(row=1,column=2)
        



    button_quit=Button(album, text='Exit Program', command=album.quit)
    button_quit.grid(row=1,column=1)

    button_back=Button(album, text='<<', command=lambda: back(0))
    button_back.grid(row=1,column=0)

    button_forward=Button(album, text='>>', command=lambda: forward(1))
    button_forward.grid(row=1,column=2)


    

def add_and_refresh():
    insert_values()
    show_all()

def open_confirmation():
    selected=my_tree.focus()
    values = my_tree.item(selected, 'values')
    wb.open_new(values[6])

def open_delivery():
    selected=my_tree.focus()
    values = my_tree.item(selected, 'values')
    #print(values[7])
    x=values[7].split(',')
    my_image=Image.open(x[2])
    my_image.show()

#def check_file_type()

def search_table():
    searchPage=Tk()
    searchPage.title("Search table")
    searchPage.iconbitmap('images/truck_b.ico')
    searchPage.geometry("400x100")
    label3=Label(searchPage,text="Insert search").grid(row=1,column=0,padx=10,sticky=W)
    entryLN=Entry(searchPage)
    entryLN.grid(row=1,column=1,pady=5)
    def show_search():
        selected=drop.get()
        entry_field=entryLN.get()
        if selected=="driver name":
            x="SELECT * FROM customers WHERE driver_name = '{}'".format(entry_field)
        if selected=="driver last name":
            x="SELECT * FROM customers WHERE driver_last_name = '{}'".format(entry_field)
        if selected=="tour id":
            x="SELECT * FROM customers WHERE tour_id = '{}'".format(entry_field)
        my_cursor.execute(x)
        items=my_cursor.fetchall()
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

update_button=Button(button_frame,text="Update Records",width=20,command=update_values)
update_button.grid(row=0,column=0,padx=10,pady=10)

add_button=Button(button_frame,text="Add Records",command=add_and_refresh,width=20)
add_button.grid(row=0,column=1,padx=10,pady=10)

removeall_button=Button(button_frame,text="Remove All Records",command=delete_database,width=20)
removeall_button.grid(row=0,column=2,padx=10,pady=10)

remove_selected_button=Button(button_frame,text="Remove Selected Record",command=delete_record,width=20)
remove_selected_button.grid(row=1,column=0,padx=10,pady=10)

search_button=Button(button_frame,text="Search",command=search_table,width=20)
search_button.grid(row=1,column=1,padx=10,pady=10)


show_button=Button(button_frame,text="Show Table",command=show_all,width=20)
show_button.grid(row=1,column=2,padx=10,pady=10)

show_conf_button=Button(button_frame,text="Show Confirmation",command=open_confirmation,width=20)   
show_conf_button.grid(row=0,column=3,padx=10,pady=10)

show_order_button=Button(button_frame,text="Show delivery Order",command=my_album,width=20)    #open_delivery 
show_order_button.grid(row=1,column=3,padx=10,pady=10)



mainPage.mainloop()