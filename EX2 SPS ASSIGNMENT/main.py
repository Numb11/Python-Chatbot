from User import *
from nicegui import *

def log_in_press(email,password):
    ui.notify("Attempting connection to server...")
    if verify(email,password):
        ui.notify("Succesfully Authentichated!")
    else:
        ui.notify("Please try again")

def new_acc_press(email,password):
    print(email)
    ui.notify("Attempting connection to server...")
    if not send_otp(email):
        ui.notify("Please retry")
        return None
    
    #Create new input for OTP
    with ui.grid(rows = 3).classes('place-self-center'):   
        otp_inp = ui.input('OTP')
        ui.button('Confirm', on_click=lambda: otp_press(email,password,otp_inp.value)).classes('bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded')

def otp_press(email,password,otp_input):
    if new_account(email,password,otp_input):
        log_in_press(email,password)
    else:
        ui.notify("please try again")


ui.run(title =  'TalkingBob', favicon = '🗣')

app.add_static_files('/topography','topography')

ui.query('body').style('background-image: url(http://localhost:8080/topography/topography.svg);')

with ui.grid(rows = 3).classes('place-self-center'):   
    ui.image('logo.png')
    email_inp = ui.input('Email')

    pass_inp = ui.input('Password', password = True)

    log_in_butt = ui.button('Log-in', on_click=lambda: log_in_press(email_inp.value,pass_inp.value)).classes('bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded')

    new_acc_butt = ui.button('Create account', on_click=lambda: new_acc_press(email_inp.value,pass_inp.value)).classes('bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded')

with email_inp.add_slot("prepend"):
    ui.icon("person")
with pass_inp.add_slot("prepend"):
    ui.icon("person")



def main_gui():
    print("lets go")