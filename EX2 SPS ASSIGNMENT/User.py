import smtplib, hashlib, random

#Global Constant Declarations
SENDER_EMAIL = 'tempforproject2@gmail.com'
SERVER = smtplib.SMTP('smtp.gmail.com',587)

# --- Dictionary containing keys and values that consist of list of potential replies ---
pybot_responses = { 
    'tell me a joke':["I'm afraid for the calendar. Its days are numbered",
    "Singing in the shower is fun until you get soap in your mouth. Then it's a soap opera.",
    'What do you call a fish wearing a bowtie? Sofishticated.',
    'I thought the dryer was shrinking my clothes. Turns out it was the refrigerator all along.'],

    'greeting':['Hey, there! Ask me a question','Hi, ask me a question', 'Hello :), ask me a question', 'Yo, ask me a question'],
    'how are you':['Im great!', 'I am a computer so who knows!', "I'm pretty tired right now", "I'm happy!"],
    'who created you':['Joe did'],
    'whats your name':['Jerry the pyhton bot']
}
# --- functions to handle user requests ---
def pybot_response(response): #defining function with response argument, will be used to generate response to argument value
    response = response.lower() #set parameter yo lower case to remove case sensitivity
    if True in list(map(lambda x: response in x ,pybot_responses.keys())):#checks if the characters in the parameter is in one of the values within the lists within the dictionary
        return pybot_responses[response][random.randint(0,len(pybot_responses[response])-1)] #retreive the response from the dictionary
    else:
        return ("I'm not sure how to respond to that.") #return default statement

def verify(email,password): #defining function with parameters 'email' and 'password'
    #Local Vatiables referencing Objects declaration

    pass_hash = hashlib.new('sha256')
    email_hash = hashlib.new('sha256')

    #Creating local class instances to read text files
    emails = open('emails.txt', 'r')
    passwords = open('passwords.txt', 'r')

    emaillist = []
    passwordlist = []

    #calling hash object method and updating objects attributes
    pass_hash.update((password).encode())
    email_hash.update((email).encode())
    for password in passwords: #will loop through each line in the file 'passwords.txt'
        passwordlist.append(password.rstrip('\n')) #add each line to passwords list local variable sttripping whitespsce and break line characcters


    for email in emails: #repeat of loop above
        emaillist.append(email.rstrip('\n'))

    if ((email_hash.hexdigest() in emaillist) and (pass_hash.hexdigest() in passwordlist)): #are the hashed parameters stored in the local variable containing emails and password
        emails.close(),passwords.close() #close the files and save rescources as there is a memory leak if not closed
        return True #return boolean value True to confirm the parameters have been verified and are ocntianed in the 'emails.txt' & 'passwords.txt' files
    
    emails.close(),passwords.close() #close the files and save rescources as there is a memory leak if not closed
    return False #return boolean value False to confirm the parameters have not been verified and are not contianed in the 'emails.txt' & 'passwords.txt' files

def send_otp(email): #defining function with parameters 'email'
    global otp #set otp local variable as global
    otp = ''.join([str(random.randint(1,9)) for i in range(5)]) #One time password, series of psuedorandom integers
    SERVER.starttls() #use server object to begin loading virtual machine server using smtplib library
    SERVER.login(SENDER_EMAIL, 'mkbjvnpaqckszzso') #use the 'login()' method with parameters for log-in details to gmail api#

    try: #Error handling
        SERVER.sendmail(SENDER_EMAIL, email, f'Your unique OTP (One Time Password) is {otp}') #sned an emial using the mail server with the paramters specified
        return True #return boolean value True 
    except:
        return False #ERROR handling

def new_account(email,password,input_otp):

    #Local Vatiables referencing Objects declaration
    pass_hash = hashlib.new('sha256')
    email_hash = hashlib.new('sha256')

    pass_hash.update((password).encode())
    email_hash.update((email).encode())

    for i in range(3): #for loop that will iterate over code below three times
        if input_otp == otp: #check if paramter is equal to otp
            emails = open('emails.txt','a') #open the file 'emails.txt' with append parameter so it can be written to
            emails.write(email_hash.hexdigest()+'\n') #write the parameter to 'email.txt'
            emails.close() #close the file to save rescources

            passwords = open('passwords.txt','a') #open the file 'passwords.txt' with append parameter so it can be written to
            passwords.write(pass_hash.hexdigest()+'\n') ##write the parameter to 'email.txt'
            passwords.close() #close the file to save rescources

            return True
            
    return False

    
