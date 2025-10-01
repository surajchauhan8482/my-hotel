from tkinter import *
from tkinter import messagebox,filedialog
import pymysql
from tkinter import ttk
from datetime import datetime
taz=Tk()
taz.title('Taz Hotel')
height=taz.winfo_screenheight()
#print(height)
width=taz.winfo_screenwidth()
#print(width)
######### for char input
# def only_char_input(P):
#     if P.isalpha() or P=='':
#         return True
#     return False
# callback=taz.register(only_char_input)
# # for digit
# def only_numeric_input(P):
#     if P.isdigit() or P=='':
#         return True
#     return False
# callback2=taz.register(only_numeric_input)
###############
# treeview
tazTV=ttk.Treeview(height=10,columns=('Item Name''Rate','Type'))
tazTV1=ttk.Treeview(height=10,columns=('Date''Name','Type','Rate','Total'))
def clear_screen():
    global taz
    for widgets in taz.winfo_children():
        widgets.grid_remove()
def menu_bar():
    if nameVar.get()=='' or typeVar.get()=='' or rateVar.get()=='':
        messagebox.showerror('Data Validation Error','Please Fill All Details of Item')
    else:
        # print(usernameVar.get())
        # print(passwordVar.get())
        dbconfig()
        name = nameVar.get()
        print(name.capitalize())
        type = typeVar.get()
        rate = rateVar.get()
        dbconfig()
        queins = "insert into menu_item (name,rate,type) values(%s,%s,%s)"
        val = (name, rate, type)
        mycursor.execute(queins, val)
        conn.commit()
        messagebox.showinfo('Data Saved','Data Saved Successfully')
def update_items():
    if nameVar.get() == '' or typeVar.get() == '' or rateVar.get() == '':
        messagebox.showerror('Data Validation Error', 'Please Fill All Details of Item')
    else:
        name = nameVar.get()
        type = typeVar.get()
        rate = rateVar.get()
        dbconfig()
        queup = "update menu_item set rate=%s, type=%s where name=%s"
        val = (rate, type,name)
        mycursor.execute(queup, val)
        conn.commit()
        messagebox.showinfo('Data Updated', 'Data Updated Successfully')
        nameVar.set('')
        typeVar.set('')
        rateVar.set('')
def delete_items():
    if nameVar.get() == '' or typeVar.get() == '' or rateVar.get() == '':
        messagebox.showerror('Data Validation Error', 'Please Fill All Details of Item')
    else:
        name = nameVar.get()
        type = typeVar.get()
        rate = rateVar.get()
        dbconfig()
        queup = "delete from menu_item where name=%s"
        val = (name)
        mycursor.execute(queup, val)
        conn.commit()
        messagebox.showinfo('Data Delete', 'Data Delete Successfully')
        nameVar.set('')
        typeVar.set('')
        rateVar.set('')
#######

#######
nameVar=StringVar()
typeVar=StringVar()
rateVar=StringVar()
def insert_items():
    clear_screen()
    main_heading()
    insert_item= Label(taz, text=" Insert_Items", font=("ariel", 25, "bold"))
    insert_item.grid(row=1, column=1, columnspan=2)
    item_name = Label(taz, text="itemsname", font=("ariel",15, "bold"))
    item_name.grid(row=2, column=1,padx=20, pady=5)
    itemname_entry = Entry(taz, textvariable=nameVar)
    itemname_entry.grid(row=2, column=2,padx=20, pady=5)
    #for validation
    # itemname_entry.configure(validate="key",validatecommand=(callback,"%p"))
    item_type = Label(taz, text="itemstype", font=("ariel", 15, "bold"))
    item_type.grid(row=3, column=1,padx=20, pady=5)
    itemtype_entry = Entry(taz, textvariable=typeVar)
    itemtype_entry.grid(row=3, column=2,padx=20, pady=5)
    item_rate = Label(taz, text="itemsrate", font=("ariel", 15, "bold"))
    item_rate.grid(row=4, column=1,padx=20, pady=5)
    itemrate_entry = Entry(taz, textvariable=rateVar)
    itemrate_entry.grid(row=4, column=2,padx=20, pady=5)
    # itemrate_entry.configure(validate="key", validatecommand=(callback2, "%p"))
    updateitems_btn= Button(taz, text="Update", width=10, height=2,bg="pink" ,fg="black",bd=10,command=update_items)
    updateitems_btn.grid(row=5, column=0,padx=20, pady=5)
    deleteitems_btn1 = Button(taz, text="Delete", width=10, height=2, bg="pink", fg="black", bd=10,command=delete_items)
    deleteitems_btn1.grid(row=5, column=3, padx=20, pady=5)
    additems_btn1 = Button(taz, text="add items", width=10, height=2, bg="pink", fg="black", bd=10,command=menu_bar)
    additems_btn1.grid(row=5, column=1, columnspan=2,padx=20, pady=5)
    back_btn = Button(taz, text="back", width=5, height=2,bg="white" ,fg="black",bd=10,command=welcomewindow)
    back_btn.grid(row=2, column=0,padx=20, pady=5)
    save_btn = Button(taz, text="save", width=5, height=2, bg="white", fg="black", bd=10)
    save_btn.grid(row=2, column=3, padx=20, pady=5)
    #####
    # treeview
    tazTV.grid(row=6, column=1, columnspan=2)
    style = ttk.Style(taz)
    style.theme_use('clam')
    style.configure("Treeview", fieldbackground="red")
    scrollBar = Scrollbar(taz, orient="vertical", command=tazTV.yview)
    scrollBar.grid(row=6, column=2, sticky="NSE")

    tazTV.configure(yscrollcommand=scrollBar.set)
    tazTV.heading('#0', text="Item Name")
    tazTV.heading('#1', text="Rate")
    tazTV.heading('#2', text="Type")
    getItemInTreeview()
    #####
def OnDoubleClick(event):
    item=tazTV.selection()
    itemNameVar1=tazTV.item(item,"text")
    item_detail = tazTV.item(item, "values")
    # print(itemNameVar1)
    # print(item_detail)
    nameVar.set(itemNameVar1)
    rateVar.set(item_detail[0])
    typeVar.set(item_detail[1])
##getitem in treeview
def getItemInTreeview():
    # to delete already inserted data
    records=tazTV.get_children()
    for x in records:
        tazTV.delete(x)
    conn=pymysql.connect(host="localhost",user="root",db="tazhotel")
    mycursor=conn.cursor(pymysql.cursors.DictCursor)
    query1="select * from menu_item"
    mycursor.execute(query1)
    data=mycursor.fetchall()
    # print(data)
    for row in data:
        tazTV.insert('','end',text=row['name'],values=(row["rate"],row['type']))
    conn.close()
    tazTV.bind("<Double-1>",OnDoubleClick)
##
global x
x=datetime.now()
datetimeVar=StringVar()
datetimeVar.set(x)
customernameVar=StringVar()
contectnoVar=StringVar()
combovariable=StringVar()
baserate=StringVar()
cost=StringVar()
qtyvariable=StringVar()
mobile=StringVar()
#####combo data######
def combo_input():
    dbconfig()
    mycursor.execute("select * from menu_item")
    data=[]
    for row in mycursor.fetchall():
        data.append(row[0])
    return data
############optioncallback
def optionCallBack(*arg):
    global itemname,v
    itemname=combovariable.get()
    # print(itemname)
    aa=ratelist()
    print(aa)
    baserate.set(aa)
    for i in aa:
        for j in i:
            v=j
######optioncallback2
def optionCallBack2(*arg):
    global qty
    qty=qtyvariable.get()
    final=int(v)*int(qty)
    cost.set(final)
########ratelist
def ratelist():
    dbconfig()
    que2=("select rate from menu_item where name=%s")
    val=(itemname)
    mycursor.execute(que2,val)
    data=mycursor.fetchall()
    print(data)
    return data
##########
def bill():
    clear_screen()
    main_heading()
    generateBill = Label(taz, text="Generate Bill",fg="red",font=("ariel", 18, "bold"))
    generateBill.grid(row=1, column=1,columnspan=2, padx=20, pady=5)
    back_btn = Button(taz, text="back", width=5, height=2, bg="white", fg="black", bd=10, command=welcomewindow)
    back_btn.grid(row=1, column=0, padx=20, pady=5)
    logoutButton = Button(taz, text="Logout", width=5, height=2, bg="white", fg="black", bd=10, command=adminLogout)
    logoutButton.grid(row=1, column=3, padx=15, pady=50)
    printbtn=Button(taz, text="Print", width=5, height=2, bg="white", fg="black", bd=10,command=printBill )
    printbtn.grid(row=2, column=0, padx=15, pady=50)

    # datetime label
    dateTimeLabel=Label(taz,text="Date and Time",font=("ariel", 15, "bold"))
    dateTimeLabel.grid(row=2, column=1, padx=20, pady=5)
    dateTimeEntry = Entry(taz, textvariable=datetimeVar)
    dateTimeEntry.grid(row=2, column=2, padx=20, pady=5)
    #costermor name label
    CustomerNameLabel = Label(taz, text="Custer Name", font=("ariel", 15, "bold"))
    CustomerNameLabel.grid(row=3, column=1, padx=20, pady=5)
    customernameEntry = Entry(taz, textvariable=customernameVar)
    customernameEntry.grid(row=3, column=2, padx=20, pady=5)
    #contect label
    ContectNoLabel = Label(taz, text="Contect No", font=("ariel", 15, "bold"))
    ContectNoLabel.grid(row=4, column=1, padx=20, pady=5)
    contectNoEntry = Entry(taz, textvariable=contectnoVar)
    contectNoEntry.grid(row=4, column=2, padx=20, pady=5)

    selectLabel = Label(taz, text="Select Item", font=("ariel", 15, "bold"))
    selectLabel.grid(row=5, column=1, padx=20, pady=5)
    l=combo_input()
    c=ttk.Combobox(taz,values=l,textvariable=combovariable)
    c.set("select Item")
    combovariable.trace('w',optionCallBack)
    c.grid(row=5, column=2, padx=20, pady=5)
    rateLabel = Label(taz, text="Rate", font=("ariel", 15, "bold"))
    rateLabel.grid(row=6, column=1, padx=20, pady=5)
    rateEntry=Entry(taz,textvariable=baserate)
    rateEntry.grid(row=6, column=2, padx=20, pady=5)
    qtyLabel = Label(taz, text="select quantity", font=("ariel", 15, "bold"))
    qtyLabel.grid(row=7, column=1, padx=20, pady=5)
    global qtyvariable
    l2 = [1,2,3,4,5,]
    qty = ttk.Combobox(taz, values=l2, textvariable=qtyvariable)
    qty.set("select quantity")
    qtyvariable.trace('w', optionCallBack2)
    qty.grid(row=7, column=2, padx=20, pady=5)
    costLabel = Label(taz, text="cost", font=("ariel", 15, "bold"))
    costLabel.grid(row=8, column=1, padx=20, pady=5)
    costEntry = Entry(taz, textvariable=cost)
    costEntry.grid(row=8, column=2, padx=20, pady=5)
    billBtn=Button(taz,text="Save Bill",width=8, height=2,bg="red",fg="black",bd=10,command=saveBill)
    billBtn.grid(row=9, column=2, padx=20, pady=5)
######printBill
def printBill():
    clear_screen()
    main_heading()
    billDetails = Label(taz, text="Bill details", fg="red", font=("ariel", 18, "bold"))
    billDetails.grid(row=1, column=1, columnspan=2, padx=20, pady=5)
    back_btn = Button(taz, text="back", width=5, height=2, bg="white", fg="black", bd=10, command=bill)
    back_btn.grid(row=1, column=0, padx=20, pady=5)
    logoutButton = Button(taz, text="Logout", width=5, height=2, bg="white", fg="black", bd=10, command=adminLogout)
    logoutButton.grid(row=1, column=3, padx=15, pady=50)
####treeviw1
    tazTV1.grid(row=5, column=0, columnspan=4)
    style = ttk.Style(taz)
    style.theme_use('clam')
    style.configure("Treeview", fieldbackground="pink")
    scrollBar = Scrollbar(taz, orient="vertical", command=tazTV.yview)
    scrollBar.grid(row=5, column=5, sticky="NSE")

    tazTV1.configure(yscrollcommand=scrollBar.set)
    tazTV1.heading('#0', text="Date/Time")
    tazTV1.heading('#1', text="Name")
    tazTV1.heading('#2', text="Mobil")
    tazTV1.heading('#3', text="Select Food")
    tazTV1.heading('#4', text="Price")
    displaybill()
########
def displaybill():
    # to delete already inserted data
    records=tazTV1.get_children()
    for x in records:
        tazTV1.delete(x)
    conn=pymysql.connect(host="localhost",user="root",db="tazhotel")
    mycursor=conn.cursor(pymysql.cursors.DictCursor)
    query1="select * from bill"
    mycursor.execute(query1)
    data=mycursor.fetchall()
    # print(data)
    for row in data:
        tazTV1.insert('','end',text=row['datetime'],values=(row["custemer_name"],row['contect_number'],row['item_name'],row['cost']))
    conn.close()
    tazTV1.bind("<Double-1>",OnDoubleClick2)
########double click2
def OnDoubleClick2(event):
    item = tazTV1.selection()
    global itemNameVar11
    itemNameVar11 = tazTV1.item(item, "text")
    item_detail = tazTV1.item(item, "values")
    recipt()
    # print(itemNameVar1)
    # print(item_detail)
# ########
def recipt():
    billstring =""
    billstring+= "=====================My hotel Bill==========\n\n"
    billstring+= "====================customer details==========\n\n"
    dbconfig()
    query="select * from bill where datetime='{}';".format(itemNameVar11)
    mycursor.execute(query)
    data=mycursor.fetchall()
    print(data)
    for row in data:
        billstring +="{}{:<20}{:<10}\n".format("date/time","",row[1])
        billstring +="{}{:<20}{:10}\n".format("Customer Name","",row[2])
        billstring +="{}{:<20}{:<10}\n".format("Contect No","",row[3])
        billstring +="\n===========Item Detail=========\n"
        billstring+="{:<10}{:<10}{:<15}{:<15}\n".format("Item Name","rate","Quantity","Price")
        billstring+="\n{:<10}{:<10}{:<25}{:<25}".format(row[4],row[5],row[6],row[7])
        billstring+="==================================\n"
        billstring+="{}{:<10}{:<15}{:<10}\n".format("Total Cost","","",row[7])
        billstring+="\n\n===============thanks Please Visit Again==============\n"
    billFile=filedialog.asksaveasfile(mode="w",defaultextension=".txt")
    if billFile is None:
        messagebox.showerror("Error", "No file selected")
    else:
        billFile.write(billstring)
        billFile.close()


######
def saveBill():
    dt=datetimeVar.get()
    custname = customernameVar.get()
    mobile = contectnoVar.get()
    item_name = itemname
    itemrate = v
    itemqty = qtyvariable.get()
    total = cost.get()
    dbconfig()
    insqu = "insert into bill(datetime,custemer_name,contect_number,item_name,item_rate,item_qty,cost)"\
              "values(%s,%s,%s,%s,%s,%s,%s)"
    val = (dt, custname, mobile, item_name, itemrate, itemqty, total)
    mycursor.execute(insqu, val)
    conn.commit()
    messagebox.showinfo("Bill Saved", "Bill Saved")
    customernameVar.set("")
    contectnoVar.set("")
    itemname.set("")
    cost.set("")


    ######
def clear_screen():
    global taz
    for widgets in taz.winfo_children():
        widgets.grid_remove()
def dbconfig():
    global conn, mycursor
    conn=pymysql.connect(host="localhost",user="root",db="tazhotel")
    mycursor=conn.cursor()

def adminLogout():
    clear_screen()
    main_heading()
    loginwindow()
def adminLogin():
    if usernameVar.get()=='' or passwordVar.get()=='':
        messagebox.showerror("Error",'Please enter Both Entries')
    else:
        # print(usernameVar.get())
        # print(passwordVar.get())
        dbconfig()
        username = usernameVar.get()
        password = passwordVar.get()
        #excuet query
        que = "select * from login_info where username=%s and password=%s"
        # que = "update login_info set username =%s, password =%s where username =rahul and password =admin"
        val = (username, password)
        mycursor.execute(que, val)
        #fatch data
        data = mycursor.fetchall()
        print(data)
        flag = False
        for row in data:
            flag = True
        conn.close()

        if flag == True:
            welcomewindow()
            # messagebox.showwarning('','login successfull')
        else:
            messagebox.showerror("Invalid User Credential", "Either User Name or Password is Incorrect")
            usernameVar.set("")
            passwordVar.set("")
#main heading
def main_heading():
    label=Label(taz,text="Ajnabi Management System",fg="red",bg="blue",
            font=("comic sans Ms",40,"bold"),padx=400,pady=0)
    label.grid(row=0,columnspan=4)
usernameVar=StringVar()
passwordVar=StringVar()
def loginwindow():
    # clear_screen()
    # main_heading()
    # usernameVar.set("")
    # passwordVar.set("")
    labellogin=Label(taz,text="Admin Login",font=("ariel",25,"bold"))
    labellogin.grid(row=1,column=1,columnspan=2,padx=50,pady=10)

    usernameLabel=Label(taz,text="User Name",font=("ariel",12,"bold"))
    usernameLabel.grid(row=2,column=1,padx=20,pady=5)

    passwordLabel = Label(taz, text="User Password",font=("ariel",12,"bold"))
    passwordLabel.grid(row=3, column=1, padx=20, pady=5)

    usernameEntry=Entry(taz,textvariable=usernameVar)
    usernameEntry.grid(row=2,column=2,padx=20,pady=5)

    passwordEntry=Entry(taz,show="*",textvariable=passwordVar)
    passwordEntry.grid(row=3, column=2, padx=20, pady=5)

    loginButton=Button(taz,text="Login",width=20,height=2,fg="green",bd=10,command=adminLogin)
    loginButton.grid(row=4, column=1, columnspan=2,padx=20, pady=50)

# welcome window
def welcomewindow():
    clear_screen()
    main_heading()
    labelwelcome = Label(taz, text=" Welcome Admin ",justify="center", font=("ariel", 25, "bold"))
    labelwelcome.grid(row=1, column=1, columnspan=1, padx=20, pady=5)
    logoutButton = Button(taz, text="Logout" ,width=20, height=2, fg="green", bd=5, command=adminLogout)
    logoutButton.grid(row=3, column=2, padx=15, pady=50)

    manageRestorent = Button(taz, text="ManageRestorent" ,width=20, height=2, fg="green", bd=5, command=insert_items)
    manageRestorent.grid(row=3, column=0, padx=15, pady=50)

    bilgenrate = Button(taz, text='Billgenrate',width=20, height=2, fg="red", bd=5, command=bill)
    bilgenrate.grid(row=3, column=1, padx=15, pady=50)
loginwindow()
main_heading()
taz.geometry("%dx%d+0+0"%(width,height))
taz.mainloop()
