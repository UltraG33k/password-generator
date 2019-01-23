import tkinter as tk
from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from tkinter import simpledialog
import hashlib
import pyperclip
import os
import json

'''
This program takes a platform and a passphrase.

It converts them into a unique sha256 string and slices it to a 
    certain amount of characters and adds some special characters
'''

root = tk.Tk()
platform = StringVar()
passphrase = StringVar()
appdata = os.getenv('APPDATA')
myPath = appdata + "\\pwgen"
myFile = "\\social.json"
platforms = {}
platforms['social'] = []

def create_password():
    global platform
    global passphrase
    plf = platform.get()
    pwp = passphrase.get()
    new_pass = hashlib.sha256()
    new_pass.update(b"" + plf.encode() + pwp.encode())
    slice_one = new_pass.hexdigest()[26:35]
    slice_two = new_pass.hexdigest()[35:43]
    sliced = slice_one + "!#%&" + slice_two.upper()
    pyperclip.copy(sliced)
    messagebox.showinfo("Success!", "Password copied to clipboard!")


def new_social_entry():
    new_social = simpledialog.askstring("Add new!", "Add new platform")
    platforms['social'].append(new_social)
    # Create dir in appdata if it doesn't exist
    if not os.path.exists(myPath):
        os.mkdir(myPath)

    with open(myPath + myFile, "w+") as social_file:
        json.dump(platforms, social_file)

    del platforms['social']
    platforms['social'] = []
    get_social_platforms()
    newest_entry = len(platforms['social']) - 1
    pl.current(newest_entry)
    pw.config(state="normal")
    btn.config(state="normal")


def get_social_platforms():
    # Open file (if file exists)
    if os.path.exists(myPath) & os.path.isfile(myPath + myFile):
        with open(myPath + myFile) as json_file:
            data = json.load(json_file)
            for s in data['social']:
                platforms['social'].append(s.capitalize())
        pl.selection_clear()
        pl.config(values=platforms['social'])
    else:
        pl.config(values=['Please add platform'])
        pw.config(state="disabled")
        btn.config(state="disabled")
    pl.current(0)


root.title("Password helper")
root.geometry("350x200")
plt = tk.Label(root, text=str("Please select platform: "), font=("Calibri Bold", 15))
plt.grid(column=1, row=0)
pl = ttk.Combobox(root, state="readonly", textvariable=platform, font=('Calibri', 15))
pl.grid(column=1, row=1)
nse = tk.Button(root, text="Add new platform", font=("Calibri", 12), command=new_social_entry)
nse.grid(column=1, row=2)
pwt = tk.Label(root, text=str("Your passphrase: "), font=("Calibri Bold", 15))
pwt.grid(column=1, row=3)
pw = tk.Entry(root, textvariable=passphrase, show="*", font=("Calibri", 15))
pw.grid(column=1, row=4)
btn = tk.Button(root, text="Generate password", font=("Calibri", 12), command=create_password)
btn.grid(column=1, row=5)

get_social_platforms()

root.grid_columnconfigure(0, weight=1)
root.grid_columnconfigure(2, weight=1)
root.grid_rowconfigure(5, weight=1)

root.mainloop()
