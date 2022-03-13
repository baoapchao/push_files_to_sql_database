import tkinter as tk
from tkinter.filedialog import askdirectory, askopenfilename

from functions import *

window = tk.Tk()
window.title("File to Database")
window.geometry("800x600")

filepath = ''

label2 = tk.Label(text= 'Input Connection String', width=20)
label2.grid(row=1, column=1)

entry_cstring = tk.Entry(width = 70, bg='yellow')
entry_cstring.grid(row=1, column=2)

label1 = tk.Label(text= 'Choose file to import to DB', width=20)
label1.grid(row=2, column=1)

text_variable1 = tk.StringVar()
label_filepath = tk.Label(textvariable = text_variable1, bg = 'white', width = 50)
label_filepath.grid(row=3, column=2)

def browse_file():
    global filepath 
    filepath = askopenfilename(title='Open a file')
    filepath = os.path.normpath(filepath)
    text_variable1.set(filepath)

button_browse_file = tk.Button(window, text='Browse File', command= lambda:browse_file(), width=12)
button_browse_file.grid(row=3, column=1)



def import_file_to_db():
    global filepath
    c_string = str(entry_cstring.get())
    file_list = [filepath]
    import_files_to_sql(c_string, file_list)

button_import_file = tk.Button(window, text='Import File', command= lambda:import_file_to_db(), width=20)
button_import_file.grid(row=3, column=3)

label3 = tk.Label(text= 'Choose file to import to DB', width=20)
label3.grid(row=6, column=1)

text_variable2 = tk.StringVar()
label_folderpath = tk.Label(textvariable = text_variable2, bg = 'white', width = 50)
label_folderpath.grid(row=7, column=2)

def browse_folder():
    global folderpath 
    folderpath = askdirectory(title='Open a folder')
    folderpath = os.path.normpath(folderpath)
    text_variable2.set(folderpath)

def import_folder_to_db():
    global folderpath
    c_string = str(entry_cstring.get())
    folder_list = [folderpath]
    import_folders_to_sql(c_string, folder_list)

button_browse_folder = tk.Button(window, text='Browse Folder', command= lambda:browse_folder() , width=12)
button_browse_folder.grid(row=7, column=1)

button_import_folder = tk.Button(window, text='Import Folder', command= lambda:import_folder_to_db(), width=20)
button_import_folder.grid(row=7, column=3)

def combine_import_folder_to_db():
    global folderpath
    c_string = str(entry_cstring.get())
    folder_list = [folderpath]
    combine_and_import_folder_to_sql(c_string, folder_list)

button_combine_import_folder = tk.Button(window, text='Combine&Import Folder', command= lambda:combine_import_folder_to_db(), width=20)
button_combine_import_folder.grid(row=8, column=3)


if __name__ == '__main__':
    window.mainloop()
