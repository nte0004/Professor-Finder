import tkinter as tk
from tkinter import ttk
import RateMyProfessor
import schoolSearch
import commentScrape
import requests

class UserInterface(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title('Professor Finder')
        #self.geometry('450x200')
        self.hasRun = False
        
        self.results = ttk.Frame(self, padding= '12 3 12 3')
        self.results.grid(column=0, row=0, sticky=tk.NSEW)
        self.results.columnconfigure(0, weight=1)
        self.results.rowconfigure(0, weight=1)

        self.header = ttk.Frame(self.results)
        self.header.grid(column=0, row=0)
        
        self.welcomeMsg = 'Welcome to Professor Finder, where you can quickly search for multiple professors at once at over 4000 schools!'
        self.exMsg = 'Example Entries: \"John Doe\", \"Thomas Smith, Jimi H\"'

        self.welcomeMsgLabel = ttk.Label(self.header, text=self.welcomeMsg, wraplength=450, justify=tk.CENTER, padding='0 3 0 3')
        self.welcomeMsgLabel.grid(column=0,row=0, sticky= tk.NSEW)

        self.exMsgLabel = ttk.Label(self.header, text=self.exMsg, padding='0 3 0 3')
        self.exMsgLabel.grid(column=0,row=4, sticky= tk.W)

        self.input = ttk.Frame(self.results, padding='0 3 0 3')
        self.input.grid(column=0, row=1, sticky=tk.NSEW)
        
        self.sLabel = ttk.Label(self.input, text='School:')
        self.sLabel.grid(column=0,row=0, sticky=tk.E)
        
        self.schoolInput = tk.StringVar()
        self.schoolInput.set('Auburn University')
        
        self.sEntry = ttk.Entry(self.input, width=36, textvariable=self.schoolInput)
        self.sEntry.grid(column=1, row=0, sticky=tk.W)

        self.pLabel = ttk.Label(self.input, text='Professor(s):')
        self.pLabel.grid(column=0, row=1, sticky=tk.E)
        
        self.professorInput = tk.StringVar()
        self.professorInput.set('Hugh Kwon, Drew Springall, Tao Shu')
        
        self.pEntry = ttk.Entry(self.input, width=36, textvariable=self.professorInput,)
        self.pEntry.grid(column=1, row=1, sticky=tk.W)

        self.search = ttk.Frame(self.results)
        self.search.grid(column=0, row=3)
        
        self.sButton = ttk.Button(self.search, text='Search', command=self.checkInput)
        self.sButton.grid(column=0,row=0)

        self.message = tk.StringVar()
        
        self.helpEntry = ttk.Label(self.results, textvariable=self.message, wraplength=450, padding='0 3 0 0')
        self.helpEntry.grid(column=0,row=4)
        
        self.results.bind('<Return>', self.checkInput)
        
        self.pEntry.bind('<Return>', self.checkInput)
        self.sEntry.bind('<Return>', self.checkInput)
        
        self.results.focus_set()

        self.session = requests.Session()
        self.session.get('https://ratemyprofessors.com/')

    def checkInput(self, *args):
        self.professorNames = []
        
        if self.schoolInput.get() == '':
            self.message.set('Invalid Input: Please enter the name of a University.')
            return

        if not self.schoolInput.get().replace(' ', '').isalpha():
            self.message.set('Invalid Input: The University name contains invalid characters.')
            return

        self.schoolFound, self.sid = schoolSearch.findMatch(self.schoolInput.get())

        if len(self.schoolFound) == 0:
            self.message.set('Invalid Input: This University is not recognized.')
            return
        
        elif len(self.professorInput.get()) == 0:
            self.message.set('Invalid Input: There no professors to search for.')
            return
        
        self.profNames = self.professorInput.get().split(',')
        for name in self.profNames:
            if not ' ' in name:
                self.message.set(f'Invalid Input: \"{name}\" does not have a last name.')
                return
        
            firstName, lastName = name.strip().split(' ', 1)
            
            if not firstName.isalpha() or not lastName.isalpha():
                self.message.set(f'{name} has invalid characters.')
                return
            
            self.professorNames.append(list((firstName, lastName)))
        
        #If all inputs are valid, either get user to specify the exact school, or if that has already been found then
        #   go ahead and run the professor search in RateMyProfessor.py
        self.message.set('')
            
        if type(self.schoolFound) == list:
            self.sButton.config(state=tk.DISABLED)
            self.schoolWindow()
        elif type(self.schoolFound) == str:
            self.searchResult = RateMyProfessor.main(self.professorNames, str(self.sid), self.session)
            self.argInput()    
    
    def schoolWindow(self):
        selectionwindow = selectionWindow(self)
        selectionwindow.grab_set()
        selectionwindow.protocol("WM_DELETE_WINDOW", self.sButton.config(state=tk.NORMAL))
    
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
        self.title('Search Results')
        
        self.results = ttk.Frame(self, padding= '3 12 3 12')
        self.results.grid(column=0, row=0)
        self.results.columnconfigure(0, weight=1)
        self.results.rowconfigure(0, weight=1)

        self.rNotebook = ttk.Notebook(self.results)
        self.rNotebook.grid(column=0, row=0, sticky=(tk.NSEW))
        
        for professor in userinterface.searchResult:
            self.resultFrame = ttk.Frame(self.results, padding='3 3 3 3')
            self.resultFrame.grid(column=0, row=0)
            
            #self.scroll = ttk.Scrollbar(self.resultFrame, orient=tk.VERTICAL, command=self.rNotebook.yview)
            #self.scroll.grid(column=1, row=0, sticky=(tk.NS))

            self.profStats = ttk.Frame(self.resultFrame, padding='3 3 3 3')
            self.profStats.grid(column=0,row=0, sticky=(tk.N))
            
            self.profStatsLabel = ttk.Label(self.profStats)
            self.profStatsLabel.grid(column=0, row=0, pady=6)
            self.profStatsLabel.config(text="Professor Information", font='bold')
            
            for index, attribute in enumerate(professor):
                self.label = ttk.Label(self.profStats, padding= '3 3 3 3') 
                self.label.grid(column=0,row=index+1, sticky=tk.W)
                self.label.config(text=attribute + ':')
                
                self.text = tk.Text(self.profStats, height=1, borderwidth=0, width=55, wrap=tk.WORD)
                self.text.grid(column=1, row=index+1)
                self.text.insert(tk.INSERT, professor[attribute])
                self.text.config(state=tk.DISABLED)
            
            self.reviews = commentScrape.main(professor['Professor Page'], userinterface.session)
            if self.reviews:
                self.profReviews = ttk.Frame(self.resultFrame, padding='3 3 3 3')
                self.profReviews.grid(column=0, row=1)
                
                self.profReviewLabel = ttk.Label(self.profReviews)
                self.profReviewLabel.grid(column=0, row=0, pady=6, sticky=tk.W)
                self.profReviewLabel.config(text='Student Reviews', font= 'bold')
                
                for idx, review in enumerate(self.reviews):
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
        self.title('Select your school')
        
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
            userinterface.searchResult = RateMyProfessor.main(userinterface.professorNames, self.sid[1], userinterface.session)
        
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
