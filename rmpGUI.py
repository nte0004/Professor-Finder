from tkinter import *
from tkinter import ttk
import GUIMiddleMan

def search(*args):
    school, sid, status = GUIMiddleMan.schoolSearchInput(schoolInput.get())
    result.set(status)
root = Tk()
root.title('Rate My Professor Finder')

#Main Content Frame
mainframe = ttk.Frame(root, padding='30 30 120 120')
mainframe.grid(column=0,row=0, sticky=(N, W, E ,S))
root.columnconfigure(0, weight=1)
root.rowconfigure(0, weight=1)

#Row 1
schoolInput = StringVar()
school_Entry = ttk.Entry(mainframe, width=20, textvariable=schoolInput)
school_Entry.grid(column=2, row=1, sticky=(W, E))

ttk.Label(mainframe, text='Your College: ').grid(column=1, row=1, sticky=E)
ttk.Button(mainframe, text='Search', command= search).grid(column=3, row=1, sticky=W)

#Row 2
result = StringVar()
ttk.Label(mainframe, textvariable= result).grid(column=2, row=2, sticky=(W, E))
ttk.Label(mainframe, text='Status:').grid(column=1, row=2, sticky=E)

def schoolListBox(school: str | list):
    listFrame = ttk.Frame(mainframe, padding = '3 3 12 12')
    listFrame.grid(column=2, row=3, sticky=(N, E, S, W))
    if type(school) is list:
        schoolList = school
        lenMax = 0
        maxSchools = len(schoolList)
        for item in schoolList:
            if len(item) > lenMax:
                lenMax = len(item)
        if maxSchools > 10:
            maxSchools = 10
        choicesvar = StringVar(value= schoolList)
        l = Listbox(listFrame, listvariable= choicesvar, height= maxSchools, width= lenMax)
        l.grid(column=0, row=0, sticky=(N, E))
        scroll = ttk.Scrollbar(listFrame, orient= VERTICAL, command= l.yview)
        scroll.grid(column=1, row=0, sticky=(N,S))
        l['yscrollcommand'] = scroll.set

    elif type(school) is str:
        ttk.Label(listFrame, text=f'School: {school}').grid(column=0, row=0, sticky=E)

#Final formatting
for child in mainframe.winfo_children():
    child.grid_configure(padx=5, pady=5)
school_Entry.focus()
root.bind('<Return>', search)

#Mainloop to display everything
root.mainloop()