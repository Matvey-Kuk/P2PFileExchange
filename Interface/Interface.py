
"""
Здесь будет реализация консольного интерфейса программы.
"""

from tkinter import *
from tkinter.ttk import *

class Interface(object):
    def input_command(self, event):
        s = self.txtfr2.get('1.0', 'end')
        self.txtfr2.delete('1.0', 'end')
        self.txtfr1['state'] = 'normal'
        s = s.strip()
        self.txtfr1.insert(AtInsert(),"\n" + s)
        input_words = s.split()
        self.txtfr1['state'] = 'disabled'

    def asking_for_information(self):
        self.txtfr1.after(5000, self.asking_for_information)
        self.txtfr1['state'] = 'normal'
        self.txtfr1.insert(AtInsert(), "\nWaiting for Matvey to explain everything")
        self.txtfr1['state'] = 'disabled'


    def __init__(self):
        self.roottk = Tk()
        self.roottk.title("Project console interface :D")

        self.txtfr1 = Text(width=80, wrap='word')
        self.txtfr1.grid(row=0, column=0, sticky='nsew')
        self.txtfr1.insert(AtInsert(), 'Welcome!\n')
        self.txtfr1['state'] = 'disabled'

        self.scrollb = Scrollbar(command=self.txtfr1.yview)
        self.txtfr1['yscrollcommand'] = self.scrollb.set
        self.scrollb.grid(row=0, column=1, sticky='nse')

        self.txtfr2 = Text(height=1)
        self.txtfr2.insert(AtInsert(), "\n")
        self.txtfr2.grid(row=1, column=0, columnspan=2, sticky='sew')
        self.txtfr2.bind('<Return>', self.input_command)

        self.roottk.rowconfigure(0, weight=1)
        self.roottk.columnconfigure(0, weight=1)

        self.txtfr1.after_idle(self.asking_for_information)
        self.roottk.mainloop()
