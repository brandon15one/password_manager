from tkinter import *
from tkinter import messagebox
import random
import pyperclip
import json

PINK = "#e2979c"
RED = "#e7305b"
YELLOW = "#f7f5dd"
FONT_NAME = "Courier"


# ---------------------------- PASSWORD GENERATOR ------------------------------- #
# Password Generator Project
def generate_password():
    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u',
               'v',
               'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q',
               'R',
               'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']

    nr_letters = random.randint(8, 10)
    nr_symbols = random.randint(2, 4)
    nr_numbers = random.randint(2, 4)

    password_letters = [random.choice(letters) for _ in range(nr_letters)]
    password_symbols = [random.choice(symbols) for _ in range(nr_symbols)]
    password_numbers = [random.choice(numbers) for _ in range(nr_numbers)]

    password_list = password_numbers + password_symbols + password_letters

    random.shuffle(password_list)

    password = "".join(password_list)

    password_entry.insert(0, password)
    pyperclip.copy(password)


# ---------------------------- SAVE PASSWORD ------------------------------- #
def add_button_click():
    w_ety = web_entry.get()
    em_ety = email_entry.get()
    pass_ety = password_entry.get()
    new_data = {
        w_ety: {
            "email": em_ety,
            "password": pass_ety,
        }
    }

    if len(w_ety) == 0 or len(pass_ety) == 0:
        messagebox.showerror(title="oops", message="Please fill all the fields correctly!")

    else:
        is_ok = messagebox.askokcancel(title="Details Check",
                                       message=f"These are the details entered : \nEmail : {em_ety}"
                                               f" \nWebsite : {w_ety} \nPassword : {pass_ety}"
                                               f"\nis it okay to save?")
        if is_ok:
            try:
                with open("id_and_password.json", mode="r") as data_file:
                    data = json.load(data_file)
            except(FileNotFoundError, json.decoder.JSONDecodeError):
                with open("id_and_password.json", mode="w") as data_file:
                    json.dump(new_data, data_file, indent=4)
            else:
                data.update(new_data)
                with open("id_and_password.json", mode="w") as data_file:
                    json.dump(data, data_file, indent=4)
            finally:
                web_entry.delete(0, "end")
                password_entry.delete(0, "end")

# ---------------------------- FIND PASSWORD ----------------- #
def find_password():
    website = web_entry.get()
    try:
        with open("id_and_password.json", mode="r") as data_file:
            data = json.load(data_file)
    except FileNotFoundError:
        messagebox.showinfo(title="Error", message=f"No data file found")
    else:
        if website in data:
            email = data[website]["email"]
            password = data[website]["password"]
            messagebox.showinfo(title=website, message=f"Email ID  : {email}\nPassword:{password}")
        else:
            messagebox.showinfo(title="Error", message=f"Data for {website} website does not exist")
# ---------------------------- UI SETUP ------------------------------- #
# WINDOW
window = Tk()
window.title("Password Manager")
window.config(padx=80, pady=80)

# CANVAS
canvas = Canvas(width=200, height=200)
bg_img = PhotoImage(file="logo.png")
canvas.create_image(100, 96, image=bg_img)
canvas.grid(row=0, column=1)

# LABELS
website_label = Label(text="Website:")
website_label.grid(row=1, column=0)
email_label = Label(text="Email/Username:")
email_label.grid(row=2, column=0)
password_label = Label(text="Password:")
password_label.grid(row=3, column=0)

# ENTRIES
web_entry = Entry(width=35)
web_entry.grid(row=1, column=1)
web_entry.focus()

email_entry = Entry(width=35)
email_entry.grid(row=2, column=1)
email_entry.insert(0, "siddhantpokemaster12@gmail.com")

password_entry = Entry(width=35)
password_entry.grid(row=3, column=1)

# BUTTONS
add_button = Button(width=36, text="Add", command=add_button_click)
add_button.grid(row=4, column=1, columnspan=2)

generate_button = Button(width=15, text="Generate Password", command=generate_password)
generate_button.grid(row=3, column=2, sticky=EW)

search_button = Button(width=15, text="Search password",command=find_password)
search_button.grid(row=1, column=2)
window.mainloop()
