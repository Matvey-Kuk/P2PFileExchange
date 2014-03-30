
"""
Здесь будет реализация консольного интерфейса программы.
"""

from tkinter import *
from tkinter.ttk import *

class Interface(object):

    def __init__(self):
        self.data_senders = []

        self.roottk = Tk()
        self.roottk.title("Project console interface :D")
        self.roottk.minsize(256, 128)

        self.frameInfo = Frame()
        self.frameCommandLine = Frame()

        self.txtfr1 = Text(self.frameCommandLine, wrap='word')
        self.txtfr1.grid(row=1, column=0, sticky='nsew')
        self.txtfr1.insert(AtInsert(), 'Welcome!\n')
        self.txtfr1['state'] = 'disabled'

        self.scrollb = Scrollbar(self.frameCommandLine, command=self.txtfr1.yview)
        self.txtfr1['yscrollcommand'] = self.scrollb.set
        self.scrollb.grid(row=1, column=1, sticky='nse')

        self.txtfr2 = Text(self.frameCommandLine, height=1)
        self.txtfr2.insert(AtInsert(), "\n")
        self.txtfr2.grid(row=2, column=0, columnspan=2, sticky='sew')
        self.txtfr2.bind('<Return>', self.input_command)

        self.frameCommandLine.rowconfigure(1, weight=1)
        self.frameCommandLine.columnconfigure(0, weight=1)

        self.frameInfo.grid(row=0, column=0, sticky='nswe')
        self.frameCommandLine.grid(row=1, column=0, sticky='nsew')

        self.roottk.columnconfigure(0, weight=1)
        self.roottk.rowconfigure(1, weight=1)


        self.txtfr1.after_idle(self.asking_for_information)
       # self.roottk.after(100, self.roottk.mainloop())

    def input_command(self, event):
        s = self.txtfr2.get('1.0', 'end')
        self.txtfr2.delete('1.0', 'end')
        self.txtfr1['state'] = 'normal'
        s = s.strip()
        self.txtfr1.insert('end',"\n" + s)
        self.txtfr1.yview_moveto(1.0)
        input_words = s.split()
        self.txtfr1['state'] = 'disabled'

    def register_data_sender(self, *data_senders):
        for data_sender in data_senders:
            if hasattr(data_sender, "send_data_to_interface"):
                ds = []
                ds.append(data_sender)
                print("Object of type %s was registered" % type(data_sender))
                ds.append(Label(self.frameInfo, anchor='center'))
                self.data_senders.append(ds)
                n = len(self.data_senders) - 1
                ds[1].grid(row=0, column=n, sticky='nsew')
                self.frameInfo.columnconfigure(n, weight=1)
            else:
                print("Object of type %s has no method to send data" % type(data_sender))

    def asking_for_information(self):
        self.txtfr1.after(1000, self.asking_for_information)
        self.txtfr1['state'] = 'normal'
        if not self.data_senders:
            self.txtfr1.insert('end', "\nno data")
        for o in self.data_senders:
            str = o[0].send_data_to_interface()
            self.txtfr1.insert('end', "\n%s" % str)
            o[1]['text'] = str
        self.txtfr1['state'] = 'disabled'


