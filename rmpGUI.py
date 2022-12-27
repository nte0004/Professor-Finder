from tkinter import *
from tkinter import ttk
import schoolSearch
import RateMyProfessor

root = Tk()
root.title('Rate My Professor Finder')

#Main Content Frame
mainframe = ttk.Frame(root, padding='30 30 120 120')
mainframe.grid(column=0,row=0, sticky=(N, W, E ,S))
root.columnconfigure(0, weight=1)
root.rowconfigure(0, weight=1)

#School Entry
school = StringVar()
school_Entry = ttk.Entry(mainframe, width=20, textvariable=school)
school_Entry.grid(column=2, row=1, sticky=(W, E))

#Labels
ttk.Label(mainframe, text='Your College: ').grid(column=1, row=1, sticky=E)