import tkinter as tk
from tkinter import ttk
import RateMyProfessor
import schoolSearch

#schools = []
#schoolChoice = str('')

class UserInterface:
    def __init__(self, parent):
        self.hasRun = False
        self.parent = parent
        self.mainframe = ttk.Frame(self.parent, padding= '3 3 12 12')
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
        self.sButton = ttk.Button(self.search, text='Submit', command=self.checkInput)
        self.sButton.grid(column=0,row=0)

        self.results = ttk.Frame(self.mainframe, padding='3 3 12 12')
        self.results.grid(column=0, row=3)

        self.resultList = []

    def checkInput(self):
        if self.hasRun == True:
            self.rNotebook.destroy()
        self.schoolFound, self.sid = schoolSearch.findMatch(self.schoolInput.get())
        if type(self.schoolFound) == list:
            self.sButton.config(state=tk.DISABLED)
            self.newWindow(selectionWindow)
        elif type(self.schoolFound) == str:
            self.searchResult = RateMyProfessor.main(self.professorInput.get(), self.sid)
            self.argInput()
        else:
            raise TypeError('Bad Result from schoolSearch.py, must be a list or string')

    def newWindow(self, _class):
        self.new = tk.Toplevel(self.parent)
        _class(self.new)

    def argInput(self):
        self.rNotebook = ttk.Notebook(self.results, padding='3 3 12 12')
        self.rNotebook.grid(column=0, row=0)
        for professor in self.searchResult:
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
            self.rNotebook.add(self.resultFrame, text= self.professorName)
            self.resultList.append(self.resultFrame)
        self.hasRun = True
        self.sButton.config(state=tk.NORMAL)

class selectionWindow:
    def __init__(self, parent):
        self.parent = parent
        self.mainframe = ttk.Frame(self.parent, padding= '3 3 12 12')
        self.mainframe.grid(column=0, row=0)
        self.mainframe.columnconfigure(0, weight=1)
        self.mainframe.rowconfigure(0, weight=1)

        self.mLabel = ttk.Label(self.mainframe, text="Select a School", padding = '3 3 3 3')
        self.mLabel.grid(column=0, row=0)

        self.lstFrame = ttk.Frame(self.mainframe, padding= '3 3 12 12')
        self.lstFrame.grid(column=0, row=1)

        self.schoolList = tk.StringVar(value=userinterface.schoolFound)
        for school in userinterface.schoolFound:
            maxLen = 0
            if len(school) > maxLen:
                maxLen = len(school)
        self.lstBox = tk.Listbox(self.lstFrame, listvariable=self.schoolList, width=maxLen, height=10)
        self.lstBox.grid(column=0, row=0)
        self.scroll = ttk.Scrollbar(self.lstFrame, orient=tk.VERTICAL, command=self.lstBox.yview)
        self.scroll.grid(column=1, row=0, sticky=(tk.N,tk.S))
        self.lstBox['yscrollcommand'] = self.scroll.set
        self.lstBox.bind('<Double-1>', self.findSID)

    def findSID(self, *args):
        self.schoolIdx = self.lstBox.curselection()
        if len(self.schoolIdx) == 1:
            self.idx = int(self.schoolIdx[0])
            userinterface.searchResult = RateMyProfessor.main(userinterface.professorInput.get(), userinterface.sid[self.idx])
            userinterface.parent.lift()
            userinterface.new.destroy()
            userinterface.argInput()
    
root = tk.Tk()
root.title('Rate My Professor Search')
userinterface = UserInterface(root)
root.mainloop()