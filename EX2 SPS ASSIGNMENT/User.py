import smtplib,hashlib
import time,random
import GPT_API

#Global Constant Declarations
global SENDER_EMAIL,SERVER
SENDER_EMAIL = "tempforproject2@gmail.com"
SERVER = smtplib.SMTP("smtp.gmail.com",587)

def verify(email,password):
    #Local Vatiables referencing Objects declaration

    pass_hash = hashlib.new("sha256")
    email_hash = hashlib.new("sha256")

    #Creating local class instances to read text files
    emails = open("emails.txt", "r")
    passwords = open("passwords.txt", "r")

    emaillist = []
    passwordlist = []

    #calling hash object method and updating objects attributes
    pass_hash.update((password).encode())
    email_hash.update((email).encode())
    for password in passwords:
        passwordlist.append(password.rstrip("\n"))

    for email in emails:
        emaillist.append(email.rstrip("\n"))

    if ((email_hash.hexdigest() in emaillist) and (pass_hash.hexdigest() in passwordlist)):
        emails.close(),passwords.close()
        return True
    else:
        emails.close(),passwords.close()
        return False

def send_otp(email):
    global otp
    otp = "".join([str(random.randint(1,9)) for i in range(5)]) #One time password, series of psuedorandom integers
    SERVER.starttls()
    SERVER.login(SENDER_EMAIL, "mkbjvnpaqckszzso")
    try:
        SERVER.sendmail(SENDER_EMAIL, email, f"Your unique OTP (One Time Password) is {otp}")
        return True
    except:
        return False #ERROR handling

def new_account(email,password,input_otp):

    pass_hash = hashlib.new("sha256")
    email_hash = hashlib.new("sha256")

    pass_hash.update((password).encode())
    email_hash.update((email).encode())

    for i in range(3):
        if input_otp == otp:
            emails = open("emails.txt","a")
            emails.write(email_hash.hexdigest()+"\n")
            emails.close()

            passwords = open("passwords.txt","a")
            passwords.write(pass_hash.hexdigest()+"\n")
            passwords.close()

            return True
            
    return False

    
