from tkinter import *
import tkinter.font as font
from tkinter import messagebox as msgbox
import os
import json


##### CONSTANTS ############
m = Tk()
m.title("Info storage")
m.geometry("500x500")
############################

font1 = font.Font(family="Agency FB", size=22)
font2 = font.Font(family="Lucinda Grande", size=14)


if not os.path.exists("data/userlist.json"):
    with open("data/userlist.json", "w") as f:
        f.write("{}")
else:
    pass


def signup():
    sw = Toplevel()
    sw.title("Sign Up")


    signup_head = Label(sw, text="Sign Up over here!", font=font1, padx=180).grid(row=0, column=0)

    username_text = Label(sw, text="Username", font=font2, pady=40).grid(row=1, column=0)
    username = Entry(sw, width=40)
    password_text = Label(sw, text="Password", font=font2, pady=10).grid(row=3, column=0)
    password = Entry(sw, width=40)
    re_password_text = Label(sw, text="Re-type your password", font=font2, pady=10).grid(row=5, column=0)
    re_password = Entry(sw, width=40)
    useless = Label(sw, text=" ", pady=50).grid(row=7, column=0)


    username.grid(row=2, column=0)
    password.grid(row=4, column=0)
    re_password.grid(row=6, column=0)
    

    def signup_work():
        p = password.get()
        rp = re_password.get()
        u = username.get()

        if p == rp:
            if len(p) >=3 and len(p) <= 52:
                with open("data/userlist.json", "r") as f:
                    account_check = json.load(f)
                    try:
                        account_check[str(u)]
                        account_exists_error = msgbox.showerror("Account already exists", "The account you a re trying to sign up for already exists! Please try out a different name for your account or login.")
                        account_exists = True
                    except KeyError:
                        account_exists = False
                
                if account_exists == False:
                    with open("data/userlist.json", "r") as f:
                        account = json.load(f)
                    account[str(u)] = str(p)
                    with open("data/userlist.json", "w") as f:
                        json.dump(account, f, indent=4)

            else:
                password_length_error = msgbox.showerror("Password length too short", f"Password must be over 3 characters and under 52 characters. Your password has {len(p)} characters")
                        
        else:
            password_error = msgbox.showerror("Password error", "The 2 passwords don't match. Please try again.")


    go_btn = Button(sw, text="GO", width=20, command=signup_work).grid(row=8, column=0)



title = Label(m, text="Login or Signup to start storing your info!", width=50, height=3, font=font1).grid(row=0, column=0)
signup_button = Button(m, text="Sign Up", command=signup).grid(row=1, column=0)

m.mainloop()