from tkinter import *
from controller import *
class Besturing(Frame):
    def __init__(self, master, controller, arduinoList):

        #setup the mainframe
        Frame.__init__(self, master)

        for x in range(20):
            self.columnconfigure(x, weight=1)
        for x in range(20):
            self.rowconfigure(x, weight=1)

        self.controller = controller
        self.besturingKnop = Button(master, text="besturing", fg="black", command=self.quit)
        self.besturingKnop.grid(row=0, column=0, columnspan=2)
        self.besturingKnop.config(width=35, height=2)

        self.statistiekenKnop = Button(master, text="statistieken", fg="black", command=Frame.quit)
        self.statistiekenKnop.grid(row=0, column=2, columnspan=1)
        self.statistiekenKnop.config(width=35, height=2)

        def wrapper2(func, args):  # without star
            return func(*args)
        lijst = list(arduinoList.keys())
        if len(lijst)==0:
            lijst[0]="noArduino"
        active_arduino = StringVar(master)
        active_arduino.set(lijst[0])  # default value

        arglist = [master, active_arduino, lijst]
        self.selecteerSchermKnop =wrapper2(OptionMenu, arglist)
        self.selecteerSchermKnop.grid(row=1, column=0, columnspan=1)
        self.selecteerSchermKnop.config(width=15, height=2, )

        self.instellingenKnop = Button(master, text="instellingen", fg="black", command=Frame.quit)
        self.instellingenKnop.grid(row=1, column=1, columnspan=1)
        self.instellingenKnop.config(width=15, height=2)

        def schermOmhoog():
            controller.schermOmhoog(active_arduino.get())
        self.schermOmhoogKnop = Button(master, text="omhoog", fg="black", command=schermOmhoog)
        self.schermOmhoogKnop.grid(row=1, column=2, columnspan=1)
        self.schermOmhoogKnop.config(width=15, height=2)


        self.automatischKnop = Checkbutton(master, text="automatisch")
        self.automatischKnop.grid(row=2, column=2, columnspan=1)
        self.automatischKnop.config(width=15, height=2)

        self.schermOmlaagKnop = Button(master, text="omlaag", fg="black", command=Frame.quit)
        self.schermOmlaagKnop.grid(row=3, column=2, columnspan=1)
        self.schermOmlaagKnop.config(width=15, height=2)


class instellingen(Frame):
    def __init__(self, master):

        #setup the mainframe
        Frame.__init__(self, master)

        for x in range (20):
            self.columnconfigure(x, weight=1)
        for x in range(20):
            self.rowconfigure(x, weight=1)

        self.selecteerSchermKnop = Menubutton(master, text="selecteerScherm", fg="black")
        self.selecteerSchermKnop.grid(row=0, column=0, columnspan=3)
        self.selecteerSchermKnop.config(width=5, height=2)

        self.statistiekenKnop = Button(master, text="statistieken", fg="black", command=Frame.quit)
        self.statistiekenKnop.grid(row=0, column=0, columnspan=3)
        self.statistiekenKnop.config(width=5, height=2)

        self.instellingenKnop = Button(master, text="instellingen", fg="black", command=Frame.quit)
        self.instellingenKnop.grid(row=2, column=2, columnspan=3)
        self.instellingenKnop.config(width=5, height=2)

        self.OkKnop = Button(master, text="omhoog", fg="black", command=Frame.quit)
        self.OkKnop.grid(row=1, column=1, columnspan=3)
        self.OkKnop.config(width=5, height=2)

        self.annuleerKnop = Button(master, text="omlaag", fg="black", command=Frame.quit)
        self.annuleerKnop.grid(row=2, column=3, columnspan=3)
        self.annuleerKnop.config(width=5, height=2)

        self.annuleerKnop = Entry(master, text="omlaag", fg="black", command=Frame.quit)
        self.annuleerKnop.grid(row=2, column=3, columnspan=3)
        self.annuleerKnop.config(width=5, height=2)

class statistieken(Frame):
    def __init__(self, master):

        #setup the mainframe
        Frame.__init__(self, master)

        for x in range (400):
            self.columnconfigure(x, weight=1)
        for x in range(400):
            self.rowconfigure(x, weight=1)

        self.besturingKnop = Button(master, text="statistieken", fg="black", command=Frame.quit)
        self.besturingKnop.grid(row=0, column=0, columnspan=3)
        self.besturingKnop.config(width=5, height=2)

        self.schermKnop = Button(master, text="statistieken", fg="black", command=Frame.quit)
        self.schermKnop.grid(row=0, column=0, columnspan=3)
        self.schermKnop.config(width=5, height=2)

'''''
root = Tk()
root.geometry('550x400+200+200')

besturing = Besturing(root, "bla")
root.mainloop()
'''