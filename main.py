import tkinter as tk
from tkinter import *
from tkinter import messagebox
from tkinter import font
import random
from characters import characters
import pyperclip
import json

# ---------------------------- PASSWORD GENERATOR ------------------------------- #
def generate_pass():
    password = ""
    for _ in range(12):
        rnd_char = str(random.choice(characters))
        password += rnd_char
    password_input.insert(0, password)
    pyperclip.copy(password)

# ---------------------------- SAVE PASSWORD ------------------------------- #
def save_password():

    website = website_input.get()
    username = username_input.get()
    userpass = password_input.get()

    new_data = {
        website: {
            "email": username,
            "password": userpass,
        }
    }

    if len(website) == 0 or len(userpass) == 0:
        return messagebox.showerror(title="Missing Data",
                                    message=f"These are the details entered: \nWebsite: {website}\nEmail: {username}\nPassword: "
                                            f"{userpass}")
    else:
        try:
            with open("saved_passwords.json", "r") as data_file:
                data = json.load(data_file)
        except FileNotFoundError:
            with open("saved_passwords.json", "w") as data_file:
                json.dump(new_data, data_file, indent=4)
        else:
            data.update(new_data)
            with open("saved_passwords.json", "w") as data_file:
                json.dump(data, data_file, indent=4)
        finally:
            website_input.delete(0, END)
            password_input.delete(0, END)

# ---------------------------- SEARCH SETUP --------------------------- #
def search_password():
    try:
        with open("saved_passwords.json", "r") as saved_data:
            data = json.load(saved_data)
            if website_input.get() in data:
                messagebox.showinfo(website_input.get(), message=f'Email: {data[website_input.get()]["email"]}\nPassword: '
                                                                 f'{data[website_input.get()]["password"]}')
                pyperclip.copy(data[website_input.get()]["password"])
            else:
                messagebox.showinfo(message="The website does not exist in the database.")
    except FileNotFoundError:
        messagebox.showerror(title="Error", message="No Data File Found.")

# ---------------------------- UI SETUP ------------------------------- #

window = tk.Tk()
window.title("Password Manager")
window.minsize(width=400, height=400)
window.config(padx=20, pady=20)

font_1 = font.Font(name="TkCaptionFont", exists=True)
font_1.config(family="Helvetica", size=10)

background = tk.Canvas(width=200, height=200)
bg_image = PhotoImage(file="logo.png")
background.create_image(100, 90, image=bg_image)
background.grid(column=0, row=0)

label_website = tk.Label(text="Website:", fg="black", font=("Courier", 12))
label_website.grid(column=0, row=2)

website_input = tk.Entry(width=30, highlightcolor="black")
website_input.focus()
website_input.grid(column=1, row=2, columnspan=4)

label_username = tk.Label(text="Email / Username:", fg="black", font=("Courier", 12))
label_username.grid(column=0, row=3)

username_input = tk.Entry(width=30, highlightcolor="black")
username_input.insert(0, "user@user.com")
username_input.grid(column=1, row=3, columnspan=4)

label_password = tk.Label(text="Password:", fg="black", font=("Courier", 12))
label_password.grid(column=0, row=4)

password_input = tk.Entry(width=30, highlightcolor="black")
password_input.grid(column=1, row=4, columnspan=4)

generate_button = tk.Button(text="Generate Password", command=generate_pass)
generate_button.config(pady=1, padx=1, activebackground="red")
generate_button.grid(column=10, row=4)

add_button = tk.Button(width=30, text="Add", command=save_password)
add_button.config(pady=1, padx=1, activebackground="green")
add_button.grid(column=2, row=12, columnspan=3)

search_button = tk.Button(width=15, text="Search", command=search_password)
search_button.config(pady=1, padx=1, background="orange", fg="black", activebackground="orange")
search_button.grid(column=10, row=2, columnspan=10)


window.mainloop()
