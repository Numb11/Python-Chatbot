from User import *
from nicegui import *
import datetime
from GPT_API import *
import  asyncio



@ui.page('/home') #Specify page, any ui content below is displayed on this page
def home(): #function to contain the elemnts of the page

# --- Verification functions ---

    def log_in_press(email,password): #function that handles a log in request
        global auth #required to ensure unauthroised access isn't granted if the directory is changed to '/chat'
        ui.notify('Attempting connection to server...') #notify the user that the program is establishing server connection and authorising
        if verify(email,password): #checks if the users details have been verified using the verify function within 'User.py'
            ui.notify('Succesfully Authentichated!') #notify the user that they have been authenticated and allowed to proceed
            auth = True #update the global variable auth so the user can progress
            ui.open(chat) #change the direcotry by appending '/chat' this will run the chat function 
        else:
            ui.notify('Please try again') #notify the user to retry inputting their details


    def new_acc_press(email,password): #function that handles a new account request
        ui.notify('An email is being sent containing a password (OTP)') #notify the user that an email has been sent to the specified email contianing a password
        if not send_otp(email): #negation of the 'send_otp' function, this function is imported from 'User.py' it will send an email with an otp, returns boolean value
            ui.notify('Email could not be sent, please retry') #notify the user that the email has not been successfully sent and they should review their details
            return None
        
        #--- Creation of new input container, styled using tailwind ---

        with ui.grid(rows = 3).classes('place-self-center'): #creatipn of grid for styling purposes
            otp_inp = ui.input('OTP') #create the input container using the input method of the NiceGui class
            ui.button('Confirm', on_click=lambda: otp_press(email,password,otp_inp.value)).classes('bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded') #create and style an input area using NiceGui methods and tailwind styling


    def otp_press(email,password,otp_input): #function to handle OTP input, it is called in reposnse to the 'otp_inp' button being clicked
        if new_account(email,password,otp_input): #if the new_account duntion return True, takes as parameter the OTP,email and password which is then verified and saved
            log_in_press(email,password) #Emulates a log in press so that the data can be verified
        else: #if the statement is False or None
            ui.notify('Incorrect details, please try again.') #Notifies the user through the ui object to try again

# --- Styling for the home page ---

    app.add_static_files('/topography','topography') #making the svg file known to the program as a static file directory so it can be accessed throughout

    ui.query('body').style('background-image: url(http://localhost:8080/topography/topography.svg);') #set the page body background to the static file directory

    with ui.grid(rows = 3).classes('place-self-center'): #creation of grid for styling purposes
        ui.image('logo.png').classes('object-fit: contain;') #imports the file 'logo.png' as a page image and displays it containing it within the grid
        email_inp = ui.input('Email') #creates input element using the UI object with the text email, this is assigned to email_inp variable

        pass_inp = ui.input('Password', password = True) #creates input elment using ui class it has the password parameter therefore characters will be hidden

        ui.button('Log-in', on_click=lambda: log_in_press(email_inp.value,pass_inp.value)).classes('bg-blue-500 hover:bg-blue-600 text-white font-bold py-2 px-4 rounded') #creation of button element that runs 'log_in_press()' on command, it is styled using tailwind

        ui.button('Create account', on_click=lambda: new_acc_press(email_inp.value,pass_inp.value)).classes('bg-blue-500 hover:bg-blue-600 text-white font-bold py-2 px-4 rounded') #same line as above however a different command parameter running 'new_acc_press()'

    with email_inp.add_slot('prepend'): #sepcified were to add elments below, specifies to add them at front of 'email_inp' container
        ui.icon('person') #creates an icon that relates to parameter

# --- styling end for home page ---
ui.run(title =  'ChatBot', favicon = '🗣') #run method called for ui object, will now run the HTML and CSS above

global auth #declaring variable as global so it can be accessed throughout
auth = False #initializing variable as False
home() #run the home function containing the styling for the home page

@ui.page('/chat') #decorator, anything after is visible only in this directory '/chat'


def chat(): #this is the main function that willl contain the elemnts of the page, this function is ran by line 70
    if not auth: #checks if the 'auth' variable is True
        ui.open(home) #the directory will change to return to the log-in page 'home'
        return #will return None, exiting the function
    
    global message_inp #declaring variable as global so it can be accessed throughout, this will be the message input object so its value can be accessed throughout
    ui.query('body').style('background-image: url(http://localhost:8080/topography/topography.svg);') #set the backgorund image of this page
    with ui.tabs().classes('w-full') as tabs: #styling content below as tabs
        GPT_tab = ui.tab('GPT-Chat') #creation of tab with title 'GPT-Chat'
        python_tab = ui.tab('Python-Chat') #creation of another tab with title 'Python-Chat'
    

    with ui.tab_panels(tabs, value = 2).classes('self-start bg-transparent'): #used to style the tabs in the tab panel, styled so the background is transparent rmeoving the need for import again
        with ui.tab_panel(GPT_tab): #anything below this will relate to the 'GPT_tab' tab object
            ui.label('This chat is still in beta, please be patient with response times, thank you.').classes('text-slate-400') #creation of label notifying user, styled to have a change in colour

            # --- functions to handle messages ---

            '''Unfortunately this library does not have a configurable time out, therefore due to high API response time real time GPT messaging is difficult due to this
                I have implemented multithreading using the asyncio library'''

            async def send_message(message): #multithreading function used to manage the sending of a message
                    event_loop = asyncio.get_event_loop() 
                    reply = event_loop.create_task(get_gpt_reply(message)) #creation of thread this will run the function 'get_gpt_reply()' the object us stored in the reply variable
                    current_time = (str(datetime.datetime.now()).split()[-1]).split('.')[0] #store the current time for time stamp usage
                    with ui.tab_panel(GPT_tab): #specify the location of elments, this will create elemnts in the 'GPT_tab'
                        ui.chat_message(message, #create message element
                        sent=True,
                        stamp= current_time,
                        )


                        try: #exception in case the API can not be contacted
                            reply_val = await(reply) #await the reply thread returning
                        except:
                            reply_val = 'Sorry I didnt understand that, please try again.' 

                        ui.chat_message(reply_val, #create message reply displaying GPT API response
                            name = 'Mr GPT',
                            sent = False,
                            stamp= current_time,
                            )
                        
            async def get_gpt_reply(message): #creation of multi threading function
                return message_reply(message) #returns the response of GPT API using function from 'User.py'

            


            message_inp = ui.input(placeholder='Type a message...', ).props('rounded outlined').style('position: fixed; bottom: 0; width: 90%; left:0; padding:8px;') #Styling and creation of message input container

            ui.button(icon = 'send' ,on_click=lambda: send_message(message_inp.value)).style('position: fixed; bottom: 20px; right:40px;') #creation of button element that will call the 'send_message' function on click


# --- PYTHON Bot ---

        with ui.tab_panel(python_tab): #styling for the 'python_tab'
            message_pyinp = ui.input(placeholder='Type a message...', ).props('rounded outlined').style('position: fixed; bottom: 0; width: 90%; left:0; padding:8px;') #create an input element for messages

            ui.button(icon = 'send' ,on_click=lambda: send_pybot_message(message_pyinp.value)).style('position: fixed; bottom: 20px; right:40px;') #creation of button that when clicked will call the send_pybot_message() function with the input vlaue of the message input element

            ui.chat_message(pybot_response('greeting'), #place message greeting user by calling the pybot_response function
                        sent=True,
                        stamp= (str(datetime.datetime.now()).split()[-1]).split('.')[0],
                        )
            
            def send_pybot_message(message): #function to handle messages in the python tab
                    current_time = (str(datetime.datetime.now()).split()[-1]).split('.')[0] #initializing current time variable with time enabling time stamp
                    with ui.tab_panel(python_tab): #specifying the location of elments below in the 'python_tab'
                        ui.chat_message(message, #creation o fmessage element with the users message
                        sent=True,
                        stamp= current_time,
                        )

                        ui.chat_message(pybot_response(message), #creation of message with response from python bot (pybot_response function call with message parameter)
                            name = 'Py Bot',
                            sent = False,
                            stamp= current_time,
                            )