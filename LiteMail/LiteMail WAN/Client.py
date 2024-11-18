import tkinter
import customtkinter
from PIL import ImageTk,Image
from tkinter import messagebox
from CTkMessagebox import CTkMessagebox
from customtkinter import *
import sqlite3
from socket import *
import time
import struct
from tkinter import filedialog
import os
from tkinter import filedialog
from tkinter import Tk

serverIP = "143.42.50.70"
serverPort = 12348
clientSocket = socket(AF_INET, SOCK_STREAM)
clientSocket.connect((serverIP, serverPort))

customtkinter.set_appearance_mode("System")  
customtkinter.set_default_color_theme("green")  

condition = ''
flag = 1
home_flag = 0

app = customtkinter.CTk() 
app.geometry("600x440")
app.title('Login')

app2 = customtkinter.CTk()  
app2.geometry("600x440")
app2.title('Sign Up')    

sign = customtkinter.CTk()  
sign.geometry("600x440")
sign.title('Sign Up')
 
NewEmail = customtkinter.CTk()
NewEmail.geometry("600x440")
NewEmail.title('NewEmail')

client = customtkinter.CTk()  
client.geometry("600x440")
client.title('Mails')

email = customtkinter.CTk()
email.geometry("600x440")
email.title('Email')

sign2 = customtkinter.CTk()  
sign2.geometry("600x440")
sign2.title('Sign Up')

def login_action(email, password):
        global condition
        global flag
        global signup_flag
        signup_flag = '0'
        clientSocket.send(bytes(signup_flag, "utf-8"))
        time.sleep(5)
        clientSocket.send(bytes(email, "utf-8"))
        time.sleep(5)
        clientSocket.send(bytes(password, "utf-8"))

        condition = clientSocket.recv(2048).decode("utf-8")
        if(condition == "logged in"):
            clientpageL(email , password)
        elif(condition == "unlogged"):
            homepage("invalid")

def convert_content_binary(filename_up):
    filename = filename_up[0]
    global filename_str
    global filename_with_extension
    filename_str = str(filename)
    filename_with_extension = os.path.basename(filename_str)
    with open(filename_str, 'rb') as file:
        data_for_upload = file.read()
    return data_for_upload

def upload_attachment():
      global NewEmail
      global get_filename
      global get_content
      get_filename = filedialog.askopenfilenames(title="Select Attachment", filetypes=( ("png", ".png"), ("jpg" , ".jpg"), ("rar" , ".rar"), ("txt" , ".txt") , ("Allfile", ".")))
      get_content   = convert_content_binary(get_filename)
      CTkMessagebox(title="Attachment", message="Attachment Uploaded Successfully", icon="check")

def new_email_to_database_without_attach(to , email , subject , message ):
        global NewEmail
        clientSocket.send(bytes('no content', "utf-8"))
        clientSocket.send(bytes(to, "utf-8"))
        time.sleep(5)
        clientSocket.send(bytes(email, "utf-8"))
        time.sleep(5)
        clientSocket.send(bytes(subject, "utf-8"))
        time.sleep(5)
        clientSocket.send(bytes(message, "utf-8"))
        time.sleep(5)
        CTkMessagebox(title="Email", message="Email Sent Successfully", icon="check")

def new_email_to_database(to , email , subject , message , content , filename):
        global NewEmail
        clientSocket.send(bytes('content', "utf-8"))
        clientSocket.send(bytes(to, "utf-8"))
        time.sleep(5)
        clientSocket.send(bytes(email, "utf-8"))
        time.sleep(5)
        clientSocket.send(bytes(subject, "utf-8"))
        time.sleep(5)
        clientSocket.send(bytes(message, "utf-8"))
        time.sleep(5)
        clientSocket.send(content)
        time.sleep(5)
        clientSocket.send(bytes(filename_with_extension, "utf-8"))
        time.sleep(5)
        CTkMessagebox(title="Email", message="Email Sent Successfully", icon="check")

def send_email(email):
    global client
    global content
    global get_content
    global get_filename
    get_filename = 'filename'
    get_content = b''
    client.destroy()
    NewEmail = customtkinter.CTk()
    NewEmail.geometry("600x440")
    NewEmail.title('NewEmail')

    frame = customtkinter.CTkFrame(master=NewEmail, width=320, height=360, corner_radius=15)
    frame.place(relx=0.5, rely=0.5, anchor=tkinter.CENTER)

    l2 = customtkinter.CTkLabel(master=frame, text="To: ", font=('Century Gothic', 12))
    l2.place(x=20, y=20)

    ToEntry = customtkinter.CTkEntry(master=frame, width=220, placeholder_text='', fg_color="transparent", border_color="#3b3a3a", border_width=1 , corner_radius=20)
    ToEntry.place(x=75, y=20)

    l3 = customtkinter.CTkLabel(master=frame, text="From: ", font=('Century Gothic', 12))
    l3.place(x=20, y=70)

    fromm = customtkinter.CTkLabel(master=frame, text=email, font=('Century Gothic', 12))
    fromm.place(x=75, y=70)

    l3 = customtkinter.CTkLabel(master=frame, text="Subject: ", font=('Century Gothic', 12))
    l3.place(x=20, y=120)

    SubEntry = customtkinter.CTkEntry(master=frame, width=220, placeholder_text='', fg_color="transparent", border_color="#3b3a3a", border_width=1 , corner_radius=20)
    SubEntry.place(x=75, y=120)

    l3 = customtkinter.CTkLabel(master=frame, text="Compose Email: ", font=('Century Gothic', 12))
    l3.place(x=20, y=160)

    textbox = customtkinter.CTkTextbox(master=frame, height=150, width= 285, fg_color="transparent", border_color="#3b3a3a", border_width=1)
    textbox.place(x=15, y=190)

    attachment=ImageTk.PhotoImage(Image.open("Images\\attachment.png").resize((30,30), Image.ANTIALIAS))
    attachment_btn= customtkinter.CTkButton(master=frame, image=attachment, text="" , width=50, height=20, fg_color="transparent" , hover_color="#1e1f1e" ,compound="left", command=lambda: upload_attachment())
    attachment_btn.place(x=240, y=300)

    send=ImageTk.PhotoImage(Image.open("Images\\send2.png").resize((30,30), Image.ANTIALIAS))
    send_btn= customtkinter.CTkButton(master=NewEmail, image=send, text="" , width=50, height=20, fg_color="transparent" , hover_color="#1e1f1e" ,compound="left", command=lambda: new_email_to_database(ToEntry.get() , email , SubEntry.get() , textbox.get(1.0 , END) , get_content, get_filename) if get_filename!= 'filename' else new_email_to_database_without_attach(ToEntry.get() , email , SubEntry.get() , textbox.get(1.0 , END) ))
    send_btn.place(x=520 , y=400)

    NewEmail.mainloop()

def download_attachment(content , filename):
    if filename != "NULL":
        root = Tk()
        root.withdraw()
        file_path = filedialog.asksaveasfilename(initialfile=filename)
        if file_path:
            with open(file_path, 'wb') as f:
                time.sleep(5)
                f.write(content)
                time.sleep(5)
                CTkMessagebox(title="Attachment", message="Attachment Downloaded Successfully" , icon="check")


def viewemail(sender, subject , message , content , filename):
    global client
    client.destroy()
    global email
    email = customtkinter.CTk()
    email.geometry("600x440")
    email.title('Email')
    frame = customtkinter.CTkFrame(master=email, width=320, height=360, corner_radius=15)
    frame.place(relx=0.5, rely=0.5, anchor=tkinter.CENTER)

    l3 = customtkinter.CTkLabel(master=frame, text="From:        " + sender, font=('Century Gothic', 12))
    l3.place(x=20, y=20)

    l3 = customtkinter.CTkLabel(master=frame, text="Subject: " + subject, font=('Century Gothic', 12))
    l3.place(x=20, y=70)

    frame2 = customtkinter.CTkFrame(master=email, width=285, height=220 , fg_color="transparent", border_color="#3b3a3a" , corner_radius=20)
    frame2.place(x=157, y=160)
    l4 = customtkinter.CTkLabel(master=frame2, height=170, width= 285, fg_color="transparent" , text="" + message , corner_radius=20, anchor="nw")
    l4.place(x=0 , y=10)
    
    frame3 = customtkinter.CTkFrame(master=frame2, width=285, height=35 , fg_color="#363636", border_color="#3b3a3a",corner_radius=0)
    frame3.place(x=0, y=190)

    if filename!='NULL':
         btn5 = customtkinter.CTkLabel(master=frame3, height=20, width= 200, fg_color="transparent" , text="Attachment: "+filename, anchor="w", font=('Century Gothic', 12))
         btn5.place(x=5 , y=5)
    
    download=ImageTk.PhotoImage(Image.open("Images\\download.png").resize((25,25), Image.ANTIALIAS))
    download= customtkinter.CTkButton(master=frame3, image=download, text="" , width=30, height=20, fg_color="transparent" , hover_color="#1e1f1e" ,compound="left" , command= lambda: download_attachment(content , filename))
    download.place(x=250, y=1)

    email.mainloop()

def clientpageL(email, password):
    global app
    global app2
    global NewEmail
    global home_flag
    if(home_flag == 0):
        app.destroy()
    elif(home_flag == 1):
        app2.destroy()

    row_count = clientSocket.recv(4)

    decoded_row_count = struct.unpack('!i', row_count)[0]

    flag_null = clientSocket.recv(2048).decode("utf-8")
    
    if flag_null == '0':      
        senders = clientSocket.recv(2048).decode("utf-8")   
        subjects = clientSocket.recv(2048).decode("utf-8")
        messages = clientSocket.recv(2048).decode("utf-8")
        datas = []
        c = 0

        while (c < decoded_row_count):
            data = clientSocket.recv(1000000)
            datas.append(data)
            c += 1
        filenames = clientSocket.recv(2048).decode("utf-8")

        global client        
        client = customtkinter.CTk()
        client.geometry("600x440")
        client.title("Emails")
        client.wm_attributes('-transparent' , '#60b26c')

        welcome_label=customtkinter.CTkLabel(master=client, text="Welcome: "+email,font=('Century Gothic',12))
        welcome_label.place(x=30, y=15)

        l2=customtkinter.CTkLabel(master=client, text="Inbox",font=('Century Gothic',20))
        l2.place(x=280, y=15 )

        scrollable_frame = customtkinter.CTkScrollableFrame(client, width=300, height=320)
        scrollable_frame.place(relx=0.5, rely=0.5, anchor=tkinter.CENTER)

        sender_list = senders.split("\n")
        subject_list = subjects.split("\n")
        message_list = messages.split("\n")
        filename_list = filenames.split("\n")
        
        for i, sender in enumerate(sender_list):
            def create_lambda_function(s=sender, subj=subject_list[i], msg=message_list[i], content=datas[i] , fname=filename_list[i]):
                return lambda: viewemail(s, subj, msg, content , fname)
            
            email_button = customtkinter.CTkButton(
                master=scrollable_frame,
                fg_color="transparent",
                text="From: " + sender,
                command=create_lambda_function(),
                corner_radius=20,
                hover_color='#252625'
            )
            email_button.pack(pady=20)
            
            line = tkinter.Canvas(
                master=scrollable_frame,
                width=600,
                height=0,
                bg='#3b3a3a',
                highlightbackground='#252625',
                borderwidth=0.1,
                highlightthickness=0
            )
            line.create_line(0, 0, email_button.winfo_width(), 0)
            line.pack()

        compose=ImageTk.PhotoImage(Image.open("Images\\composee.png").resize((40,40), Image.ANTIALIAS))
        compose_btn= customtkinter.CTkButton(master=client, text="" , image=compose, width=50, height=20, fg_color="transparent" , hover_color="#1e1f1e" ,compound="left" , command=lambda: send_email(email) )
        compose_btn.place(x=520, y=370)

        client.mainloop()

    if flag_null == '1':

        client = customtkinter.CTk()
        client.geometry("600x440")
        client.title("Emails")
        client.wm_attributes('-transparent' , '#60b26c')

        welcome_label=customtkinter.CTkLabel(master=client, text="Welcome: "+email,font=('Century Gothic',12))
        welcome_label.place(x=30, y=15)

        l2=customtkinter.CTkLabel(master=client, text="Inbox",font=('Century Gothic',20))
        l2.place(x=280, y=15 )

        nomail_frame = customtkinter.CTkFrame(client, width=300, height=320)
        nomail_frame.place(relx=0.5, rely=0.5, anchor=tkinter.CENTER)
       
        nomail=customtkinter.CTkLabel(master=nomail_frame, text="No Mails Available", font=('Century Gothic',20) )
        nomail.place(x=60, y=105 )

        compose=ImageTk.PhotoImage(Image.open("Images\\composee.png").resize((40,40), Image.ANTIALIAS))
        compose_btn= customtkinter.CTkButton(master=client, text="" , image=compose, width=50, height=20, fg_color="transparent" , hover_color="#1e1f1e" ,compound="left" , command=lambda: send_email(email) )
        compose_btn.place(x=520, y=370)

        client.mainloop()

def clientpageS(email):
    global NewEmail
    global sign
    global sign2
    global from_sign_window
    global client

    if from_sign_window == 'sign':
        sign.destroy()
    elif from_sign_window == "sign2":
        sign2.destroy()

    client = customtkinter.CTk()
    client.geometry("600x440")
    client.title("Emails")
    client.wm_attributes('-transparent' , '#60b26c')

    welcome_label=customtkinter.CTkLabel(master=client, text="Welcome: "+email,font=('Century Gothic',12))
    welcome_label.place(x=30, y=15)

    l2=customtkinter.CTkLabel(master=client, text="Inbox",font=('Century Gothic',20))
    l2.place(x=280, y=15 )

    nomail_frame = customtkinter.CTkFrame(client, width=300, height=320)
    nomail_frame.place(relx=0.5, rely=0.5, anchor=tkinter.CENTER)

    nomail=customtkinter.CTkLabel(master=nomail_frame, text="No Mails Available", font=('Century Gothic',20) )
    nomail.place(x=60, y=105 )

    compose=ImageTk.PhotoImage(Image.open("Images\\composee.png").resize((40,40), Image.ANTIALIAS))
    compose_btn= customtkinter.CTkButton(master=client, text="" , image=compose, width=50, height=20, fg_color="transparent" , hover_color="#1e1f1e" ,compound="left" , command=lambda: send_email(email) )
    compose_btn.place(x=520, y=370)

    client.mainloop()

def signup_invalid():
    global signup_flag
    global sign
    global sign2
    global from_sign_window
    from_sign_window = "sign2"
    sign.destroy()  
    sign2 = customtkinter.CTk()  
    sign2.geometry("600x440")
    sign2.title('Sign Up')      
    img1=ImageTk.PhotoImage(Image.open("Images\\test1.jpg"))
    l1=customtkinter.CTkLabel(master=sign2,image=img1)
    l1.pack()

    frame=customtkinter.CTkFrame(master=l1, width=320, height=360, corner_radius=15)
    frame.place(relx=0.5, rely=0.5, anchor=tkinter.CENTER)

    l2=customtkinter.CTkLabel(master=frame, text="Sign Up",font=('Century Gothic',18))
    l2.place(x=125, y=15)

    l6=customtkinter.CTkLabel(master=frame, text="INVALID",font=('Century Gothic',18))
    l6.place(x=120, y=45)

    firstname_entry=customtkinter.CTkEntry(master=frame, width=220, placeholder_text='Firstname')
    firstname_entry.place(x=50, y=85)

    lastname_entry=customtkinter.CTkEntry(master=frame, width=220, placeholder_text='Lastname')
    lastname_entry.place(x=50, y=125)

    email_signup_gui=customtkinter.CTkEntry(master=frame, width=220, placeholder_text='Email')
    email_signup_gui.place(x=50, y=165)

    email_error=customtkinter.CTkLabel(master=frame, text="*Domain must be @litemail.com or Email already Exists",font=('Century Gothic',10))
    email_error.place(x=50, y=195)

    password_signup_gui=customtkinter.CTkEntry(master=frame, width=220, placeholder_text='Password', show="*")
    password_signup_gui.place(x=50, y=225)

    password_error=customtkinter.CTkLabel(master=frame, text="*Password must be at least 8 characters",font=('Century Gothic',10))
    password_error.place(x=50, y=255)

    signup_btn = customtkinter.CTkButton(master=frame, width=100, text="Sign Up", command= lambda: signup_action(email_signup_gui.get(), password_signup_gui.get()), corner_radius=6)
    signup_btn.place(x=110, y=300)

    sign2.mainloop()

def signup_action(email_s , password_s):
        clientSocket.send(bytes(email_s, "utf-8"))
        clientSocket.send(bytes(password_s, "utf-8"))
        flag_invalid_sign = clientSocket.recv(2048).decode("utf-8")
        print(flag_invalid_sign)
        #if email and pass are not in db
        if flag_invalid_sign == '1':
             signup_invalid()
        #if email and pass are in in db
        elif flag_invalid_sign == '0':
             clientpageS(email_s)
             
def signup():
    global signup_flag
    signup_flag = '1'
    clientSocket.send(bytes(signup_flag, "utf-8"))
    global sign
    global from_sign_window
    from_sign_window = "sign"
    app.destroy()  
    sign = customtkinter.CTk()  
    sign.geometry("600x440")
    sign.title('Sign Up')      
    img1=ImageTk.PhotoImage(Image.open("Images\\test1.jpg"))
    l1=customtkinter.CTkLabel(master=sign,image=img1)
    l1.pack()

    frame=customtkinter.CTkFrame(master=l1, width=320, height=360, corner_radius=15)
    frame.place(relx=0.5, rely=0.5, anchor=tkinter.CENTER)

    l2=customtkinter.CTkLabel(master=frame, text="Sign Up",font=('Century Gothic',20))
    l2.place(x=125, y=45)

    firstname_entry=customtkinter.CTkEntry(master=frame, width=220, placeholder_text='Firstname')
    firstname_entry.place(x=50, y=85)

    lastname_entry=customtkinter.CTkEntry(master=frame, width=220, placeholder_text='Lastname')
    lastname_entry.place(x=50, y=125)

    email_signup_gui=customtkinter.CTkEntry(master=frame, width=220, placeholder_text='Email')
    email_signup_gui.place(x=50, y=165)

    email_val=customtkinter.CTkLabel(master=frame, text="*Email must be @litemail.com",font=('Century Gothic',10))
    email_val.place(x=50, y=195)

    password_signup_gui=customtkinter.CTkEntry(master=frame, width=220, placeholder_text='Password', show="*")
    password_signup_gui.place(x=50, y=225)

    password_val=customtkinter.CTkLabel(master=frame, text="*Password must be at least 8 characters",font=('Century Gothic',10))
    password_val.place(x=50, y=255)

    signup_btn = customtkinter.CTkButton(master=frame, width=100, text="Sign Up", command= lambda: signup_action(email_signup_gui.get(), password_signup_gui.get()), corner_radius=6)
    signup_btn.place(x=110, y=300)

    sign.mainloop()
    
def homepage(user):
    if (user == "valid"):
        img1=ImageTk.PhotoImage(Image.open("Images\\test1.jpg"))
        l1=customtkinter.CTkLabel(master=app,image=img1)
        l1.pack()

        frame=customtkinter.CTkFrame(master=l1, width=320, height=360, corner_radius=20 )
        frame.place(relx=0.5, rely=0.5, anchor=tkinter.CENTER)

        l2=customtkinter.CTkLabel(master=frame, text="Log into your Account",font=('Century Gothic',20))
        l2.place(x=50, y=45)

        email_login_gui=customtkinter.CTkEntry(master=frame, width=220, placeholder_text='Email' )
        email_login_gui.place(x=50, y=110)
        
        password_login_gui=customtkinter.CTkEntry(master=frame, width=220, placeholder_text='Password', show="*")
        password_login_gui.place(x=50, y=165)

        login_btn = customtkinter.CTkButton(master=frame, width=100, text="Login", corner_radius=6, hover_color="#252625",
                                   command=lambda: login_action(email_login_gui.get(), password_login_gui.get()))

        login_btn.place(x=110, y=220)

        l3=customtkinter.CTkLabel(master=frame, text="Don't have an account?",font=('Century Gothic',12))
        l3.place(x=90,y=255)

        sign_btn = customtkinter.CTkButton(master=frame, width=100, text="Sign Up Now", command= lambda: signup(), corner_radius=6 ,hover_color="#252625")
        sign_btn.place(x=110, y=290)
        app.mainloop()

    if(user == "invalid"):
        app.destroy()
        global home_flag
        global app2
        home_flag = 1
        app2 = customtkinter.CTk()  
        app2.geometry("600x440")
        app2.title('Sign Up')   

        img1=ImageTk.PhotoImage(Image.open("Images\\test1.jpg"))
        l1=customtkinter.CTkLabel(master=app2,image=img1)
        l1.pack()

        frame=customtkinter.CTkFrame(master=l1, width=320, height=360, corner_radius=20 )
        frame.place(relx=0.5, rely=0.5, anchor=tkinter.CENTER)

        l2=customtkinter.CTkLabel(master=frame, text="Log into your Account",font=('Century Gothic',20))
        l2.place(x=50, y=45)

        email_login_gui=customtkinter.CTkEntry(master=frame, width=220, placeholder_text='Email' )
        email_login_gui.place(x=50, y=110)
        
        password_login_gui=customtkinter.CTkEntry(master=frame, width=220, placeholder_text='Password', show="*")
        password_login_gui.place(x=50, y=165)

        error=customtkinter.CTkLabel(master=frame, text="Invalid Email or Password",font=('Century Gothic',10))
        error.place(x=100, y=195)

        login_btn = customtkinter.CTkButton(master=frame, width=100, text="Login", corner_radius=6, hover_color="#252625",
                                   command=lambda: login_action(email_login_gui.get(), password_login_gui.get()))

        login_btn.place(x=110, y=225)

        app2.mainloop()

homepage("valid")

