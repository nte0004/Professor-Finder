import tkinter as tk
from tkinter import ttk
import RateMyProfessor
import schoolSearch
import time
class UserInterface:
    def __init__(self, parent):
        self.hasRun = False
        self.mainframe = ttk.Frame(parent, padding= '3 3 12 12')
        self.mainframe.grid(column=0, row=0)
        self.mainframe.columnconfigure(0, weight=1)
        self.mainframe.rowconfigure(0, weight=1)

        self.school = ttk.Frame(self.mainframe, padding= '3 3 12 12')
        self.school.grid(column=0, row=0)
        self.sLabel = ttk.Label(self.school, text='School:', padding='3 3 3 3')
        self.sLabel.grid(column=0,row=0)
        self.schoolInput = tk.StringVar()
        self.sEntry = ttk.Entry(self.school, width=32, textvariable=self.schoolInput)
        self.sEntry.grid(column=1, row=0)

        self.professors = ttk.Frame(self.mainframe, padding= '3 3 12 12')
        self.professors.grid(column=0, row=1)
        self.pLabel = ttk.Label(self.professors, text='Professors:', padding='3 3 3 3')
        self.pLabel.grid(column=0, row=0)
        self.professorInput = tk.StringVar()
        self.pEntry = ttk.Entry(self.professors, width=32, textvariable=self.professorInput)
        self.pEntry.grid(column=1, row=0)

        self.search = ttk.Frame(self.mainframe, padding='3 3 12 12')
        self.search.grid(column=0, row=2)
        self.sButton = ttk.Button(self.search, text='Submit', command=self.argInput)
        self.sButton.grid(column=0,row=0)

        self.results = ttk.Notebook(self.mainframe, padding='3 3 12 12')
        self.results.grid(column=0, row=3)

        self.resultList = []
    def argInput(self):
        self.sButton.config(state=tk.DISABLED)
        if self.hasRun == True:
            for frame in self.resultList:
                frame:ttk.Frame
                frame.destroy()
                self.results.update()
            self.resultList.clear()
        sid = schoolSearch.findMatch(self.schoolInput.get())
        searchResult = RateMyProfessor.main(self.professorInput.get(), sid)
        for professor in searchResult:
            self.resultFrame = ttk.Frame(self.results, padding='3 3 3 3')
            self.resultFrame.grid(column=0, row=0)
            for index, attribute in enumerate(professor):
                self.label = ttk.Label(self.resultFrame)
                self.label.grid(column=0,row=index)
                self.label.config(text=attribute)
                self.label2 = ttk.Label(self.resultFrame)
                self.label2.grid(column=1, row=index)
                self.label2.config(text=professor[attribute])
            first = professor['First Name']
            last = professor['Last Name']
            self.professorName = first + ' ' + last
            self.results.add(self.resultFrame, text= self.professorName)
            self.resultList.append(self.resultFrame)
        self.hasRun = True
        self.sButton.config(state=tk.NORMAL)
root = tk.Tk()
root.title('Rate My Professor Search')
userinterface = UserInterface(root)
root.mainloop()