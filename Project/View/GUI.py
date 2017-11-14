import time
from tkinter import *
from tkinter import _setit

from Project.Model.controller import *
from Project.View import grafiek


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
        if not isinstance(self.view, Statistieken):
            activeArd = self.view.active_arduino.get()
            if view == 0: #besturing
                self.view = Besturing(self, self.controller)
                self.view.active_arduino.set(activeArd)
                print(self.view.active_arduino.get())
            if view == 1: #instellingen
                self.view = Instellingen(self)
                self.view.active_arduino.set(activeArd)
            if view == 2: #statistieken
                self.view = Statistieken(self)
        if isinstance(self.view, Statistieken):
            if view == 0: #besturing
                self.view = Besturing(self, self.controller)
            if view == 1: #instellingen
                self.view = Instellingen(self)
            if view == 2: #statistieken
                self.view = Statistieken(self)

        self.createScreen()

    def createScreen(self):
        self.view.grid(row=0, column=0)  # besturing toevoegen aan grid
        self.view.config(background="light grey")
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
                    self.view.automatischKnop = Button(self.view, text="automatisch", command=self.view.stopAuto, fg="white", bg="dim gray", activebackground="snow4", activeforeground="white")
                    self.view.automatischKnop.grid(row=5, column=2, columnspan=1)
                    self.view.automatischKnop.config(width=20, height=2)
                    self.view.automatischKnop.config(state=DISABLED)
                    if active_arduino in self.controller.autoArduinoList:
                        self.view.automatischKnop.config(state=NORMAL)
                elif self.view.active_arduino.get() in self.controller.connectedArduinoList:
                    self.view.schermOmhoogKnop.config(state=NORMAL)
                    self.view.schermOmlaagKnop.config(state=NORMAL)
                    self.view.instellingenKnop.config(state=NORMAL)
                    self.view.automatischKnop = Button(self.view, text="automatisch", command=self.view.goAuto, fg="white", bg="dim gray", activebackground="snow4", activeforeground="white")
                    self.view.automatischKnop.grid(row=5, column=2, columnspan=1)
                    self.view.automatischKnop.config(width=20, height=2)

                    self.view.tijd = getTime(self.view.pane)
                    self.view.aantalScherm = aantalSchermen(self.view.pane)
                    self.view.temperatuur = getTemp(self.view.pane)
                    self.view.lichtintensiteit = getLight(self.view.pane)
                    self.view.hoogte = getDistance(self.view.pane)
                updateSelectScherm(self.view, self.controller.arduino_list)
            if isinstance(self.view, Instellingen):
                updateSelectScherm(self.view, self.view.master.controller.arduino_list)
                if self.view.lastArduinoUpdated != self.view.active_arduino.get():
                    self.view.lastArduinoUpdated = self.view.active_arduino.get()
                    self.view.lichtText.set(self.view.master.controller.arduino_list[self.view.active_arduino.get()].get_light_threshold())
                    self.view.hoogteText.set(self.view.master.controller.arduino_list[self.view.active_arduino.get()].get_distance_threshold())
                    self.view.tempText.set(self.view.master.controller.arduino_list[self.view.active_arduino.get()].get_temp_threshold())

                    self.view.tijd = getTime(self.view.pane)
                    self.view.aantalScherm = aantalSchermen(self.view.pane)
                    self.view.temperatuur = getTemp(self.view.pane)
                    self.view.lichtintensiteit = getLight(self.view.pane)
                    self.view.hoogte = getDistance(self.view.pane)
                pass
            if isinstance(self.view, Statistieken):
                self.view.doDaPlotsPlox()
        self.after(1000, self.doUpdate)

# functie voor het doorgeven van parameters
def wrapper1(func, args): #arguments niet in list
    return(func(args))
def wrapper2(func, args):  # args in list
    return func(*args)

# de 2 hoofdbesturingsknoppen
def getNavigationBesturing(frame):
    frame.besturingKnop = Button(frame, text="besturing", fg="white", bg="grey", command=frame.master.updateView0)
    frame.besturingKnop.grid(row=0, column=0, columnspan=1)
    frame.besturingKnop.config(width=35, height=1)

    frame.statistiekenKnop = Button(frame, text="statistieken", fg="black", command=frame.master.updateView2)
    frame.statistiekenKnop.grid(row=0, column=2, columnspan=1)
    frame.statistiekenKnop.config(width=35, height=1)

def getNavigationStatistieken(frame):
    frame.besturingKnop = Button(frame, text="besturing", fg="black", command=frame.master.updateView0)
    frame.besturingKnop.grid(row=0, column=0, columnspan=1)
    frame.besturingKnop.config(width=35, height=1)

    frame.statistiekenKnop = Button(frame, text="statistieken", fg="white", bg="grey", command=frame.master.updateView2)
    frame.statistiekenKnop.grid(row=0, column=2, columnspan=1)
    frame.statistiekenKnop.config(width=35, height=1)

def getNavigationInstellingen(frame):
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
    selecteerSchermKnop.grid(row=0, column=0, columnspan=3, rowspan=1, pady=3, padx=3, ipady=3, ipadx=3, sticky=N) #north west
    selecteerSchermKnop.config(width=15, height=1)
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
    if frame.active_arduino.get()=="noArduino":
        frame.active_arduino.set(lijst[0])  # default value

    for command in lijst:
        try:
            knop['menu'].add_command(label=command, command=_setit(frame.active_arduino, command))
        except:
            print(sys.exc_info())


def getInstellingen(frame):
    instellingenKnop = Button(frame, text="instellingen", fg="black", command=frame.master.updateView1)
    instellingenKnop.grid(row=2, column=2, columnspan=2)
    instellingenKnop.config(width=17, height=1)
    return instellingenKnop

def getTime(frame):
    klokLabel = Label(frame, text="tijd", bg='white')
    klokLabel.grid(row=4, column=0, columnspan=1)
    klokLabel.config(width=15, height=1)

    klok = Label(frame,  bg='white', fg="dim gray")
    klok.grid(row=4, column=2, columnspan=1)
    klok.config(width=15, height=1)

    s = time.strftime('%H:%M:%S')
    if s != klok["text"]:
        klok["text"] = s


def aantalSchermen(frame):
    schermenLabel = Label(frame, text="aantal schermen is" , bg='white')
    schermenLabel.grid(row=5, column=0, columnspan=1)
    schermenLabel.config(width=15, height=1)

    text = str(len(frame.master.master.controller.arduino_list))
    schermen = Label(frame, text=text, bg='white', fg="dim gray")
    schermen.grid(row=5, column=2, columnspan=1)
    schermen.config(width=15, height=1)

def getTemp(frame):
    temperatuurLabel = Label(frame, text="temperatuur", bg='white')
    temperatuurLabel.grid(row=6, column=0, columnspan=1)
    temperatuurLabel.config(width=15, height=1)
    try:
        temperatuur1 = frame.master.master.controller.arduino_list[frame.master.active_arduino.get()].request("get_temp")[1] +"C"
    except:
        temperatuur1 = "temp nvt"
    temperatuur = Label(frame, bg='white', text=temperatuur1, fg="dim gray")
    temperatuur.grid(row=6, column=2, columnspan=1)
    temperatuur.config(width=15, height=1)

    return temperatuur

def getDistance(frame):
    distanceLabel = Label(frame, text="cm uitgerold", bg='white')
    distanceLabel.grid(row=7, column=0, columnspan=1)
    distanceLabel.config(width=15, height=1)

    try:
        distance1 = frame.master.master.controller.arduino_list[frame.master.active_arduino.get()].request("get_distance")[1]+" cm"
    except:
        distance1 = "afstand nvt"
    distance = Label(frame, bg='white', text=distance1, fg="dim gray")
    distance.grid(row=7, column=2, columnspan=1)
    distance.config(width=15, height=1)

    return distance

def getLight(frame):
    lightLabel = Label(frame, text="lichtintensiteit", bg='white')
    lightLabel.grid(row=8, column=0, columnspan=1)
    lightLabel.config(width=15, height=1)

    try:
        light1 = frame.master.master.controller.arduino_list[frame.master.active_arduino.get()].request("get_light")[1][:3] + "lux"
    except:
        light1 = "licht nvt"
    light = Label(frame, bg='white', text=light1, fg="dim gray")
    light.grid(row=8, column=2, columnspan=1)
    light.config(width=15, height=1)

    poep = Label(frame, bg='white')
    poep.grid(row=9, column=2, columnspan=2)
    poep.config(width=15, height=1)

    poepie = Label(frame, bg='white')
    poepie.grid(row=3, column=2, columnspan=2)
    poepie.config(width=15, height=1)

    return light


class Besturing(Frame):
    def __init__(self, master, controller):
        Frame.__init__(self, master)
        self.master = master
        self.arduinoList = controller.arduino_list
        self.active_arduino = None
        self.controller = controller

        getNavigationBesturing(self) # get navigatiebalk

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

        self.pane.grid(row=1, column=0, columnspan=3, rowspan=8, pady=25, padx=10, sticky=NW) #north west

        def schermOmhoog():
            self.controller.schermOmhoog(self.active_arduino.get())
        def schermOmlaag():
            self.controller.schermOmlaag(self.active_arduino.get())

        self.schermOmhoogKnop = Button(self, text="omhoog", fg="white", bg="dim gray", command=schermOmhoog, activebackground="snow4", activeforeground="white")
        self.schermOmhoogKnop.grid(row=4, column=2, columnspan=1)
        self.schermOmhoogKnop.config(width=20, height=2)

        self.schermOmlaagKnop = Button(self, text="omlaag", fg="white", bg="dim gray", command=schermOmlaag, activebackground="snow4", activeforeground="white")
        self.schermOmlaagKnop.grid(row=6, column=2, columnspan=1)
        self.schermOmlaagKnop.config(width=20, height=2)



        if self.active_arduino.get() not in controller.autoArduinoList:
            self.automatischKnop = Button(self, text="automatisch", command=self.goAuto, fg="white", bg="dim gray", activebackground="snow4", activeforeground="white")
            self.automatischKnop.grid(row=5, column=2, columnspan=1)
            self.automatischKnop.config(width=20, height=2)
        else:
            self.automatischKnop = Button(self, text="automatisch", command=self.stopAuto, fg="white", bg="dim gray", activebackground="snow4", activeforeground="white")
            self.automatischKnop.grid(row=5, column=2, columnspan=1)
            self.automatischKnop.config(width=20, height=2)

    def goAuto(self):
        self.schermOmhoogKnop.config(state=DISABLED)
        self.schermOmlaagKnop.config(state=DISABLED)
        self.instellingenKnop.config(state=DISABLED)
        self.automatischKnop = Button(self, text="automatisch", command=self.stopAuto, fg="white", bg="dim gray", activebackground="snow4", activeforeground="white")
        self.automatischKnop.grid(row=5, column=2, columnspan=1)
        self.automatischKnop.config(width=20, height=2)
        self.controller.goAuto(self.active_arduino.get())

    def stopAuto(self):
        self.schermOmhoogKnop.config(state=NORMAL)
        self.schermOmlaagKnop.config(state=NORMAL)
        self.instellingenKnop.config(state=NORMAL)
        self.automatischKnop = Button(self, text="automatisch", command=self.goAuto, fg="white", bg="dim gray", activebackground="snow4", activeforeground="white")
        self.automatischKnop.grid(row=5, column=2, columnspan=1)
        self.automatischKnop.config(width=20, height=2)
        self.controller.stopAuto(self.active_arduino.get())
    def getContent(self):
        return self.content

class Instellingen(Frame):
    def __init__(self, master):
        #setup the mainframe
        Frame.__init__(self, master)

        self.arduinoList = master.controller.findarduino()
        self.active_arduino = None
        getNavigationInstellingen(self)  # get besturing
        self.pane=Frame(self)
        self.pane.grid(row=1, column=0, columnspan=2, sticky=NW) #north west
        self.lastArduinoUpdated = None

        self.pane = Frame(self)
        self.pane.config(background='white')

        self.selectSchermKnop = getSelectScherm(self.pane, self.arduinoList) # 'selecteer scherm' knop
        self.tijd = getTime(self.pane)
        self.aantalScherm = aantalSchermen(self.pane)
        self.temperatuur = getTemp(self.pane)
        self.lichtintensiteit = getLight(self.pane)
        self.hoogte = getDistance( self.pane)

        self.pane.grid(row=1, column=0, columnspan=3, rowspan=8, pady=25, padx=10, sticky=NW) #north west

        def on_button():
            print(self.temperatuurInvul.get())
            self.master.controller.arduino_list[self.active_arduino.get()].set_temp_thres(self.temperatuurInvul.get())
            print(self.hoogteInvul.get())
            self.master.controller.arduino_list[self.active_arduino.get()].set_distance_thres(self.hoogteInvul.get())
            print(self.lichtInvul.get())
            self.master.controller.arduino_list[self.active_arduino.get()].set_light_thres(self.lichtInvul.get())

        self.pane1 = Frame(self)
        self.pane1.config(background='light grey')

        self.tempLabel = Label(self.pane1, text="drempelwaarde voor temperatuur", wraplength=100, bg="light grey")
        self.tempLabel.grid(row=1, column=0)
        self.tempLabel.config(width=15)

        self.gradenLabel = Label(self.pane1, text="°C", height=1, bg="light grey")
        self.gradenLabel.grid(row=1, column=2)
        self.gradenLabel.config(width=5)


        self.tempText = StringVar()
        self.temperatuurInvul = Entry(self.pane1, fg="black", textvariable=self.tempText)
        self.tempText.set(self.master.controller.arduino_list[self.active_arduino.get()].get_temp_threshold())
        self.temperatuurInvul.grid(row=1, column=1, columnspan=1)
        self.temperatuurInvul.config(width=7)

        self.fillerLabel1 = Label(self.pane1, bg="light grey")
        self.fillerLabel1.grid(row=2, column=0, columnspan=3)

        self.cmLabel = Label(self.pane1, text="maximale uitrolstand", height=1, bg="light grey")
        self.cmLabel.grid(row=3, column=0)

        self.hoogteLabel = Label(self.pane1, text="cm", height=1, bg="light grey")
        self.hoogteLabel.grid(row=3, column=2)
        self.hoogteLabel.config(width=5)

        self.hoogteText = StringVar()
        self.hoogteInvul = Entry(self.pane1, fg="black", textvariable=self.hoogteText)
        self.hoogteText.set(self.master.controller.arduino_list[self.active_arduino.get()].get_distance_threshold())
        self.hoogteInvul.grid(row=3, column=1, columnspan=1)
        self.hoogteInvul.config(width=7)

        self.fillerLabel1 = Label(self.pane1, bg="light grey")
        self.fillerLabel1.grid(row=4, column=0, columnspan=3)

        self.lichtLabel = Label(self.pane1, text="drempelwaarde voor licht", wraplength=100, bg="light grey")
        self.lichtLabel.grid(row=5, column=0)
        self.lichtLabel.config(width=15)

        self.luxLabel = Label(self.pane1, text="lux", height=1, bg="light grey")
        self.luxLabel.grid(row=5, column=2)
        self.luxLabel.config(width=5)

        self.lichtText = StringVar()
        self.lichtInvul = Entry(self.pane1, fg="black", textvariable=self.lichtText)
        self.lichtText.set(self.master.controller.arduino_list[self.active_arduino.get()].get_light_threshold())
        self.lichtInvul.grid(row=5, column=1, columnspan=1)
        self.lichtInvul.config(width=7)

        self.fillerLabel1 = Label(self.pane1, bg="light grey")
        self.fillerLabel1.grid(row=6, column=3, columnspan=3)

        self.enterKnop = Button(self.pane1, text="Invoeren", fg="white", bg="dim gray", command=on_button)
        self.enterKnop.grid(row=7, column=0, columnspan=1)
        self.enterKnop.config(width=8, height=1)

        self.annuleerKnop = Button(self.pane1, text="Annuleer", fg="white", bg="dim gray", command=master.updateView0)
        self.annuleerKnop.grid(row=7, column=1, columnspan=1)
        self.annuleerKnop.config(width=8, height=1)

        self.pane1.grid(row=1, column=1, columnspan=3, rowspan=8, pady=25, padx=10, sticky=NW)  # north west


class Statistieken(Frame):
    def __init__(self, master):
        #setup the mainframe
        Frame.__init__(self, master)
        self.listje ={}
        getNavigationStatistieken(self)  # get besturing
        self.grafiek = None
        self.plotList = []
        self.plotListLength = 0

    def doDaPlotsPlox(self):
        try:
            for x in self.plotList:
                x.canvas.grid_forget
            self.plotList=[]
            number = 1
            for ardport in self.master.controller.connectedArduinoList:
                self.master.controller.connectedArduinoList[ardport].set_type()
                if self.master.controller.connectedArduinoList[ardport].type !=1:
                    self.createPlotsTemp(ardport, self.master.controller, number)
                else:
                    self.createPlotsLight(ardport, self.master.controller, number)
                number += 1
        except:
            self.master.updateView2()


    def createPlotsTemp(self, arduino, controller, number):

        plotframe = Frame(self)
        if number == 1:
            plotframe.grid(column=0, row=1, columnspan=3)
        if number == 2:
            plotframe.grid(column=3, row=1, columnspan=3)
        if number == 3:
            plotframe.grid(column=0, row=2, columnspan=3)
        if number == 4:
            plotframe.grid(column=3, row=2, columnspan=3)

        label = Label(plotframe, text=arduino)
        label.grid(column=0, row=0)
        label = Label(plotframe, text='graden Celcius')
        label.grid(column=0, row=1)
        cmLabel = Label(plotframe, text="cm", height=1)
        cmLabel.grid(row=2, column=0)

        label = Label(plotframe, text=arduino)
        label.grid(column=0, row=0)
        plot = self.setTempPlot(arduino, controller, plotframe)
        plot.canvas.grid(column=1, row=1, columnspan=4)
        plot2 = self.setDistPlot(arduino, controller, plotframe)
        plot2.canvas.grid(column=1, row=2, columnspan=4)


    def createPlotsLight(self, arduino, controller, number):
        plotframe = Frame(self)
        if number == 1:
            plotframe.grid(column=0, row=1, columnspan=3)
        if number == 2:
            plotframe.grid(column=3, row=1, columnspan=3)
        if number == 3:
            plotframe.grid(column=0, row=2, columnspan=3)
        if number == 4:
            plotframe.grid(column=3, row=2, columnspan=3)
        label = Label(plotframe, text=arduino)
        label.grid(column=0, row=0)
        label = Label(plotframe, text='lux')
        label.grid(column=0, row=1)
        cmLabel = Label(plotframe, text="cm", height=1)
        cmLabel.grid(row=2, column=0)
        plot = self.setLightPlot(arduino, controller, plotframe)
        plot.canvas.grid(column=1, row=1, columnspan=4)
        plot2 = self.setDistPlot(arduino, controller, plotframe)
        plot2.canvas.grid(column=1, row=2, columnspan=4)

    def setTempPlot(self, arduino, controller, master):
        lijst = self.getTempHistory(arduino, controller)
        if not len(lijst)<1:
            plot = grafiek.Plot(master, lijst)
            self.plotList.append(plot)
            return plot

    def getTempHistory(self,arduino,controller):
        self.listje = controller.arduino_list[arduino].temperature_history
        return self.listje

    def setLightPlot(self, arduino, controller, master):
        lijst = self.getLightHistory(arduino, controller)
        #
        # #print(lijst)
        if not len(lijst)<1:
            plot = grafiek.Plot(master, lijst, light=1)
            self.plotList.append(plot)
            return plot

    def getLightHistory(self,arduino,controller):
        self.listje = controller.arduino_list[arduino].light_history
        return self.listje

    def setDistPlot(self, arduino, controller, master):
        lijst = self.getDistHistory(arduino, controller)
        #print(len(lijst))
        if not len(lijst)<1:
            plot = grafiek.Plot(master, lijst)
            self.plotList.append(plot)
            return plot

    def getDistHistory(self,arduino,controller):
        self.listje = controller.arduino_list[arduino].distance_history
        return self.listje
