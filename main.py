# imports
import tkinter as tk
from tkinter import filedialog
import keyboard as key


# database
text = ''
scroll_list = []
scroll = 0


# windows
window = tk.Tk()
window.geometry('600x500')
window.title('Mon super éditeur')
window.configure(bg= "#A9A9A9")


# miscellanous_class
class button:
    def __init__(self, Tk, command, txt, x, y, width, height):
        global open_data
        global modify_data
        
        btn = tk.Button(Tk, text= txt, command= command, width= width, height= height)
        btn.place(x= x, y= y)


# buttons
button_save_as = button(window, lambda : modify_data(), 'Save As', 5, 10, 5, 1)
button_open = button(window, lambda : open_data(), 'Open', 100, 10, 4, 1)
button_save = button(window, lambda : save_data(), 'Save', 55, 10, 4, 1)
button_new = button(window, lambda : new_file(), 'New', 145, 10, 4, 1)


# new_file
def new_file():
    ays = tk.Tk()
    ays.title('')
    ays.geometry('200x50')
    save = button(ays, lambda : save_data_new(), 'Save', 22, 15, 4, 1)
    save_as = button(ays, lambda : modify_data_new(), 'Save as', 67, 15, 5, 1)
    go_back = button(ays, lambda : go_back(ays), 'Go Back', 122, 15, 5, 1)


# go_back
def go_back(Tk):
    Tk.quit()
   

# text_zone
text_zone = tk.Label(window)
text_zone.configure(text= text, fg= '#000000', anchor= 'nw', width= 205, height= 60, justify='left')
text_zone.place(x= 0, y= 60)


# miscellanous_function
def check_read(read):
    global text
    global scroll
    global scroll_list
    start = 0
    count = 0
    for i, char in enumerate(read):
        if char == '\n':
            count = count + 1
            if count == 50:
                scroll_list.append(read[start:i+1])
                print(scroll_list[0].count('\n'))
                start = i + 1
                scroll += 1
                count = 0
        if start < len(read):
            text = read[start:]


# file_dialog
def open_filedialog():
    file_directory = filedialog.askopenfilename(initialdir= '/', title= 'select a file directory', 
                                            filetypes= (('Text File', '*.txt'), ('Python File', '*.py')))
    return file_directory

def create_filedialog():
    file_directory = filedialog.asksaveasfilename(initialdir= '/', title= 'select a file directory', 
                                              filetype= (('Text File', '*.txt'), ('Python File', '*.py')),
                                              defaultextension= '.txt',)
    return file_directory
    

# open_data
def open_data():
    global text
    global scroll_list
    global scroll
    global directory

    directory = open_filedialog()
    try:    
        with open(directory, 'r') as data:
            read = data.read()
            print(data.read())
        if read.count('\n') >= 50:
            check_read(read)
        else:
            text = read
        text_zone.configure(text= text)
    except FileNotFoundError:
        pass


# modify_data
def modify_data():
    global text
    global directory
    
    directory = create_filedialog()
    try:    
        with open(directory, 'w') as data:
                for part in scroll_list:
                    data.write(part)
                data.write(text)
    except FileNotFoundError:
        pass


def modify_data_new():
    global text
    global directory
    global scroll_list
    
    directory = create_filedialog()
    try:    
        with open(directory, 'w') as data:
                for part in scroll_list:
                    data.write(part)
                data.write(text)
    except FileNotFoundError:
        pass
    text = ''
    scroll_list = []
    text_zone.configure(text= text)


# save_data
def save_data():
    global scroll_list
    global text
    global directory
    
    with open(directory, 'w') as data:
        try:
            for part in scroll_list:
                data.write(part)
            data.write(text)
        except NameError:
            modify_data

def save_data_new():
    global scroll_list
    global text
    global directory
    
    with open(directory, 'w') as data:
        try:
            for part in scroll_list:
                data.write(part)
            data.write(text)
        except NameError:
            modify_data
    text = ''
    scroll_list = []
    text_zone.configure(text= text)


# keyboard_gestion
def key_action(event):
    global text
    global scroll
    
    if len(event.name) == 1:
        text += event.name
        text_zone.configure(text= text)
        scroll = len(scroll_list)      
    elif event.name == 'space':
        text += ' '
        text_zone.configure(text= text)
        scroll = len(scroll_list)
    elif event.name == 'tab':
        text += '    '
        text_zone.configure(text= text)
        scroll = len(scroll_list)
    elif event.name == 'backspace':
        if text == '':
            text = scroll_list[-1]
            del scroll_list[-1]
            text_zone.configure(text= text)
        text = text[:-1]
        text_zone.configure(text= text)
        scroll = len(scroll_list)
    elif event.name == 'enter':
        if text.count('\n') >= 50:
            text += '\n'
            scroll_list.append(text)
            text = ''
            text_zone.configure(text= text)
            scroll = len(scroll_list)               
        else:
            text += "\n"
            text_zone.configure(text= text, anchor= 'nw')
            scroll = len(scroll_list)
    elif event.scan_code == 72 and scroll > 0:
        scroll -= 1
        text_zone.configure(text= scroll_list[scroll])    
    elif event.scan_code == 80:
        try:
            scroll += 1
            text_zone.configure(text= scroll_list[scroll])
        except IndexError:
            text_zone.configure(text= text)
            scroll = len(scroll_list)
key.on_press(key_action)


# mainloop
window.mainloop()