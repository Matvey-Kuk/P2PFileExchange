
"""
Здесь будет реализация консольного интерфейса программы.
"""

from tkinter import *
from tkinter.ttk import *


class Interface(object):

    __output_callbacks = {}
    __commands_processors_callbacks = {}

    def __init__(self):

        self.Info_labels = {}
        self.previous_commands = []
        self.current_command_number = 0

        self.roottk = Tk()
        self.roottk.title("Project console interface :D")
        self.roottk.minsize(256, 128)

        self.frameInfo = Frame()
        self.frameTBox = Frame()
        self.frameCommandLine = Frame()

        self.txtfr1 = Text(self.frameTBox, wrap='word')
        self.txtfr1.grid(row=0, column=0, sticky='nsew')
        self.txtfr1.insert('end', 'Welcome!\n')
        self.txtfr1['state'] = 'disabled'

        self.scrollb = Scrollbar(self.frameTBox, command=self.txtfr1.yview)
        self.txtfr1['yscrollcommand'] = self.scrollb.set
        self.scrollb.grid(row=0, column=1, sticky='nse')

        self.frameTBox.rowconfigure(0, weight=1)
        self.frameTBox.columnconfigure(0, weight=1)

        self.txtfr2 = Text(self.frameCommandLine, height=1)
        self.txtfr2.insert('end', "\n")
        self.txtfr2.grid(row=0, column=0, sticky='sew')
        self.txtfr2.bind('<Return>', self.input_command)
        self.txtfr2.bind('<Up>', self.input_up_command)
        self.txtfr2.bind('<Down>', self.input_down_command)

        self.b_input = Button(self.frameCommandLine, text='OK', width=20, command=self.input_command)
        self.b_input.grid(row=0, column=1, sticky='sew')

        self.frameCommandLine.rowconfigure(0, weight=1)
        self.frameCommandLine.columnconfigure(0, weight=1)

        self.frameInfo.grid(row=0, column=0, sticky='nswe')
        self.frameTBox.grid(row=1, column=0, sticky='nsew')
        self.frameCommandLine.grid(row=2, column=0, sticky='nsew')

        self.roottk.columnconfigure(0, weight=1)
        self.roottk.rowconfigure(1, weight=1)
        #self.roottk.rowconfigure(2, weight=0)

        i = -1
        for prefix in self.__output_callbacks.keys():
            i += 1
            self.Info_labels[prefix] = Label(self.frameInfo, anchor='center')
            self.Info_labels[prefix].grid(row=0, column=i, sticky='nsew')
        self.frameInfo.columnconfigure(i, weight=1)

        self.txtfr1.after_idle(self.asking_for_information)
       # self.roottk.after(100, self.roottk.mainloop())

    def input_command(self, *event):
        """Обработчик введённых команд"""
        s = self.txtfr2.get('1.0', 'end')
        self.txtfr2.delete('1.0', 'end')

        self.txtfr1['state'] = 'normal'
        s = s.strip()
        self.txtfr1.insert('end', "\n" + s)
        self.txtfr1.yview_moveto(1.0)

        self.previous_commands.append(s)

        input_words = s.split(None, 1)

        try:
            str = Interface.__commands_processors_callbacks[input_words[0].lower()](input_words[1])
            self.txtfr1.insert('end', "\n" + str)
            self.txtfr1.yview_moveto(1.0)
        except:
            self.txtfr1.insert('end', "\n" + "Undefined command (prefix)")
            self.txtfr1.yview_moveto(1.0)

        self.txtfr1['state'] = 'disabled'
        self.current_command_number = len(self.previous_commands)

    def input_up_command(self, event):
        if self.current_command_number:
            self.current_command_number -= 1
        self.txtfr2.delete('1.0', 'end')
        self.txtfr2.insert('end', self.previous_commands[self.current_command_number])

    def input_down_command(self, event):
        if self.current_command_number < len(self.previous_commands) - 1:
            self.current_command_number += 1
        self.txtfr2.delete('1.0', 'end')
        self.txtfr2.insert('end', self.previous_commands[self.current_command_number])

    def asking_for_information(self):
        """Метод, опрашивающий поставщиков данных"""
        self.txtfr1.after(1000, self.asking_for_information)
        #self.txtfr1['state'] = 'normal'
        if not self.Info_labels:
            self.txtfr1.insert('end', "\nno data")
        for prefix in self.Info_labels.keys():
            str = Interface.__output_callbacks[prefix]()
            #self.txtfr1.insert('end', "\n%s" % str)
            self.Info_labels[prefix]['text'] = str
        #self.txtfr1['state'] = 'disabled'

    @staticmethod
    def register_output_callback(prefix, callback):
        """Здесь должны регистрироваться коллбэки функций, которые будут выводить на монитор данные в реалтайме"""
        Interface.__output_callbacks[prefix.lower()] = callback

    @staticmethod
    def register_command_processor_callback(prefix, callback):
        """Здесь регистрируются коллбэки функций, которые обрабатывают команды"""
        Interface.__commands_processors_callbacks[prefix.lower()] = callback
