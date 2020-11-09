# Imports and Set-up
import sys
import tkinter as tk
from tkinter import ttk
from tkinter.filedialog import askopenfilename, asksaveasfile
import os
import duplicates_reffered_and_hh_members
import duplicates_interviewed_and_hh_members
from tkinter import messagebox

app_version = '0.5'
app_title = "PEP: Findind names duplicates - "+app_version
intro_text = "This app checks duplicates names in a given dataset"

#Dataset we are working with
matches_df = None
finished = False

def tkinter_display_title(title):
    label = ttk.Label(frame, text=title, wraplength=546, justify=tk.LEFT, font=("Calibri", 12, 'bold'), style='my.TLabel')
    label.pack(anchor='nw', padx=(30, 30), pady=(0, 5))
    frame.update()
    return label

def tkinter_display(the_message):
    # the_message = datetime.now().strftime("%H:%M:%S") + '     ' + the_message
    label = ttk.Label(frame, text=the_message, wraplength=546, justify=tk.LEFT, font=("Calibri Italic", 11), style='my.TLabel')
    label.pack(anchor='nw', padx=(30, 30), pady=(0, 5))
    frame.update()
    return label


def save_results():
    file_types = [('Excel File', '*.xlsx')]

    saving_path = asksaveasfile(mode='wb', filetypes = file_types, defaultextension=".xlsx")

    result = names_duplicates.save_df_to_excel(saving_path, matches_df)

    tkinter_display("Saved. Bye!")

def import_file():

    global matches_df
    global finished

    if(finished):
        return
    dataset_path = askopenfilename()

    #If no file was selected, do nothing
    if not dataset_path:
        return

    importing_file_label = tkinter_display("Finding duplicates...")


    if(reffered_and_hh_members_checkbuttom_var.get()==1):
        results_df_path = duplicates_reffered_and_hh_members.search_duplicates(dataset_path)
    else:
        results_df_path = duplicates_interviewed_and_hh_members.search_duplicates(dataset_path)

    finished=True
    importing_file_label = tkinter_display("Ready! Results saved in "+results_df_path)


def window_setup(master):

    global window_width
    global window_height

    #Add window title
    master.title(app_title)

    #Set window position and max size
    window_width, window_height = 600,500#master.winfo_screenwidth(), master.winfo_screenheight()
    master.geometry("%dx%d+0+0" % (window_width, window_height))
    # master.state('zoomed')

    #Make window reziable
    master.resizable(True, True)


def window_style_setup(root):
    root.style = ttk.Style()
    # # root.style.theme_use("clam")  # ('winnative', 'clam', 'alt', 'default', 'classic', 'vista', 'xpnative')
    root.style.configure('my.TButton', font=("Calibri", 11, 'bold'), background='white')
    root.style.configure('my.TLabel', background='white')
    root.style.configure('my.TCheckbutton', background='white')
    root.style.configure('my.TMenubutton', background='white')


if __name__ == '__main__':

    # Create GUI window
    root = tk.Tk()

    window_setup(root)

    window_style_setup(root)

    # Create canvas where app will displayed
    canvas = tk.Canvas(root, width=window_width, height=window_height, bg="white")
    canvas.pack(side="left", fill="both", expand=True)

    # Create frame inside canvas
    frame = tk.Frame(canvas, width=window_width, height=window_height, bg="white")
    frame.pack(side="left", fill="both", expand=True)
    # frame.place(x=0, y=0)

    #This create_window is related to the scrollbar. Im going to delete it atm
    canvas.create_window(0,0, window=frame, anchor="nw")

    #Add intro text
    app_title_label = ttk.Label(frame, text=app_title, wraplength=536, justify=tk.LEFT, font=("Calibri", 13, 'bold'), style='my.TLabel')
    app_title_label.pack(anchor='nw', padx=(30, 30), pady=(30, 10))

    intro_text_1_label = ttk.Label(frame, text=intro_text, wraplength=746, justify=tk.LEFT, font=("Calibri", 11), style='my.TLabel')
    intro_text_1_label.pack(anchor='nw', padx=(30, 30), pady=(0, 12))


    # \nPlease choose one of the following options: either to look for duplicates between referred people and interviewed people + house members, or between interviewed people and house members

    options_label = ttk.Label(frame, text="Options:", wraplength=546, justify=tk.LEFT, font=("Calibri", 12, 'bold'), style='my.TLabel')
    options_label.pack(anchor='nw', padx=(30, 30), pady=(0, 10))


    def reffered_and_hh_members_checkbuttom_command():

        #If both are now off, reselect this one
        if(reffered_and_hh_members_checkbuttom_var.get()==0 and interviewed_and_hh_members_checkbuttom_var.get()==0):
            messagebox.showinfo("Error", "You must have one option selected")
            reffered_and_hh_members_checkbuttom_var.set(True)

        #If the other one is on, turn it off.
        if(interviewed_and_hh_members_checkbuttom_var.get()==1 and reffered_and_hh_members_checkbuttom_var.get()==1):
            interviewed_and_hh_members_checkbuttom.deselect()


    reffered_and_hh_members_checkbuttom_var = tk.IntVar(value=1)
    reffered_and_hh_members_checkbuttom_text = "Find duplicates between referred people and interviewed people + house members"
    reffered_and_hh_members_checkbuttom = tk.Checkbutton(frame,
        text=reffered_and_hh_members_checkbuttom_text,
        bg="white",
        activebackground="white",
        variable=reffered_and_hh_members_checkbuttom_var,
        onvalue=1,
        offvalue=0,
        command = reffered_and_hh_members_checkbuttom_command)
    reffered_and_hh_members_checkbuttom.pack(anchor='nw', padx=(30, 30), pady=(0, 10))


    def interviewed_and_hh_members_checkbuttom_command():

        #If both are now off, reselect this one
        if(reffered_and_hh_members_checkbuttom_var.get()==0 and interviewed_and_hh_members_checkbuttom_var.get()==0):
            messagebox.showinfo("Error", "You must have one option selected")
            interviewed_and_hh_members_checkbuttom_var.set(True)

        #If the other one is on, turn it off.
        if(reffered_and_hh_members_checkbuttom_var.get()==1 and interviewed_and_hh_members_checkbuttom_var.get()==1):
            reffered_and_hh_members_checkbuttom.deselect()

    interviewed_and_hh_members_checkbuttom_var = tk.IntVar(value=0)
    interviewed_and_hh_members_checkbuttom_text = "Find duplicates between interviewed people and house members"
    interviewed_and_hh_members_checkbuttom = tk.Checkbutton(frame,
        text=interviewed_and_hh_members_checkbuttom_text,
        bg="white",
        activebackground="white",
        variable=interviewed_and_hh_members_checkbuttom_var,
        onvalue=1,
        offvalue=0,
        command = interviewed_and_hh_members_checkbuttom_command)
    interviewed_and_hh_members_checkbuttom.pack(anchor='nw', padx=(30, 30), pady=(0, 10))


    #Labels and buttoms to run app
    start_application_label = ttk.Label(frame, text="Run application: ", wraplength=546, justify=tk.LEFT, font=("Calibri", 12, 'bold'), style='my.TLabel')
    start_application_label.pack(anchor='nw', padx=(30, 30), pady=(0, 10))

    select_dataset_button = ttk.Button(frame, text="Select Dataset", command=import_file, style='my.TButton')
    select_dataset_button.pack(anchor='nw', padx=(30, 30), pady=(0, 5))

    # Constantly looping event listener
    root.mainloop()
