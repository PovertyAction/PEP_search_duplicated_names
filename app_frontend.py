# Imports and Set-up
import sys
import tkinter as tk
from tkinter import ttk
from tkinter.filedialog import askopenfilename, asksaveasfile
from PIL import ImageTk, Image
import webbrowser
import os
import names_duplicates

intro_text = "This app checks duplicates names in a given dataset."
app_title = "Findind names duplicates - v0.1"

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
    
    # matches_df.to_csv('duplicates.csv', index=False)
    matches_df = names_duplicates.search_names_intersection(dataset_path)
    finished = True

    importing_file_label.pack_forget()
    importing_file_label = tkinter_display("Ready!")

    select_dataset_button = ttk.Button(frame, text="Save results", command=save_results, style='my.TButton')
    select_dataset_button.pack(anchor='nw', padx=(30, 30), pady=(0, 5))


def window_setup(master):

    global window_width
    global window_height

    #Add window title
    master.title(app_title)
    
    #Set window position and max size
    window_width, window_height = 500,500#master.winfo_screenwidth(), master.winfo_screenheight()
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
    
    #Labels and buttoms to run app
    start_application_label = ttk.Label(frame, text="Run application: ", wraplength=546, justify=tk.LEFT, font=("Calibri", 12, 'bold'), style='my.TLabel')
    start_application_label.pack(anchor='nw', padx=(30, 30), pady=(0, 10))
    
    select_dataset_button = ttk.Button(frame, text="Select Dataset", command=import_file, style='my.TButton')
    select_dataset_button.pack(anchor='nw', padx=(30, 30), pady=(0, 5))

    # Constantly looping event listener
    root.mainloop()  