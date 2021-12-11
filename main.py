from tkinter import *
from tkinter.font import Font
from tkinter import messagebox as msgbox
from tkinter import ttk

import os
import json
from time import sleep


##### CONSTANTS ############
m = Tk()
m.title("Info storage")
m.geometry("500x500")
m.resizable(False, False)
############################

##### FONTS ####################################
font1 = Font(family="Agency FB", size=22)
font2 = Font(family="Lucinda Grande", size=14)
font3 = Font(family="Berlin Sans", size=19)
################################################


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
    
    # The work to be done during signup
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



# The save data function
def save_data(user, key, value):
    # Checking if the data length is too short
    if len(key) or len(value) > 0:
        with open(f"data/userdata/{user}.json", "r") as df:
            data = json.load(df)
            try: # Checking if data already exists. Or else it will give error
                data[str(key)]
                data_exists_error = msgbox.showerror("Key already exists", "The key for this data already exists")
                data_exists = True
            except KeyError:
                data_exists = False

        # Saving the data
        if data_exists == False:
            with open(f"data/userdata/{user}.json", "r") as sf:
                saving_data = json.load(sf)
            saving_data[str(key)] = str(value)
            with open(f"data/userdata/{user}.json", "w") as ff:
                json.dump(saving_data, ff, indent=4)
    else:
        too_short_error = msgbox.showerror("Key or Value length too short", "The length of your key or value MUST be over 0 letters. Please try again") # Error for data length


# Function for the in-account window
def info(user):
    iw = Toplevel()
    iw.geometry("500x650")
    iw.title("Your info")
    iw.resizable(False, False)

    title_store = Label(iw, text=f"Data by {user}", font=font3, width=35).grid(row=0, column=0) # Title of in-account window

    # Auto detection for the data of the specefic account or else it creates a new file
    if not os.path.exists("data/userdata"):
        os.mkdir("data/userdata")
        with open(f"data/userdata/{user}.json", "w") as f: f.write("{}")
    elif not os.path.exists(f"data/userdata/{user}.json"):
        with open(f"data/userdata/{user}.json", "w") as f: f.write("{}")
    else:
        pass

    # The frames to view all data
    info_frame = Frame(iw, pady=45)
    info_canvas = Canvas(info_frame)
    scrollbar = ttk.Scrollbar(info_frame, orient="vertical", command=info_canvas.yview)
    scroll_frame = ttk.Frame(info_canvas)

    scroll_frame.bind(
        "<Configure>",
        lambda e: info_canvas.configure(scrollregion=info_canvas.bbox("all"))
    )
    info_canvas.create_window((0,0), window=scroll_frame, anchor="nw")
    info_canvas.configure(yscrollcommand=scrollbar.set)

    info_frame.grid(row=1, column=0)
    info_canvas.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")
    
    # Widgets to save the data
    add_info = Label(iw, text="Add new data", font=font2)
    enter_key = Label(iw, text="Enter the key for your value")
    key_data_entry = Entry(iw, width=15)
    enter_value = Label(iw, text="Enter your value")
    info_data_entry = Entry(iw, width=45)

    # Refresh function for the data which will refresh the data window. It also calls the save data function because I couldn't enter 2 function names for the Save button
    def refresh_frame():
        # Save data function which saves the given data to the user file
        save_data(user, key_data_entry.get(), info_data_entry.get())
        
        # Refreshing the data
        with open(f"data/userdata/{user}.json", "r") as rshowf:
            refreshed_all_data = json.load(rshowf)

        count = 0
        for i in refreshed_all_data:
            count += 1
            testL = ttk.Label(scroll_frame, text=f"{i}: {refreshed_all_data[i]}").grid(row=count, column=0)


    # The button to save your given credentials
    go_data_btn = Button(iw, text="Save", width=20, height=2, command=refresh_frame)

    add_info.grid(row=2, column=0, pady=3)
    enter_key.grid(row=3, column=0, pady=2)
    key_data_entry.grid(row=4, column=0, pady=13)
    enter_value.grid(row=5, column=0, pady=2)
    info_data_entry.grid(row=6, column=0, pady=13)
    go_data_btn.grid(row=7, column=0, pady=13)

    with open(f"data/userdata/{user}.json", "r") as showf:
        all_data = json.load(showf)

    # Looping through "all_data" and puting it inside the frame
    count = 0
    for i in all_data:
        count += 1
        testL = ttk.Label(scroll_frame, text=f"{i}: {all_data[i]}").grid(row=count, column=0)



# Login
def login_work(username, password):
    user = username.get()
    passwd = password.get()


    with open("data/userlist.json", "r") as f:
        find_account = json.load(f)

        try: #trying to find an account with the username or else, an error occurs
            if find_account[str(user)] == passwd: # Checking if password matches
                #logged_in = msgbox.showinfo("Logged in", f'Logged in successfully as "{user}"') # Successfully logged in
                info(user)
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
