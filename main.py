import string, random, re, pyperclip
from tkinter import *
from datetime import datetime
from tkinter import messagebox


# ---------------------------- GENERATE PASSWORD ------------------------------- #

def generate_password():
    """Generates a password in the password entry widget and copies it automatically to a clipboard"""

    # Generate a 10-18-characters-long password from:
    password = "".join(random.choices(string.ascii_lowercase, k=random.randint(4, 6)) # 4-6 lowercase letters
                       + random.choices(string.ascii_uppercase, k=random.randint(2, 4)) # 2-4 uppercase letters
                       + random.choices(
        list(filter(lambda char: char not in "(){}[]|~ ,'=+-", string.punctuation)),
        k=random.randint(2, 4)) # 2-4 punctuation symbols excluding (){}[]|~ ,'=+-
                       + random.choices(string.digits, k=random.randint(2, 4))) # 2-4 digits

    # Clear the password entry widget and inserts the new password
    password_box.delete(0, END)  # Clears previous generated password if any
    password_box.insert(0, password)

    # Copy the new password to clipboard
    pyperclip.copy(password)


# ---------------------------- SAVE PASSWORD ------------------------------- #
def ask_user():
    """Asks the user if the details they have entered are correct."""
    response = messagebox.askquestion('Are the details correct?',
                                      'Please confirm that the details you have entered are correct.')
    if response == 'yes':
        print('The details are correct.')
        return True
    else:
        print('The details are incorrect.')
        return False


def clear_entry_box(*widgets):
    """Clears any entry widget field passed"""
    for widget in widgets:
        widget.delete(0, END)


def add_password():

    # Get information from entry fields
    website, email, password = website_box.get(), email_box.get(), password_box.get()

    # Check if boxes are not empty
    if any(len(value) == 0 for value in [website, email, password]):
        messagebox.showinfo("Wrong Input", "All boxes must be filled out.")
        return None

    # Check with the user if details are correct
    if not ask_user():
        website_box.focus()
        return None

    # check if csv already exists
    if not os.path.isfile("./password_log.csv"):
        # create a new csv file
        columns = {"Date": [],
                   "Website": [],
                   "Email": [],
                   "Password": []
                   }
        new_data = pandas.DataFrame(columns)
        new_data.to_csv("./password_log.csv")

    # check if the password already in csv
    data = pandas.read_csv("./password_log.csv")
    if any([row.Password == password for (index, row) in data.iterrows()]): # if not [list] means it is empty
        print("This password has been used.")
        return None

    # add a new row/entry
    now = datetime.now()
    date_ = now.strftime("%d%m%y %H:%M")
    new_entry = {"Date": [date_],
                 "Website": [website],
                 "Email": [email],
                 "Password": [password]
                 }
    new_data = pandas.DataFrame.from_dict(new_entry)
    new_data.to_csv("./password_log.csv", mode='a', header=False)
    print("Successfully added a new entry")

    # Clear all fields
    clear_entry_box(website_box, email_box, password_box)

# ---------------------------- UI SETUP ------------------------------- #


# WINDOW
window = Tk()
window.title("Password Generator")
#window.geometry("220x220")
window.config(padx=20, pady=20)
#window.resizable(0, 0)

window.grid_columnconfigure(0, weight=1, uniform="pass")
window.grid_columnconfigure(1, weight=2, uniform="pass")
window.grid_columnconfigure(2, weight=2, uniform="pass")

# PADLOCK LOGO
padlock_logo = Canvas(width=200, height=200, highlightthickness=0)
padlock_logo_img = PhotoImage(file="./logo.png")
padlock_logo.create_image(100, 94, image=padlock_logo_img)
padlock_logo.grid(row=0, column=0, columnspan=3)

# -----------
# WEBSITE LINE

# Website Label
website_label = Label(text="Website:")
website_label.grid(row=1, column=0, sticky="e")

# Website Entry
website_box = Entry()
website_box.grid(row=1, column=1, columnspan=2, sticky="ew")
website_box.focus()

# -----------
# EMAIL/USERNAME LINE

# Email/username label
email_label = Label(text="Email/Username:")
email_label.grid(row=2, column=0, sticky="e")


# Validate if input is email
def validate_email(*args):
    email = email_entry_variable.get()
    correct_formatting = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
    if re.match(correct_formatting, email):
        print("OK")
        add_button.config(state='normal')
        password_button.config(state='normal')
    else:
        print("invalid")
        add_button.config(state='disabled')
        password_button.config(state='disabled')


# Email/username entry
email_entry_variable = StringVar()
# email_entry_variable.set("pawelpedziwiatr@gmail.com") # <-- sets initial textvalue of StringVar/entry_box to "string"

email_box = Entry(textvariable=email_entry_variable) # StringVar bound to email_box
email_box.grid(row=2, column=1, columnspan=2, sticky="ew")

# Checks if email has email format (traces 'write' events on StringVar()
email_entry_variable.trace_add('write', validate_email)

# Add initial example email to email_box (not StringVar, because not want to ENABLE buttons with the example mail)
DEFAULT_EMAIL = "pawelpedziwiatr@gmail.com"
email_box.insert(END, DEFAULT_EMAIL)


def clear_default_email(*args):
    """Removes default email from the email entry field"""
    if email_box.get() == DEFAULT_EMAIL:
        clear_entry_box(email_box)


# Clear email_box on click for convenience
email_box.bind('<Button-1>', clear_default_email)


# -----------
# PASSWORD LINE

# Password Label
password_label = Label(text="Password:")
password_label.grid(row=3, column=0, sticky="e")

# Password entry
password_box = Entry(show="*")
password_box.grid(row=3, column=1, columnspan=1, sticky="ew")

# Password Buttons Frame
password_buttons_frame = Frame()
password_buttons_frame.grid(row=3, column=2)


# Show/Hide Password
def show_pass(event):
    password_box.configure(show="")


def hide_pass(event):
    password_box.configure(show="*")


# Show/Hide Password Button
password_button = Button(password_buttons_frame, text="Show Password")
password_button.grid(row=0, column=0)
password_button.bind("<ButtonPress-1>", show_pass)
password_button.bind("<ButtonRelease-1>", hide_pass)

# Generate Password Button
password_button = Button(password_buttons_frame, text="Generate Password", command=generate_password)
password_button.grid(row=0, column=1)
password_button.config(state='disabled')

# -----------
# ADD LINE
# Add Button
add_button = Button(text="Add", command=add_password)
add_button.grid(row=4, column=1, columnspan=2)
add_button.config(state='disabled')

# Close App
window.mainloop()
