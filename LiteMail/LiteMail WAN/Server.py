import sqlite3
from socket import *
import time
import struct
from threading import Thread
from time import ctime

Succ = "logged in"
Fail = "unlogged"
MailSuccess = "EMAIL SENT SUCCESSFULLY !! "
Reg = "REGISTERED SUCCESSFULLY !! "

def serviceRequest(connectionSocket):
    db = sqlite3.connect("app.db")
    cr = db.cursor()

    print(f"New Connection Joined At: {ctime()}") 

    while 1:
        signup_flag = connectionSocket.recv(2048).decode("utf-8")

        if signup_flag == '1':   

            while(1):

                try:
                    flag_invalid_sign ='0'
                    email = connectionSocket.recv(2048).decode("utf-8")
                    password = connectionSocket.recv(2048).decode("utf-8")

                    if email.endswith('@litemail.com') and len(password) >= 8:
                        cr.execute("INSERT INTO users (email, password) VALUES (?, ?)", (email, password))
                        db.commit()
                        connectionSocket.send(bytes(flag_invalid_sign, "utf-8"))
                        break
                    else:
                        flag_invalid_sign ='1'
                        connectionSocket.send(bytes(flag_invalid_sign, "utf-8"))
                
                except Exception as e:
                    flag_invalid_sign ='1'
                    connectionSocket.send(bytes(flag_invalid_sign, "utf-8"))

            flag_null= '1'
            connectionSocket.send(bytes(flag_null, "utf-8"))
            flag_content_message = connectionSocket.recv(2048).decode("utf-8")

            if flag_content_message == 'content':
                To = connectionSocket.recv(2048).decode("utf-8")
                email = connectionSocket.recv(2048).decode("utf-8")
                Subject = connectionSocket.recv(2048).decode("utf-8")
                Message = connectionSocket.recv(2048).decode("utf-8")
                content = connectionSocket.recv(1000000)
                filename = connectionSocket.recv(2048).decode("utf-8")
                cr.execute("insert into maildata values (?,?,?,?,?,?) ",
                            (To, email, Subject,  Message, content, filename))
                db.commit()

            elif flag_content_message == 'no content':
                extra1 = b'NULL'
                extra2 = "NULL"
                To = connectionSocket.recv(2048).decode("utf-8")
                email = connectionSocket.recv(2048).decode("utf-8")
                Subject = connectionSocket.recv(2048).decode("utf-8")
                Message = connectionSocket.recv(2048).decode("utf-8")
                cr.execute("insert into maildata values (?,?,?,?,?,?) ",
                            (To, email, Subject,  Message, extra1, extra2))
                db.commit()

        elif signup_flag == '0':
            email = connectionSocket.recv(2048).decode("utf-8")
            password = connectionSocket.recv(2048).decode("utf-8")
            print(f"Received :  {email} , {password}")

            cr.execute(
                    "SELECT email, password FROM users WHERE email=? AND password=?", (email, password))

            row = (cr.fetchone())

            if row is not None:
                connectionSocket.send(bytes(Succ, "utf-8"))
                cr.execute( "SELECT sender , subject , message , data , filename FROM maildata where rec=?", (email,))
                rows = cr.fetchall()
                senders = []
                subjects = []
                messages = []
                datas = []
                filenames = []

                row_count = int(len(rows))
                encoded_row_count = struct.pack('!i', row_count)
                connectionSocket.send(encoded_row_count)
                time.sleep(5)

                for row in rows:
                    sender, subject, message, data , filename = row
                    senders.append(sender)
                    subjects.append(subject)
                    messages.append(message)
                    datas.append(data)
                    filenames.append(filename)

                if(senders and subjects and messages and datas and filenames):
                    flag_null ='0'
                    connectionSocket.send(bytes(flag_null, "utf-8"))
                    time.sleep(5)
                    connectionSocket.send(bytes("\n".join(senders), "utf-8"))
                    time.sleep(5)
                    connectionSocket.send(bytes("\n".join(subjects), "utf-8"))
                    time.sleep(5)
                    connectionSocket.send(bytes("\n".join(messages), "utf-8"))
                    time.sleep(5)

                    c = 0
                    while (c < row_count):
                        datas[c]
                        connectionSocket.send(datas[c])
                        time.sleep(5)
                        c += 1
                    time.sleep(5)
                    connectionSocket.send(bytes("\n".join(filenames), "utf-8"))
                    time.sleep(5)

                else:
                    flag_null= '1'
                    connectionSocket.send(bytes(flag_null, "utf-8"))
                flag_content_message = connectionSocket.recv(2048).decode("utf-8")
               
                if flag_content_message == 'content':
                    To = connectionSocket.recv(2048).decode("utf-8")
                    email = connectionSocket.recv(2048).decode("utf-8")
                    Subject = connectionSocket.recv(2048).decode("utf-8")
                    Message = connectionSocket.recv(2048).decode("utf-8")
                    content = connectionSocket.recv(1000000)
                    filename = connectionSocket.recv(2048).decode("utf-8")
                    cr.execute("insert into maildata values (?,?,?,?,?,?) ",
                                (To, email, Subject,  Message, content, filename))
                    db.commit()

                elif flag_content_message == 'no content':
                    extra1 = b'NULL'
                    extra2 = "NULL"
                    To = connectionSocket.recv(2048).decode("utf-8")
                    email = connectionSocket.recv(2048).decode("utf-8")
                    Subject = connectionSocket.recv(2048).decode("utf-8")
                    Message = connectionSocket.recv(2048).decode("utf-8")
                    cr.execute("insert into maildata values (?,?,?,?,?,?) ",
                                (To, email, Subject,  Message, extra1, extra2))
                    db.commit()
            
            else:
                connectionSocket.send(bytes(Fail, "utf-8"))

serverIP = "localhost"
serverPort = 12348

serverSocket = socket(AF_INET, SOCK_STREAM)
serverSocket.bind((serverIP, serverPort))
serverSocket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)

print('[SERVER] UP AND RUNINNNNN . . . . . . . ')

threads = []
serverSocket.listen(40)

while True:
    connectionSocket, client_address = serverSocket.accept()
    print(f"Client Joined From: {client_address}")
    newThread = Thread(target=serviceRequest, args=(connectionSocket,))
    newThread.start()
    threads.append(newThread)
