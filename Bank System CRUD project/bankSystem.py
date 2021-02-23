#PROJECT NAME: NETBANKING SYSTEM FOR BANK OF MAHARSHTRA
#STUDENT NAME: NAYAN MANDLIK
#SUBMIT DATE: 7/JUN/2020

from tkinter import *
from tkinter import messagebox,ttk
from PIL import Image, ImageTk
import mysql.connector
import random
import datetime

root=Tk()
root.title("BANK OF MAHARASHTRA")
root.geometry("1200x700")
root.resizable(False,False)

#global variable declaration
currentUser=StringVar()
balance=int()
tempbal=int()
tempbalance=int()
date = datetime.datetime.now()
date= date.strftime("%d,%B,%Y")

#global connection to database for multiuses
conn= mysql.connector.connect(
            host="localhost",
            user="root",
            passwd="root",
            database='bankSystem'
        )
print(conn)
cursor = conn.cursor()


#-------------------------------BACKEND CODE START HERE----------------------------------------
def click(frm):
    global tempbal,date, enterAmount,balance,currentUser,tempbalance

    if frm=="f2":
        Frame.tkraise(f2)

    elif frm=="f3":
        Frame.tkraise(f3)

    elif frm=="f4":
        balanceForF4Label.set(tempbal)
        Frame.tkraise(f4)
       

    elif frm=="f5":
        Frame.tkraise(f5)

    elif frm=="f6":
        Frame.tkraise(f6)
    
    elif frm=="register":
        #to regester new user in register table
        name = Name.get()
        adress =Adress.get()
        email = Email.get()
        gender = Gender.get()
        phoneNumber  = PhoneNumber.get()
        acType = AcType.get()
        acNumber=random.randint(100000000000000,999999999999999)
        panNumber = PanNumber.get()
        password = Password.get()

        #create table register(Name varchar(30) not null, Adress varchar(40) not null, Email varchar(30), Gender varchar(20) not null, PhoneNumber varchar(20) not null, AccountType varchar(20) not null, AccountNumber varchar(20), PanNumber varchar(20) not null, Password varchar(20) not null);
        #create table transactions(Email varchar(30),date varchar(20) not null, transactionType varchar(10) not null, amount int not null, balance int not null, foreign key(Email) references users(Email));
        
        query='insert into users(Name,Adress,Email,Gender,PhoneNumber,AccountType,AccountNumber,PanNumber,Password) values(%s,%s,%s,%s,%s,%s,%s,%s,%s)'
        values=(name,adress,email,gender,phoneNumber,acType,acNumber,panNumber,password)
        cursor.execute(query,values)
        conn.commit()
        print(cursor.rowcount,'rows inserted.')

        Frame.tkraise(f2)

    elif frm=="login":
        #code to display balance after succesfully login on transaction page
        currentUser=userid.get()
        Query = "select * from transactions where Email='{user}'".format(user=currentUser)
        cursor.execute(Query)
        records = cursor.fetchall()

        for row in records:
            balance=row[4]
            tempbalance=balance

        balanceForF4Label.set(tempbalance)
        
        #login authentication code start here
        count=0
        flag="false"
        currentUser=userid.get()

        Query = "select * from users"
        cursor.execute(Query)
        records = cursor.fetchall()
        print("Total number of users : ", cursor.rowcount)

        useridValue=userid.get()
        passwordValue=password1.get()

        for row in records:
            if useridValue==row[2] and passwordValue==row[8]:
                Frame.tkraise(f4)
                flag="true"
                break
            else:
                count=count+1
            
        if count > 0 and flag=="false" :
            messagebox.showinfo("LOGIN FAILED", "USERNAME OR PASSWORD SHOULD BE WRONG?")
        
    elif frm=="updateBalance":
        #block start for getting recent avilable balance of user from databse.
        currentUser=userid.get()
        transactionType=r1.get()
        amount=int(enterAmount.get())

        Query = "select * from transactions where Email='{user}'".format(user=currentUser)
        cursor.execute(Query)
        records = cursor.fetchall()
        print("Total number of row in transactions: ", cursor.rowcount)

        for row in records:
            balance=row[4]

        if transactionType=="credit":
            balance= balance + amount
        else:
            balance= balance - amount

        tempbal=balance
        balanceForF5Label.set(tempbal)

        #insert transaction data in database
        Query='insert into transactions(Email,date,transactionType,amount,balance) values(%s,%s,%s,%s,%s)'
        values=(currentUser,date,transactionType,amount,balance)
        cursor.execute(Query,values)
        conn.commit()
        print(cursor.rowcount,'rows inserted.')

        #to show users all transactions(including last transaction) in table on Mini statement frame.
        Query = "select * from transactions where Email='{user}'".format(user=currentUser)
        cursor.execute(Query)
        records = cursor.fetchall()
        print("Total number of row in transactions: ", cursor.rowcount)

        for i in table.get_children():
            table.delete(i)

        for row in records:
            table.insert('','end',values=row)

        Frame.tkraise(f5)

    else:
        pass


#-------------------------------GUI COADING START HERE--------------------------------

#LOG IN FRAME
f2=Frame(root, width=1200, height=700, bg="#c6e2ff")
f2_inner=Frame(f2, width=400, height=400, borderwidth=2, relief="ridge", bg="#5677fc")

userid=StringVar()
password=StringVar()

Label(f2_inner,text="LOGIN PAGE", font='lucida 15 bold', bg="#5677fc",fg="white").place(x=140, y=30)

Label(f2_inner,text="Enter your a/c number", font='lucida 8 bold', bg="#5677fc").place(x=75, y=80)
Entry(f2_inner, textvariable=userid,  font='lucida 18 ').place(x=75, y=100)

Label(f2_inner,text="Enter your pasword", font='lucida 8 bold', bg="#5677fc").place(x=75, y=150)
password1=StringVar()
Entry(f2_inner, textvariable=password1, font='lucida 18 ',).place(x=75, y=170)

Button(f2_inner,text="LOG IN TO MY ACCOUNT", font='lucida 10 bold', padx=5, pady=5, width=31,command=lambda: click("login")).place(x=75, y=220)

Label(f2_inner,text="Note: if u dont have bank a/c plz create here", font='lucida 8 bold', bg="#5677fc").place(x=75, y=300)
Button(f2_inner,text="CREATE NEW ACCOUNT?", font='lucida 10 bold',padx=5, pady=5, width=31,command=lambda: click("f3")).place(x=75, y=325)

f2_inner.place(x=400, y=150)
f2.place(x=0,y=0)


#REGISTRATION FRAME
f3=Frame(root, width=1200, height=700, bg="#c6e2ff")
f3_inner=Frame(f3, width=600, height=600, borderwidth=2, relief="ridge", bg="#5677fc")

Name=StringVar()
Adress=StringVar()
Email=StringVar()
Gender=StringVar()
PhoneNumber=StringVar()
AcType=StringVar()
PanNumber=StringVar()
Password=StringVar()

Label(f3_inner,text="REGISTRATION FORM", font='lucida 15 bold', bg="#5677fc",fg="white").place(x=180, y=30)

Label(f3_inner,text="Enter your Full Name", font='lucida 11 bold', bg="#5677fc").place(x=50, y=100)
Entry(f3_inner, textvariable=Name,  font='lucida 18 ').place(x=280, y=100)

Label(f3_inner,text="Enter your Adress", font='lucida 11 bold', bg="#5677fc").place(x=50, y=150)
Entry(f3_inner, textvariable=Adress,  font='lucida 18 ').place(x=280, y=150)

Label(f3_inner,text="Enter Email id", font='lucida 11 bold', bg="#5677fc").place(x=50, y=200)
Entry(f3_inner, textvariable=Email,  font='lucida 18 ').place(x=280, y=200)

Label(f3_inner, text="Select Gender", font='lucida 11 bold', bg="#5677fc").place(x=50, y=250)
Gender.set("male")
Radiobutton(f3_inner,text="Male", variable=Gender, value="male",bg="#5677fc").place(x=280,y=250)
Radiobutton(f3_inner,text="Female", variable=Gender, value="female",bg="#5677fc").place(x=430,y=250)


Label(f3_inner,text="Enter your Mobile Number", font='lucida 11 bold', bg="#5677fc").place(x=50, y=300)
Entry(f3_inner, textvariable=PhoneNumber,  font='lucida 18 ').place(x=280, y=300)

Label(f3_inner, text="Choose Account Type", font='lucida 11 bold', bg="#5677fc").place(x=50, y=350)
AcType.set("saving")
Radiobutton(f3_inner,text="saving", variable=AcType, value="saving",bg="#5677fc").place(x=280,y=350)
Radiobutton(f3_inner,text="current", variable=AcType, value="current",bg="#5677fc").place(x=430,y=350)

Label(f3_inner,text="Enter your Pan Number", font='lucida 11 bold', bg="#5677fc").place(x=50, y=400)
Entry(f3_inner, textvariable=PanNumber,  font='lucida 18 ').place(x=280, y=400)

Label(f3_inner,text="Set Password to account", font='lucida 11 bold', bg="#5677fc").place(x=50, y=450)
Entry(f3_inner, textvariable=Password,  font='lucida 18 ').place(x=280, y=450)

Button(f3_inner,text="SUBMIT", font='lucida 12 bold', padx=5, pady=5, width=20,command=lambda: click("register")).place(x=200, y=500)

f3_inner.place(x=300, y=50)
f3.place(x=0,y=0)


#TRANSACTIONS FRAME
f4=Frame(root, width=1200, height=700, bg="#c6e2ff")
f4_inner=Frame(f4, width=600, height=600, borderwidth=2, relief="ridge", bg="#5677fc")

img1 = Image.open("logo.jpg")
photo1 = ImageTk.PhotoImage(img1)
Label(f4_inner,image=photo1).place(x=100, y=30)

Label(f4_inner, text="Your A/C Balance Is Rupees :", bg="#5677fc", font='lucida 12 bold').place(x=100,y=250)
balanceForF4Label=StringVar()
Label(f4_inner, text="", textvariable=balanceForF4Label, bg="#5677fc", font='lucida 12 bold',fg="white").place(x=330,y=250)

Label(f4_inner, text="Choose transaction from bellow..", font='lucida 12 bold', bg="#5677fc",fg="white" ).place(x=100, y=300)
r1=StringVar()
r1.set("credit")
Radiobutton(f4_inner,text="DEPOSIT MONEY", variable=r1, value="credit").place(x=100,y=350)
Radiobutton(f4_inner,text="WITHDRAWLS", variable=r1, value="debit").place(x=300,y=350)

Label(f4_inner,text="Enter Amount To Credit/Debit :",bg="#5677fc").place(x=100,y=400)
enterAmount=StringVar()
Entry(f4_inner, textvariable=enterAmount, font='lucida 12 ').place(x=300, y=400)

Button(f4_inner,text="SUBMIT", font='lucida 12 bold', padx=15, pady=3, command=lambda: click("updateBalance")).place(x=200, y=480)

f4_inner.place(x=300, y=50)
f4.place(x=0,y=0)


# MINI STATEMENT FRAME
f5=Frame(root, width=1200, height=700, bg="#c6e2ff")
f5_inner=Frame(f5, width=1100, height=600, borderwidth=2, relief="ridge", bg="#5677fc")

Label(f5_inner, text="TOTAL BALANCE  =", bg="#5677fc", font='lucida 16 bold',fg="white").place(x=350,y=30)
balanceForF5Label=StringVar()
Label(f5_inner, text="", textvariable=balanceForF5Label, bg="#5677fc", font='lucida 16 bold',fg="white").place(x=560,y=30)

Label(f5_inner, text="MINI STATEMENT", font='lucida 14 bold', bg="#5677fc").place(x=430, y=100)

table=ttk.Treeview( f5_inner, columns=(1,2,3,4,5), show="headings", height=15 )
table.place(x=50,y=150)

table.heading(1,text="Email")
table.heading(2,text="Transaction Date")
table.heading(3,text="Transaction Type")
table.heading(4,text="Amount")
table.heading(5,text="Total Available Balance")


Button(f5_inner,text="CLICK HERE FOR MORE TRANSACTION ", font='lucida 10 bold',padx=10, pady=5, width=30, command=lambda: click("f4")).place(x=250, y=500)
Button(f5_inner,text="EXIT", font='lucida 10 bold', padx=10, pady=5, width=30, command=lambda: click("f6")).place(x=600, y=500)

f5_inner.place(x=50, y=50)
f5.place(x=0,y=0)


# THANK YOU FRAME
f6=Frame(root, width=1200, height=700, bg="#c6e2ff")
f6_inner=Frame(f6, width=800, height=400, borderwidth=2, relief="ridge", bg="#5677fc")

Label(f6_inner, text="Thank You For using our service", font='lucida 30 bold', bg="#5677fc",fg="#18dd11" ).place(x=100, y=100)
Button(f6_inner,text="CLOSE APLLICATION.", font='lucida 10 bold', borderwidth=2, relief="solid", padx=10, pady=5, bg="#5677fc",fg="white", width=30, command=quit).place(x=250, y=200)
f6_inner.place(x=200, y=150)
f6.place(x=0,y=0)


# WELCOME FRAME
f1=Frame(root, width=1200, height=700, bg="#c6e2ff", )
Label(f1, text="WELCOME TO", font='lucida 20 bold', bg="#c6e2ff",fg="#0a6b0c" ).place(x=500, y=100)
Label(f1, text="BANK OF MAHARASHTRA", font='Sentinel 30 bold', bg="#c6e2ff",fg="#075a08" ).place(x=350, y=150)
Button(f1, text="click here to continue..", font='lucida 10 bold', bg="#c6e2ff",command=lambda: click("f2")).place(x=900, y=600)

img = Image.open("bank.jpg")
photo = ImageTk.PhotoImage(img)
Label(f1,image=photo).place(x=350, y=250)
f1.place(x=0,y=0)


root.mainloop()