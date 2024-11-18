import sqlite3

db = sqlite3.connect("app.db")

# Setting up a cursor
cr = db.cursor()


# CREATING TABLES

cr.execute(
    "CREATE TABLE if not exists maildata (rec VARCHAR, sender VARCHAR, subject VARCHAR, message VARCHAR)")


# ADD ACCOUNTS TO DATABASE

cr.execute("insert into users values ('honda@gmail.com',12345)")

# Saving changes
db.commit()

# db = sqlite3.connect("app.db")
# cr = db.cursor()

# # email = input('Please Enter Your Email : \n')
# # password = input('Please Enter Your Password : \n')

# cr.execute(
#     "SELECT email, password FROM users WHERE email=? AND password=?", (email, password))

# row = (cr.fetchone())

# if row is not None:

#     db_email, db_password = row
#     print(f"Login Successfull !\nWelcome : {db_email}  ")

# else:
#     print("Login Failed ! ")
