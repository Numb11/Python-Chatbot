from User import *
from nicegui import *
import datetime
from GPT_API import *
import  asyncio



@ui.page("/home") #Specify page, any ui content below is displayed on this page
def home(): #function to contain the elemnts of the page


    def log_in_press(email,password): #function that handles a log in request
        global auth #required to ensure unauthroised access isn't granted if the directory is changed to '/chat'
        ui.notify("Attempting connection to server...") #notify the user that the program is establishing server connection and authorising
        if verify(email,password): #checks if the users details have been verified using the verify function within 'User.py'
            ui.notify("Succesfully Authentichated!") #notify the user that they have been authenticated and allowed to proceed
            auth = True #update the global variable auth so the user can progress
            ui.open(chat) #change the direcotry by appending '/chat' this will run the chat function 
        else:
            ui.notify("Please try again") #notify the user to retry inputting their details


    def new_acc_press(email,password): #function that handles a new account request
        ui.notify("An email is being sent containing a password (OTP)") #notify the user that an email has been sent to the specified email contianing a password
        if not send_otp(email): #negation of the 'send_otp' function, this function is imported from 'User.py' it will send an email with an otp, returns boolean value
            ui.notify("Email could not be sent, please retry") #notify the user that the email has not been successfully sent and they should review their details
            return None
        
        #--- Creation of new input container, styled using tailwind ---

        with ui.grid(rows = 3).classes('place-self-center'): #create a grid for styling purposes
            otp_inp = ui.input('OTP') #create the input container using the input method of the NiceGui class
            ui.button('Confirm', on_click=lambda: otp_press(email,password,otp_inp.value)).classes('bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded') #create and style an input area using NiceGui methods and tailwind styling


    def otp_press(email,password,otp_input): #function to handle OTP input, it is called in reposnse to the 'otp_inp' button being clicked
        if new_account(email,password,otp_input):
            log_in_press(email,password)
        else:
            ui.notify("Incorrect details, please try again.")

    app.add_static_files('/topography','topography')

    ui.query('body').style('background-image: url(http://localhost:8080/topography/topography.svg);')

    with ui.grid(rows = 3).classes('place-self-center'):   
        title_image =  ui.image('logo.png').classes('object-fit: contain;')
        email_inp = ui.input('Email')

        pass_inp = ui.input('Password', password = True)

        ui.button('Log-in', on_click=lambda: log_in_press(email_inp.value,pass_inp.value)).classes('bg-blue-500 hover:bg-blue-600 text-white font-bold py-2 px-4 rounded')

        ui.button('Create account', on_click=lambda: new_acc_press(email_inp.value,pass_inp.value)).classes('bg-blue-500 hover:bg-blue-600 text-white font-bold py-2 px-4 rounded')

    with email_inp.add_slot("prepend"):
        ui.icon("person")

ui.run(title =  'ChatBot', favicon = '🗣')

global auth
auth = False
home()

@ui.page("/chat")



def chat():
    if not auth:
        ui.open(home)
        return  None
    
    ui.query('body').style('background-image: url(http://localhost:8080/topography/topography.svg);')
    with ui.tabs().classes('w-full') as tabs:
        GPT_tab = ui.tab('GPT-Chat')
        Python_tab = ui.tab('Python-Chat')
    

    with ui.tab_panels(tabs, value = 2).classes('self-start bg-transparent'):
        with ui.tab_panel(GPT_tab):
            ui.label("This chat is still in beta, please be patient with response times, thank you.").classes('text-slate-400')
            async def send_message(message):
                    event_loop = asyncio.get_event_loop()
                    reply = event_loop.create_task(get_gpt_reply(message))
                    current_time = (str(datetime.datetime.now()).split()[-1]).split(".")[0]
                    with ui.tab_panel(GPT_tab):
                        ui.chat_message(message,
                        sent=True,
                        stamp= current_time,
                        )


                        try:
                            reply_val = await(reply)
                        except:
                            reply_val = "Sorry I didnt understand that, please try again."

                        ui.chat_message(reply_val,
                            name = 'Mr GPT',
                            sent = False,
                            stamp= current_time,
                            )
                        
            async def get_gpt_reply(message):
                return message_reply(message)

            


            #Styling and creation of message input container
            global message_inp
            message_inp = ui.input(placeholder='Type a message...', ).props('rounded outlined').style('position: fixed; bottom: 0; width: 90%; left:0; padding:8px;')

            ui.button(icon = 'send' ,on_click=lambda: send_message(message_inp.value)).style('position: fixed; bottom: 20px; right:40px;')

                

            

        with ui.tab_panel(Python_tab):
            ui.label('First tab')
        