import tkinter as tk
from tkinter import filedialog as fd
from tkinter.messagebox import showinfo
import pandas as pd
from utils import *
from api import *

# create the root window
root = tk.Tk()
root.title('CSV imported for Google Sheets')
root.resizable(False, False)
root.geometry('400x700')


lbl = tk.Label(root, text=csv_path)
lbl.grid()

    
# Prompts user to enter the name of existing spreadsheet
def upload_existing():
    tk.Label(root, text="--------------------------------------------\nName of the Sheet").grid()
    sheet_name = tk.Entry(root, width=20)
    sheet_name.grid(row = len(col_list)+8, column=0)
    tk.Button(root, text="Go!", command=lambda: upload(sheet_name.get())).grid(row=len(col_list)+8, column=1)

# Selects the spreadsheet and lists all of the available worksheets + an option to create a new worksheet
def upload(sheet_name):
    global sheet
    sheet = gc.open(sheet_name)
    tk.Label(root, text="Sheet Not found! Check name and try again.").grid()
    tk.Label(root, text="--------------------------------------------\nChoose the Sheet to upload to").grid()
    global ws_list
    ws_list = []
    for i, ws in enumerate(sheet.worksheets()):
        ws_list.append(ws.title)
        tk.Button(root, text=ws.title, command=lambda: to_sheet(ws_list[i])).grid()
    new_ws = tk.Entry(root, width=20)
    new_ws.grid()
    tk.Button(root, text="Create new worksheet", command=lambda: new_worksheet(new_ws.get())).grid()

# Create a new worksheet of desied name
def new_worksheet(ws_name):
    sheet.add_worksheet(ws_name, rows=1000, cols=100)
    to_sheet(ws_name)

# Code to import the selected columns to GSheets
def to_sheet(ws):
    worksheet = sheet.worksheet(ws)
    worksheet.update([df.columns.values.tolist()] + df.values.tolist())
    tk.Label(root, text=f"CSV imported to {ws} worksheet. You may now close this window").grid()

# Create new spreadsheet
def new_sheet(sheet_name):
    global sheet
    sheet = gc.create(sheet_name)
    upload(sheet_name)

# Prompts user to input name of new sheet
def create_new_sheet():
    tk.Label(root, text="--------------------------------------------\nName of the Sheet").grid()
    sheet_name = tk.Entry(root, width=20)
    sheet_name.grid(row=len(col_list)+8, column=0)
    tk.Button(root, text="Go!", command=lambda: new_sheet(sheet_name.get())).grid(row=len(col_list)+8, column=1)
    
# Code to delete the selected columns
def delete_cols():
    del_list = []
    for index, col in enumerate(df.columns):
        if col_list[index].get() == 0:
            del_list.append(col)
    for i in del_list:
        del df[i]
    tk.Label(root, text="--------------------------------------------").grid()
    tk.Button(root, text="Upload to existing Spreadsheet", command=upload_existing).grid()
    tk.Button(root, text="Create New Spreadsheet", command=create_new_sheet).grid()


submit_button = tk.Button(root, text="Submit", command=delete_cols)

# File selection window
def select_file():
    filetypes = (
        ('comma separated values', '*.csv'),
    )

    filename = fd.askopenfilename(
        title='Open a file',
        initialdir='/',
        filetypes=filetypes)
    
    global csv_path
    global df
    
    csv_path = filename
    df = pd.read_csv(csv_path)
    showinfo(
        title='Selected File',
        message=filename
    )

    lbl.configure(text=csv_path)

    tk.Label(root, text="--------------------------------------\nSelect the Columns you wish to import\n--------------------------------------").grid()
    for index, col in enumerate(df.columns):
        col_list.append(tk.IntVar(value=0))
        tk.Checkbutton(root, variable=col_list[index], text=col, onvalue=1, offvalue=0).grid(column=0)
    submit_button.grid()
    

# open button
open_button = tk.Button(
    root,
    text='Open a File',
    command=select_file
)

open_button.grid()

placement = 6


# run the application
root.mainloop()