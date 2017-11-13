from tkinter import *
from tkinter import _setit
from controller import *
import time
import grafiek

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

    def doUpdate(self):
        self.controller.update()
        self.update()

        if hasattr(self, 'view'):
            if isinstance(self.view, Besturing):
                active_arduino = self.view.active_arduino.get()
                if active_arduino not in self.controller.connectedArduinoList:
                    self.view.schermOmhoogKnop.config(state=DISABLED)
                    self.view.schermOmlaagKnop.config(state=DISABLED)
                    self.view.instellingenKnop.config(state=DISABLED)
                    self.view.automatischKnop = Button(self.view, text="automatisch", command=self.view.stopAuto)
                    self.view.automatischKnop.grid(row=6, column=2, columnspan=1)
                    self.view.automatischKnop.config(width=15, height=1)
                    self.view.automatischKnop.config(state=DISABLED)
                    if active_arduino in self.controller.autoArduinoList:
                        self.view.automatischKnop.config(state=NORMAL)
                elif self.view.active_arduino.get() in self.controller.connectedArduinoList:
                    self.view.schermOmhoogKnop.config(state=NORMAL)
                    self.view.schermOmlaagKnop.config(state=NORMAL)
                    self.view.instellingenKnop.config(state=NORMAL)
                    self.view.automatischKnop = Button(self.view, text="automatisch", command=self.view.goAuto)
                    self.view.automatischKnop.grid(row=3, column=2, columnspan=1)
                    self.view.automatischKnop.config(width=15, height=2)
                updateSelectScherm(self.view, self.controller.arduino_list)
            if isinstance(self.view, Instellingen):
                pass
            if isinstance(self.view, Statistieken):
                #self.view
                pass
        self.after(100, self.doUpdate)

# functie voor het doorgeven van parameters
def wrapper1(func, args): #arguments niet in list
    return(func(args))
def wrapper2(func, args):  # args in list
    return func(*args)

# de 2 hoofdbesturingsknoppen
def getNavigation(frame):
    frame.besturingKnop = Button(frame, text="besturing", fg="black", command=frame.master.updateView0)
    frame.besturingKnop.grid(row=0, column=0, columnspan=1)
    frame.besturingKnop.config(width=35, height=1)

    frame.statistiekenKnop = Button(frame, text="statistieken", fg="black", command=frame.master.updateView2)
    frame.statistiekenKnop.grid(row=0, column=2, columnspan=1)
    frame.statistiekenKnop.config(width=35, height=1)

def getSelectScherm(frame, arduinoList):
    # lijstje maken met aangesloten arduino poorten
    lijst = list(arduinoList)
    if len(lijst) == 0:
        lijst = ["noArduino"]

    # variabel met de actieve arduino(wordt aangepast door de OtionMenu(dropdown
    frame.master.active_arduino = StringVar(frame)
    frame.master.active_arduino.set(lijst[0])  # default value

    arglist = [frame, frame.master.active_arduino, lijst]  # lijstje met parameters
    selecteerSchermKnop = wrapper2(OptionMenu, arglist)
    selecteerSchermKnop.grid(row=0, column=0, columnspan=1, rowspan=1, sticky=NW) #north west
    selecteerSchermKnop.config(width=15, height=2,)
    return selecteerSchermKnop

def updateSelectScherm(frame, arduinoList):
    knop = frame.selectSchermKnop

    # lijstje maken met aangesloten arduino poorten
    lijst = list(arduinoList.keys())
    if len(lijst) == 0:
        lijst = ["noArduino"]

    # variabel met de actieve arduino(wordt aangepast door de OtionMenu(dropdown
    try:
        knop['menu'].delete(0, 'end')
    except:
        print(sys.exc_info())
    frame.active_arduino.set(lijst[0])  # default value

    for command in lijst:
        try:
            knop['menu'].add_command(label=command, command=_setit(frame.active_arduino, command))
        except:
            print(sys.exc_info())


def getInstellingen(frame):
    instellingenKnop = Button(frame, text="instellingen", fg="black", command=frame.master.updateView1)
    instellingenKnop.grid(row=1, column=2, columnspan=1)
    instellingenKnop.config(width=15, height=1)
    return instellingenKnop

def getTime(frame):
    klokLabel = Label(frame, text="tijd", bg='white')
    klokLabel.grid(row=3, column=0, columnspan=1)
    klokLabel.config(width=15, height=1)

    klok = Label(frame,  bg='white')
    klok.grid(row=3, column=1, columnspan=1)
    klok.config(width=15, height=1)

    s = time.strftime('%H:%M:%S')
    if s != klok["text"]:
        klok["text"] = s
    klok.after(200, getTime)

def aantalSchermen(frame):
    schermenLabel = Label(frame, text="aantal schermen is" , bg='white')
    schermenLabel.grid(row=4, column=0, columnspan=1)
    schermenLabel.config(width=15, height=1)

    schermen = Label(frame, text="0" , bg='white')
    schermen.grid(row=4, column=1, columnspan=1)
    schermen.config(width=15, height=1)

def getTemp(frame):
    temperatuurLabel = Label(frame, text="temperatuur", bg='white')
    temperatuurLabel.grid(row=5, column=0, columnspan=1)
    temperatuurLabel.config(width=15, height=1)

    temperatuur1 =   frame.master.master.controller.arduino_list[frame.master.active_arduino.get()].sendCommand("get_temp")[1]
    temperatuur = Label(frame, bg='white', text=temperatuur1)
    temperatuur.grid(row=5, column=1, columnspan=1)
    temperatuur.config(width=15, height=1)


    return temperatuur1

def getDistance(frame):
    distanceLabel = Label(frame, text="hoogte", bg='white')
    distanceLabel.grid(row=6, column=0, columnspan=1)
    distanceLabel.config(width=15, height=1)

    distance = Label(frame, bg='white')
    distance.grid(row=6, column=1, columnspan=1)
    distance.config(width=15, height=1)

    distance1 = frame.master.master.controller.arduino_list[frame.master.active_arduino.get()].sendCommand("get_distance")[1]
    return distance1

def getLight(frame):
    lightLabel = Label(frame, text="lichtintensiteit", bg='white')
    lightLabel.grid(row=7, column=0, columnspan=1)
    lightLabel.config(width=15, height=1)

    light = Label(frame, bg='white')
    light.grid(row=7, column=1, columnspan=1)
    light.config(width=15, height=1)

    light1 = frame.master.master.controller.arduino_list[frame.master.active_arduino.get()].sendCommand("get_light")[1]
    return light1


class Besturing(Frame):
    def __init__(self, master, controller):
        Frame.__init__(self, master)
        self.master = master
        self.arduinoList = controller.arduino_list
        self.active_arduino = None
        self.controller = controller

        getNavigation(self) # get navigatiebalk

        self.pane = Frame(self)
        self.pane.config(background='white')

        #display
        self.selectSchermKnop = getSelectScherm(self.pane, self.arduinoList) # 'selecteer scherm' knop
        self.tijd = getTime(self.pane)
        self.aantalScherm = aantalSchermen(self.pane)
        self.temperatuur = getTemp(self.pane)
        self.lichtintensiteit = getLight(self.pane)
        self.hoogte = getDistance( self.pane)

        self.instellingenKnop = getInstellingen(self)                    # 'instellingen' knop
        self.pane.grid(row=1, column=0, columnspan=2, rowspan=6, sticky=NW) #north west
        self.pane.grid(row=1, column=0, columnspan=2, rowspan=7, sticky=NW) #north west

        def schermOmhoog():
            self.controller.schermOmhoog(self.active_arduino.get())
        def schermOmlaag():
            self.controller.schermOmlaag(self.active_arduino.get())

        self.schermOmhoogKnop = Button(self, text="omhoog", fg="black", command=schermOmhoog)
        self.schermOmhoogKnop.grid(row=3, column=2, columnspan=1)
        self.schermOmhoogKnop.config(width=15, height=1)

        self.schermOmlaagKnop = Button(self, text="omlaag", fg="black", command=schermOmlaag)
        self.schermOmlaagKnop.grid(row=9, column=2, columnspan=1)
        self.schermOmlaagKnop.config(width=15, height=1)



        if self.active_arduino.get() not in controller.autoArduinoList:
            self.automatischKnop = Button(self, text="automatisch", command=self.goAuto)
            self.automatischKnop.grid(row=6, column=2, columnspan=1)
            self.automatischKnop.config(width=15, height=1)
        else:
            self.automatischKnop = Button(self, text="automatisch", command=self.stopAuto)
            self.automatischKnop.grid(row=6, column=2, columnspan=1)
            self.automatischKnop.config(width=15, height=1)

    def goAuto(self):
        self.schermOmhoogKnop.config(state=DISABLED)
        self.schermOmlaagKnop.config(state=DISABLED)
        self.instellingenKnop.config(state=DISABLED)
        self.automatischKnop = Button(self, text="automatisch", command=self.stopAuto)
        self.automatischKnop.grid(row=6, column=2, columnspan=1)
        self.automatischKnop.config(width=15, height=1)
        self.controller.goAuto(self.active_arduino.get())

    def stopAuto(self):
        self.schermOmhoogKnop.config(state=NORMAL)
        self.schermOmlaagKnop.config(state=NORMAL)
        self.instellingenKnop.config(state=NORMAL)
        self.automatischKnop = Button(self, text="automatisch", command=self.goAuto)
        self.automatischKnop.grid(row=6, column=2, columnspan=1)
        self.automatischKnop.config(width=15, height=1)
        self.controller.stopAuto(self.active_arduino.get())
    def getContent(self):
        return self.content

class Instellingen(Frame):
    def __init__(self, master):
        #setup the mainframe
        Frame.__init__(self, master)

        self.arduinoList = master.controller.findarduino()
        self.active_arduino = None
        getNavigation(self)  # get besturing
        self.pane=Frame(self)
        getSelectScherm(self.pane, self.arduinoList)
        self.pane.grid(row=1, column=0, columnspan=2, sticky=NW) #north west
        def on_button():
            print(self.temperatuurInvul.get())
            self.master.controller.arduino_list[self.active_arduino.get()].set_temp_thres(self.temperatuurInvul.get())
            print(self.hoogteInvul.get())
            self.master.controller.arduino_list[self.active_arduino.get()].set_distance_thres(self.hoogteInvul.get())
            print(self.lichtInvul.get())
            self.master.controller.arduino_list[self.active_arduino.get()].set_light_thres(self.lichtInvul.get())

        self.tempLabel = Label(self, text="drempelwaarde voor temperatuur", wraplength=100)
        self.tempLabel.grid(row=1, column =2)
        self.temperatuurInvul = Entry(self, fg="black")
        self.temperatuurInvul.grid(row=1, column=3, columnspan=1)
        self.temperatuurInvul.insert(0,self.master.controller.arduino_list[self.active_arduino.get()].get_temp_threshold())
        self.temperatuurInvul.config(width=10)

        self.fillerLabel1 = Label(self)
        self.fillerLabel1.grid(row=2, column=3, columnspan=2)

        self.hoogteLabel = Label(self, text="maximale uitrolstand", height=1)
        self.hoogteLabel.grid(row=3, column=2)
        self.hoogteInvul = Entry(self, fg="black")
        self.hoogteInvul.insert(0, self.master.controller.arduino_list[self.active_arduino.get()].get_distance_threshold())
        self.hoogteInvul.grid(row=3, column=3, columnspan=1)
        self.hoogteInvul.config(width=15)

        self.fillerLabel1 = Label(self)
        self.fillerLabel1.grid(row=4, column=3, columnspan=2)

        self.lichtLabel = Label(self, text="drempelwaarde voor licht", wraplength=100)
        self.lichtLabel.grid(row=5, column=2)
        self.lichtInvul = Entry(self, fg="black")
        self.lichtInvul.grid(row=5, column=3, columnspan=1)
        self.lichtInvul.insert(0,self.master.controller.arduino_list[self.active_arduino.get()].get_light_threshold())
        self.lichtInvul.config(width=15)

        self.fillerLabel1 = Label(self)
        self.fillerLabel1.grid(row=6, column=3, columnspan=2)

        self.enterKnop = Button(self, text="Okto", fg="black", command=on_button)
        self.enterKnop.grid(row=7, column=2, columnspan=1)
        self.enterKnop.config(width=15, height=2)

        self.annuleerKnop = Button(self, text="annuleer", fg="black", command=master.updateView0)
        self.annuleerKnop.grid(row=7, column=3, columnspan=1)
        self.annuleerKnop.config(width=15, height=2)

class Statistieken(Frame):
    def __init__(self, master):
        #setup the mainframe
        Frame.__init__(self, master)
        self.listje ={}
        getNavigation(self)  # get besturing
        self.setPlot('COM10', self.master.controller)
        self.grafiek = None
        if(len(self.listje)>0):
           self.grafiek=grafiek.Plot(self, self.listje)

    def setPlot(self, arduino, controller):
        lijst = self.getTempHistory(arduino, controller)
        if not len(lijst)<1:
            self.grafiek = grafiek.Plot(self, lijst)

    def getTempHistory(self,arduino,controller):
        self.listje = controller.arduino_list[arduino].temperature_history
        print(self.listje)
        return self.listje
