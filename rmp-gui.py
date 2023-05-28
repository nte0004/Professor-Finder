import tkinter as tk
from tkinter import ttk
import RateMyProfessor
import schoolSearch
import commentScrape

class UserInterface(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title('Rate My Professor Search')
        self.hasRun = False
        self.results = ttk.Frame(self, padding= '3 3 12 12')
        self.results.grid(column=0, row=0)
        self.results.columnconfigure(0, weight=1)
        self.results.rowconfigure(0, weight=1)

        self.school = ttk.Frame(self.results, padding= '3 3 12 12')
        self.school.grid(column=0, row=0,sticky=tk.W)
        self.sLabel = ttk.Label(self.school, text='School:', padding='3 3 3 3')
        self.sLabel.grid(column=0,row=0, sticky=tk.W)
        self.schoolInput = tk.StringVar()
        self.schoolInput.set('Auburn University')
        self.sEntry = ttk.Entry(self.school, width=32, textvariable=self.schoolInput)
        self.sEntry.grid(column=1, row=0, sticky=(tk.W, tk.E), padx=23)

        self.professors = ttk.Frame(self.results, padding= '3 3 12 12')
        self.professors.grid(column=0, row=1, sticky=tk.W)
        self.pLabel = ttk.Label(self.professors, text='Professor(s):', padding='3 3 3 3')
        self.pLabel.grid(column=0, row=0, sticky=tk.W)
        self.professorInput = tk.StringVar()
        self.professorInput.set('Hugh Kwon')
        self.pEntry = ttk.Entry(self.professors, width=32, textvariable=self.professorInput,)
        self.pEntry.grid(column=1, row=0, sticky=(tk.W, tk.E))

        self.search = ttk.Frame(self.results, padding='3 3 12 12')
        self.search.grid(column=0, row=2)
        self.sButton = ttk.Button(self.search, text='Submit', command=self.checkInput)
        self.sButton.grid(column=0,row=0)

        self.message = tk.StringVar()
        self.helpEntry = ttk.Label(self.results, textvariable=self.message, wraplength=450)
        self.helpEntry.grid(column=0,row=3)
        self.results.bind('<Return>', self.checkInput)
        self.pEntry.bind('<Return>', self.checkInput)
        self.sEntry.bind('<Return>', self.checkInput)
        self.results.focus_set()

    def checkInput(self, *args):
        if self.hasRun == True:
            self.message.set('')
        self.professorNames = []
        self.cleanInput = self.professorInput.get().split(',')
        for name in self.cleanInput:
            if not ' ' in name:
                self.message.set('A professor name must have a first and last part.\nCheck for extra commas or whitespaces.')
                return
            fullname = name.strip().split(' ', 1)
            if not fullname[0].isalpha() or not fullname[1].isalpha():
                self.message.set(f'{fullname[0]} {fullname[1]} has invalid characters.')
                return
            self.professorNames.append(fullname)
        self.schoolFound, self.sid = schoolSearch.findMatch(self.schoolInput.get())
        if len(self.schoolFound) == 0:
            self.message.set('No school(s) found. Try a different search.')
            return
        elif len(self.professorInput.get()) == 0:
            self.message.set('Please add professor(s).\nIf there is more than one, seperate the entire name with a comma.')
            return
        #If all inputs are valid, either get user to specify the exact school, or if that has already been found then
        #   go ahead and run the professor search in RateMyProfessor.py
        else:
            self.message.set('')
            if type(self.schoolFound) == list:
                self.sButton.config(state=tk.DISABLED)
                self.schoolWindow()
            elif type(self.schoolFound) == str:
                self.searchResult = RateMyProfessor.main(self.professorNames, self.sid)
                self.argInput()
                
            else:
                raise TypeError('Bad Result from schoolSearch.py, must be a list or string')
    
    def schoolWindow(self):
        selectionwindow = selectionWindow(self)
        selectionwindow.grab_set()
    
    def resultWindow(self):
        resultswindow = resultsWindow(self)
        resultswindow.grab_set()

    def argInput(self):
        self.resultWindow()
        self.hasRun = True
        self.sButton.config(state=tk.NORMAL)

class resultsWindow(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title('Rate My Professor Search')
        self.results = ttk.Frame(self, padding= '3 3 12 12')
        self.results.grid(column=0, row=0)
        self.results.columnconfigure(0, weight=1)
        self.results.rowconfigure(0, weight=1)

        self.rNotebook = ttk.Notebook(self.results, padding='3 3 12 12')
        self.rNotebook.grid(column=0, row=0, sticky=(tk.W, tk.E))
        
        for professor in userinterface.searchResult:
            self.resultFrame = ttk.Frame(self.results, padding='3 3 3 3')
            self.resultFrame.grid(column=0, row=0)
            self.profStats = ttk.Frame(self.resultFrame, padding='3 3 3 3')
            self.profStats.grid(column=0,row=0)
            for index, attribute in enumerate(professor):
                self.label = ttk.Label(self.profStats, padding= '3 3 3 3') #use if not error to do better formatting for real results
                self.label.grid(column=0,row=index, sticky=tk.W)
                self.label.config(text=attribute + ':')
                self.text = tk.Text(self.profStats, height=1, borderwidth=0, width=55, wrap=tk.WORD)
                self.text.grid(column=1, row=index)
                self.text.insert(tk.INSERT, professor[attribute])
                self.text.config(state=tk.DISABLED)
            if not 'Error' in professor:
                self.profReviews = ttk.Frame(self.resultFrame, padding='3 3 3 3')
                self.profReviews.grid(column=1, row=0)
                self.profReviewLabel = ttk.Label(self.profReviews)
                self.profReviewLabel.grid(column=0, row=0)
                self.profReviewLabel.config(text='Student Reviews')
                for idx, review in enumerate(commentScrape.main(professor['Professor Page'])):
                    self.reviewFrame = ttk.Frame(self.profReviews, padding='3 3 3 3')
                    self.reviewFrame.grid(column=0, row= idx+1)
                    self.rclass = ttk.Label(self.reviewFrame)
                    self.rclass.grid(column=0, row=0, sticky=tk.W)
                    self.rclass.config(text=review['Class'])
                    self.review = tk.Text(self.reviewFrame, height=5, border=0, width=76, wrap = tk.WORD)
                    self.review.grid(column=0, row=1)
                    self.review.insert(tk.INSERT, review['Comment'])
                    self.review.config(state=tk.DISABLED)
                
            
            first = professor['First Name']
            last = professor['Last Name']
            self.professorName = first + ' ' + last
            self.rNotebook.add(self.resultFrame, text= self.professorName)
        
        self.button = ttk.Button(self.results, text='Done', command=self.destroy, padding='12 12 12 12')
        self.button.grid(column=0, row=1)      

class selectionWindow(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title('Rate My Professor Search')
        self.results = ttk.Frame(self, padding= '3 3 12 12')
        self.results.grid(column=0, row=0)
        self.results.columnconfigure(0, weight=1)
        self.results.rowconfigure(0, weight=1)

        self.mLabel = ttk.Label(self.results, text="Select a School", padding = '3 3 3 3')
        self.mLabel.grid(column=0, row=0, columnspan=2)

        self.mFrame = ttk.Frame(self.results, padding= '3 3 12 12')
        self.mFrame.grid(column=0, row=2)

        self.lstFrame = ttk.Frame(self.results, padding= '15 3 12 12')
        self.lstFrame.grid(column=0, row=1)

        self.mFrameButton = ttk.Button(self.mFrame, text="Submit", command=self.findSID)
        self.mFrameButton.grid(column=0, row=0)

        self.curSelection = tk.StringVar()
        self.curSelLabel = ttk.Label(self.mFrame, textvariable=self.curSelection, wraplength=250)
        self.curSelLabel.grid(column=0, row=1)

        self.schoolList = tk.StringVar(value=userinterface.schoolFound)
        for school in userinterface.schoolFound:
            maxLen = 0
            if len(school) > maxLen:
                maxLen = len(school)
        self.lstBox = tk.Listbox(self.lstFrame, listvariable=self.schoolList, width=maxLen, height=10, )
        self.lstBox.grid(column=0, row=0)

        self.scroll = ttk.Scrollbar(self.lstFrame, orient=tk.VERTICAL, command=self.lstBox.yview)
        self.hscroll = ttk.Scrollbar(self.lstFrame)
        self.scroll.grid(column=1, row=0, sticky=(tk.N,tk.S))
        self.lstBox['yscrollcommand'] = self.scroll.set

        self.lstBox.bind('<Double-1>', self.findSID)
        self.lstBox.bind('<<ListboxSelect>>', self.curSel)

    def findSID(self, *args):
        self.schoolIdx = self.lstBox.curselection()
        self.schoolName = self.lstBox.get(self.schoolIdx)
        self.sid = schoolSearch.findMatch(self.schoolName)
        if len(self.schoolIdx) == 1:
            userinterface.schoolInput.set(str(self.schoolName))
            userinterface.searchResult = RateMyProfessor.main(userinterface.professorNames, self.sid[1])
            self.destroy()
            userinterface.argInput()
    
    def curSel(self, *args):
        self.schoolIdx = self.lstBox.curselection()
        if len(self.schoolIdx) == 1:
            self.idx = int(self.schoolIdx[0])
            self.selection = userinterface.schoolFound[self.idx]
            self.curSelection.set(f'School: {self.selection}')

if __name__ == "__main__":
    userinterface = UserInterface()
    userinterface.mainloop()