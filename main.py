from tkinter import *
import tkinter.font as font
from tkinter import messagebox as msgbox
import os
import json
from time import sleep


##### CONSTANTS ############
m = Tk()
m.title("Info storage")
m.geometry("500x500")
m.resizable(False, False)
############################

font1 = font.Font(family="Agency FB", size=22)
font2 = font.Font(family="Lucinda Grande", size=14)


# Auto-detection of "userlist.json"
if not os.path.exists("data"):
    os.mkdir("data")
    with open("data/userlist.json", "w") as f: f.write("{}")
else:
    if not os.path.exists("data/userlist.json"):
        with open("data/userlist.json", "w") as f: f.write("{}")
    else:
        pass


# Signup

def signup():
    sw = Toplevel()
    sw.title("Sign Up")
    sw.resizable(False, False)


    signup_head = Label(sw, text="Sign Up over here!", font=font1, padx=180).grid(row=0, column=0)

    username_text = Label(sw, text="Username", font=font2, pady=40).grid(row=1, column=0)
    username = Entry(sw, width=40)
    password_text = Label(sw, text="Password", font=font2, pady=10).grid(row=3, column=0)
    password = Entry(sw, width=40, show="\u2022")
    re_password_text = Label(sw, text="Re-type your password", font=font2, pady=10).grid(row=5, column=0)
    re_password = Entry(sw, width=40, show="\u2022")
    useless = Label(sw, text=" ", pady=50).grid(row=7, column=0)


    username.grid(row=2, column=0)
    password.grid(row=4, column=0)
    re_password.grid(row=6, column=0)
    

    def signup_work():
        p = password.get()
        rp = re_password.get()
        u = username.get()

        if p == rp: # Checking is bot the paswords are the same
            if len(p) >=3 and len(p) <= 52: # Checking if password length is in range (Between 3 and 52)
                with open("data/userlist.json", "r") as f:
                    account_check = json.load(f)
                    try: # Checking if account exists by
                        account_check[str(u)] # Looking for a key with the username in the json file (This will send an error if account already exists.)
                        account_exists_error = msgbox.showerror("Account already exists", "The account you are trying to sign up for already exists! Please try out a different name for your account or login.") # Giving an error with the details which will be displayed on the screen.
                        account_exists = True # Setting account exists to True
                    except KeyError: # When account doesn't exist
                        account_exists = False # Setting account exists to False
                
                # The things to do when account doesn't exist (Basically creating an account)
                if account_exists == False:
                    with open("data/userlist.json", "r") as f:
                        account = json.load(f)
                    account[str(u)] = str(p)
                    with open("data/userlist.json", "w") as f:
                        json.dump(account, f, indent=4)
                    account_created = msgbox.showinfo("Account created", f'Account for "{u}" has been successfully created!')
                    sleep(1) # Waiting for 1 second after clicking ok
                    sw.destroy() # Destroying the signup window

            else:
                password_length_error = msgbox.showerror("Password length is incorrect", f"Password must be over 3 characters and under 52 characters. Your password has {len(p)} characters") # Giving an error if password length is too short.
                        
        else:
            password_error = msgbox.showerror("Password error", "The 2 passwords don't match. Please try again.") # Giving an error if passwords do not match


    go_btn = Button(sw, text="GO", width=20, command=signup_work).grid(row=8, column=0)


# Login
def login_work(username, password):
    user = username.get()
    passwd = password.get()
    with open("data/userlist.json", "r") as f:
        find_account = json.load(f)

        try: #trying to find an account with the username or else, an error occurs
            if find_account[str(user)] == passwd: # Checking if password matches
                logged_in = msgbox.showinfo("Logged in", f'Logged in successfully as "{user}"') # Successfully logged in
            else:
                password_not_match = msgbox.showerror("Password doesn't match", "The password for this account doesn't match the given credentials. Please enter the correct password") # Password doesn't match

        except KeyError: # Error. No account found
            account_not_found = msgbox.showerror("Account not found", "The account you are trying to login to doesn't exist! Please signup or try a different name.") # Error which is displayed onscreen which says account not found

# VARIABLES

title = Label(m, text="Login to start accessing your info", width=50, height=3, font=font1).grid(row=0, column=0)
enter_username = Label(m, text="Username", pady=20, font=font2).grid(row=1, column=0)
username = Entry(m, width=40,)
enter_password = Label(m, text="Password", pady=20, font=font2).grid(row=3, column=0)
password = Entry(m, width=40, show="\u2022")
useless = Label(m, text=" ", pady=10).grid(row=5, column=0)
login_button = Button(m, text="Login", font=font2, command=lambda: login_work(username, password)).grid(row=6, column=0)
or_text = Label(m, text="Or, you could signup!", pady=20, font=font1).grid(row=7, column=0)
signup_button = Button(m, text="Sign Up", font=font2, command=signup).grid(row=8, column=0)

###########

username.grid(row=2, column=0)
password.grid(row=4, column=0)

m.mainloop()
