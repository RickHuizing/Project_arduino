from tkinter import *
from controller import *

class MainView(Tk):
    def __init__(self, controller):
        Tk.__init__(self) #dit is het main scherm
        self.controller = controller # controller
        self.besturing = Besturing(self, self.controller) # de besturings view
        self.besturing.grid(row=0, column=0) # besturing toevoegen aan grid

        self.instellingen = instellingen(self)
        self.instellingen.grid(row=1)


class Besturing(Frame):
    def __init__(self, master, controller):
        Frame.__init__(self, master)
        self.arduinoList = controller.getConnectedArduinolist()
        #self.content = Frame(master)
        #self.content.grid(row=0, column=0, columnspan=2)
        self.controller = controller

        self.besturingKnop = Button(self, text="besturing", fg="black", command=Frame.quit)
        self.besturingKnop.grid(row=0, column=0, columnspan=2)
        self.besturingKnop.config(width=35, height=2)

        self.statistiekenKnop = Button(self, text="statistieken", fg="black", command=Frame.quit)
        self.statistiekenKnop.grid(row=0, column=2, columnspan=1)
        self.statistiekenKnop.config(width=35, height=2)

        # functie voor het doorgeven van parameters
        def wrapper2(func, args):  # without star
            return func(*args)

        # lijstje maken met aangesloten arduino poorten
        lijst = list(self.arduinoList.keys())
        if len(lijst) == 0:
            lijst = ["noArduino"]

        # variabel met de actieve arduino(wordt aangepast door de OtionMenu(dropdown
        active_arduino = StringVar(self)
        active_arduino.set(lijst[0])  # default value
        print("hoi2")
        arglist = [self, active_arduino, lijst]  # lijstje met parameters
        self.selecteerSchermKnop = wrapper2(OptionMenu, arglist)
        self.selecteerSchermKnop.grid(row=1, column=0, columnspan=1)
        self.selecteerSchermKnop.config(width=15, height=2, )

        self.instellingenKnop = Button(self, text="instellingen", fg="black", command=Frame.quit)
        self.instellingenKnop.grid(row=1, column=1, columnspan=1)
        self.instellingenKnop.config(width=15, height=2)

        def schermOmhoog():
            controller.schermOmhoog(active_arduino.get())
        self.schermOmhoogKnop = Button(self, text="omhoog", fg="black", command=schermOmhoog)
        self.schermOmhoogKnop.grid(row=1, column=2, columnspan=1)
        self.schermOmhoogKnop.config(width=15, height=2)


        self.automatischKnop = Checkbutton(self, text="automatisch")
        self.automatischKnop.grid(row=2, column=2, columnspan=1)
        self.automatischKnop.config(width=15, height=2)

        self.schermOmlaagKnop = Button(self, text="omlaag", fg="black", command=Frame.quit)
        self.schermOmlaagKnop.grid(row=3, column=2, columnspan=1)
        self.schermOmlaagKnop.config(width=15, height=2)

    def getContent(self):
        return self.content

class instellingen(Frame):
    def __init__(self, master):

        #setup the mainframe
        Frame.__init__(self, master)

        for x in range (20):
            self.columnconfigure(x, weight=1)
        for x in range(20):
            self.rowconfigure(x, weight=1)

        self.selecteerSchermKnop = Menubutton(self, text="selecteerScherm", fg="black")
        self.selecteerSchermKnop.grid(row=0, column=0, columnspan=2)
        self.selecteerSchermKnop.config(width=15, height=2)

        self.statistiekenKnop = Button(self, text="statistieken", fg="black", command=Frame.quit)
        self.statistiekenKnop.grid(row=0, column=3, columnspan=1)
        self.statistiekenKnop.config(width=15, height=2)

        self.instellingenKnop = Button(self, text="instellingen", fg="black", command=Frame.quit)
        self.instellingenKnop.grid(row=2, column=1, columnspan=3)
        self.instellingenKnop.config(width=15, height=2)

        self.OkKnop = Button(self, text="omhoog", fg="black", command=Frame.quit)
        self.OkKnop.grid(row=1, column=1, columnspan=3)
        self.OkKnop.config(width=15, height=2)

        self.annuleerKnop = Button(self, text="omlaag", fg="black", command=Frame.quit)
        self.annuleerKnop.grid(row=2, column=1, columnspan=3)
        self.annuleerKnop.config(width=15, height=2)


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