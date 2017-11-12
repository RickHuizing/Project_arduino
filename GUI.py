from tkinter import *
from controller import *

class MainView(Tk):
    def __init__(self, controller):
        Tk.__init__(self) #dit is het main scherm
        self.controller = controller # controller
        self.view = Frame(self)
        self.view = Besturing(self, self.controller) # de besturings view
        self.view.grid(row=0, column=0) # besturing toevoegen aan grid
        self.updateView(0)

    def updateView0(self):
        self.updateView(0)
    def updateView1(self):
        self.updateView(1)
    def updateView2(self):
        self.updateView(2)
    def updateView(self, view):
        self.view.destroy()
        if view == 0: #besturing
            self.view = Besturing(self, self.controller)
        if view == 1: #instellingen
            self.view = Instellingen(self)
        if view == 2: #statistieken
            self.view = Statistieken(self)
        self.createScreen()

    def createScreen(self):
        self.view.grid(row=0, column=0)  # besturing toevoegen aan grid
        self.view.config(background="grey")
        self.update()

# functie voor het doorgeven van parameters
def wrapper1(func, args): #arguments niet in list
    return(func(args))
def wrapper2(func, args):  # args in list
    return func(*args)

# de 2 hoofdbesturingsknoppen
def getNavigation(frame):
    frame.besturingKnop = Button(frame, text="besturing", fg="black", command=frame.master.updateView0)
    frame.besturingKnop.grid(row=0, column=0, columnspan=2)
    frame.besturingKnop.config(width=35, height=2)

    frame.statistiekenKnop = Button(frame, text="statistieken", fg="black", command=frame.master.updateView2)
    frame.statistiekenKnop.grid(row=0, column=2, columnspan=1)
    frame.statistiekenKnop.config(width=35, height=2)

def getSelectScherm(frame, arduinoList):
    # lijstje maken met aangesloten arduino poorten
    lijst = list(arduinoList.keys())
    if len(lijst) == 0:
        lijst = ["noArduino"]

    # variabel met de actieve arduino(wordt aangepast door de OtionMenu(dropdown
    frame.master.active_arduino = StringVar(frame)
    frame.master.active_arduino.set(lijst[0])  # default value

    arglist = [frame, frame.master.active_arduino, lijst]  # lijstje met parameters
    frame.selecteerSchermKnop = wrapper2(OptionMenu, arglist)
    frame.selecteerSchermKnop.grid(row=1, column=0, columnspan=1)
    frame.selecteerSchermKnop.config(width=15, height=2, )

def getInstellingen(frame):
    frame.instellingenKnop = Button(frame, text="instellingen", fg="black", command=frame.master.updateView1)
    frame.instellingenKnop.grid(row=1, column=2, columnspan=1)
    frame.instellingenKnop.config(width=15, height=2)

class Besturing(Frame):
    def __init__(self, master, controller):
        Frame.__init__(self, master)
        self.master = master
        self.arduinoList = controller.getConnectedArduinolist()
        active_arduino = None
        self.controller = controller

        getNavigation(self) # get navigatiebalk

        self.pane = Frame(self)
        self.pane.config(background='white')

        getSelectScherm(self.pane, self.arduinoList) # 'selecteer scherm' knop
        getInstellingen(self)                    # 'instellingen' knop
        self.pane.grid(row=1, column=0, columnspan=2, rowspan=1)

        def schermOmhoog():
            self.controller.schermOmhoog(self.active_arduino.get())
        def schermOmlaag():
            self.controller.schermOmlaag(self.active_arduino.get())
        self.schermOmhoogKnop = Button(self, text="omhoog", fg="black", command=schermOmhoog)
        self.schermOmhoogKnop.grid(row=2, column=2, columnspan=1)
        self.schermOmhoogKnop.config(width=15, height=2)


        self.automatischKnop = Checkbutton(self, text="automatisch")
        self.automatischKnop.grid(row=3, column=2, columnspan=1)
        self.automatischKnop.config(width=15, height=2)

        self.schermOmlaagKnop = Button(self, text="omlaag", fg="black", command=schermOmlaag)
        self.schermOmlaagKnop.grid(row=4, column=2, columnspan=1)
        self.schermOmlaagKnop.config(width=15, height=2)

    def getContent(self):
        return self.content

class Instellingen(Frame):
    def __init__(self, master):
        #setup the mainframe
        Frame.__init__(self, master)

        self.arduinoList = master.controller.getConnectedArduinolist()

        getNavigation(self)  # get besturing

        getSelectScherm(self, self.arduinoList)

        self.OkKnop = Button(self, text="ok", fg="black", command=Frame.quit)
        self.OkKnop.grid(row=1, column=1, columnspan=3)
        self.OkKnop.config(width=15, height=2)

        self.annuleerKnop = Button(self, text="annuleer", fg="black", command=master.updateView0)
        self.annuleerKnop.grid(row=2, column=1, columnspan=3)
        self.annuleerKnop.config(width=15, height=2)

        self.temperatuurInvul = Entry(self, text="vul temp", fg="black") #yolo
        self.temperatuurinvul.grid(row=3, column=1, columnspan=3)
        self.temperatuurinvul.config(width=15, height=2)

class Statistieken(Frame):
    def __init__(self, master):
        #setup the mainframe
        Frame.__init__(self, master)


        getNavigation(self)  # get besturing