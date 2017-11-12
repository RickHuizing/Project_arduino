import arduino
import sys
import time
from serial.tools import list_ports_windows

# bevat een lijst met aangesloten arduino's en functies om de arduino's aan te sturen
class Controller:
    def __init__(self):
        self.views = 0
        # dictionary met arduino's, key="COM#portnumber", value=arduino
        self.arduino_list = {}
        # lijst met actieve arduino's(deze zijn aangesloten), wordt op dezelfde manier gebruikt als arduino_list
        self.connectedArduinoList = {}
        # lijst met arduino's waarvan de verbinding verbroken is
        self.disconnectedArduinoList = []

        self.autoArduinoList = {}

        self.updateTime = 0

    # voegt een arduino toe aan de lijst met arduino's en maakt handshake
    #TODO: (handshake misschien overbodig)
    def add_arduino(self, port):
        if port not in self.arduino_list.keys():
            try:
                self.arduino_list[port] = arduino.Arduino(port)
                self.connectedArduinoList[port] = self.arduino_list[port]
                print('added arduino on port: '+port)
                self.arduino_list[port].start()
            except OSError:
                print(sys.exc_info()[1])
                print('Could not add arduino on port: ' + port)
        else:
            print('Port '+port+' already in use')

    # parameter is een 'comport' string(vb: "COM10")
    # voegt een arduino toe aan de lijst met aangesloten arduino's en initialiseerd seriele connectie(nodig voor communicatie)
    def connectArduino(self, conn_arduino):
        self.connectedArduinoList[conn_arduino] = self.arduino_list[conn_arduino]
        self.connectedArduinoList[conn_arduino].ser_init()
        print('connected arduino')

    # parameter is een 'comport' string(vb: "COM10")
    # verbreekt de seriele connectie en verwijderd de arduino uit de lijst met actieve arduino's
    def disconnectArduino(self, port):
        self.arduino_list[port].ser_close()
        del self.connectedArduinoList[port]
        print('disconnected arduino')

    def goAuto(self, luik):
        print(luik.request('go_auto'))
        luik.ser_close()
        self.autoArduinoList[luik.port] = luik

    def stopAuto(self, luik):
        del self.autoArduinoList[luik.port]
        luik.ser_init()
        '''
        while 1:
            x = luik.ser.readline().decode('ascii').strip()
            if x == '':
                break
                '''

    # general update functie
    # TODO: is niet erg netjes en kan dus waarschijnlijk vervangen worden
    def update(self):
        # update the list of active arduino's
        self.updateArduinoList()
        # update arduino's and detect ones that are disconnected

        for a in self.connectedArduinoList.values():
            try:
                b=a
                #a.update()
                # a.request("info")
                #a.sendCommand("get_distance")
                #a.sendCommand("get_dist_thres")
                #a.sendCommand("get_temp")
                #a.sendCommand("get_temp_thres")
                #a.sendCommand("up")
                #a.sendCommand("get_distance")

            except arduino.serial.SerialException:
                print('The device on port ' +a.port+' can not be found or can not be configured.')
                print(sys.exc_info())

    # zoekt naar aangesloten arduino's aan de pc en update aan de hand daarvan de lijst met (actieve) arduino's
    def updateArduinoList(self):
        # fetch een lijst met aangesloten arduino's
        port_list = self.findarduino()

        disconnectedArduinoList = []
        # zijn er arduino's in de lijst met aangesloten arduino's die niet zijn aangesloten?
        for x in self.connectedArduinoList:
            if x not in port_list:
                disconnectedArduinoList.append(x)
            if x in self.autoArduinoList:
                disconnectedArduinoList.append(x)
        [self.disconnectArduino(x) for x in disconnectedArduinoList] # verbreek dan de verbinding

        # kopieer port_list(zodat je er over kan iteraten en aanpassingen kan maken)
        iterate_port_list = port_list.copy()
        for x in iterate_port_list:                     # x='comport'string(vb: "COM10")
            if x in self.connectedArduinoList:        # heeft x al een actieve verbinding
                port_list.remove(x)                         # dan is alles goed
            elif x in self.arduino_list:          # is deze anders al eerder aangesloten geweest?
                if x not in self.autoArduinoList:
                    self.connectArduino(x)            # maak dan een verbinding
                port_list.remove(x)                     # en dan is alles goed

        for x in port_list:                         # voor de over gebleven poorten(dit zijn nieuw aangesloten arduino's)
            self.add_arduino(x)               # voeg ze toe

    # geef een lijst met 'comport' strings(vb: "COM10") van aangesloten arduino's
    def findarduino(self):
        ports = list_ports_windows.comports()
        port_list = []
        for x in ports:
            #print(x.__str__()) #                   TODO: bewonder dit lijstje
            if 'Arduino' in x.__str__():                    # comport met arduino?
                port_list.append(x.__str__()[:5].strip())   # sla de eerste 5 tekens op("COM##" of "COM# ")
        return port_list
    def getConnectedArduinolist(self):
        self.updateArduinoList()
        return self.connectedArduinoList

    #comando's naar de arduino
    def schermOmhoog(self, port):
        if port in self.connectedArduinoList:
            self.connectedArduinoList[port].sendCommand("up")
    def schermOmlaag(self, port):
        if port in self.connectedArduinoList:
            self.connectedArduinoList[port].sendCommand("down")


'''
controller = Controller()
while True:
    try:                        #probeer dit
        controller.update()
    except:                     # foutje?
        print('oeps')           # zeg oeps
        print(sys.exc_info())   # stuur het foutje door naar de terminal zonder het programma stop te zetten
    time.sleep(0.25)
'''