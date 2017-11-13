import serial
import time
import sys

# >>> b'a string'.decode('ascii')
# 'a string'
# >>> 'a string'.encode('ascii')
# b'a string'

class Arduino:

    def __init__(self, port):
        #COM port (string)
        self.port = port
        # geeft aan of er een seriele connectie actief is
        self.serial_connection = False
        # initialiseer seriele connectie
        self.ser_init()

        self.type = 0

        #drempelwaarden voor het dalen/stoppen met dalen van het rolluik
        self.distance_threshold = 0.02  #in m
        self.light_threshold = 1        #in lux?? idk
        self.temperature_threshold = 22 #in graden C

        #huidige uitrolstatus in m
        self.distance = 0.02
        #maximale uitrollengte in m
        self.screen_length = 1.52
        #snelheid waarmee het scherm in- en uitrolt in m/s
        self.roll_speed = 0.0166 #=1m/minuut

        #dictionaries met voorgaande waarden vd sensoren
        self.distance_history = {}
        self.light_history = {}
        self.temperature_history = {}

        self.automodus = False


    # initieer seriele connectie, baud rate 19200
    def ser_init(self):
        self.ser = serial.Serial(self.port, 19200, timeout=1)
        self.serial_connection = True

    # sluit seriele connectie
    def ser_close(self):
        self.ser.close()
        self.serial_connection = False

    def set_type(self):
        self.type = int(self.request("get_type")[1])

    # Functie request
    #    argment: command -> commando voor Arduino
    #    return value: tuple met daarin statuscode (OK of ERR) en evt. aanvullende info
    def request(self, command):
        self.ser.write((command + "\n").encode('ascii'))  # Let op! pyserial heeft geen writeline, zelf \n aan string toevoegen!
        extra_info = "empty"
        l = self.ser.readline().decode('ascii').strip()
        if l not in ["OK", "ERR"]:
            extra_info = l
            l = self.ser.readline().decode('ascii').strip()
            if l not in ["OK", "ERR"]:
                l = "noreturn"
        return (l, extra_info)

    def readInput(self):
        input = ''
        while input.__len__()<2:
            input = self.ser.readline().decode('ascii').strip()
        return input

    def sendCommand(self, command):
        response = self.request(command)
        while response[0]!= 'OK':
            print(response)
            time.sleep(1)
            response = self.request(command)
        if(response[1]=="empty"):
            time.sleep(0.05)
            response = (response[0], self.ser.readline().decode('ascii').strip())
        print("command: "+command+" completed, result: "+response[0]+", "+response[1])
        #clean-up
        self.ser.readline()
        self.ser.readline()
        self.ser.readline()
        self.ser.readline()
        return response

    # probeer een handshake te maken(= checken of er verbinding is)
    def start(self):
        # Handshake
        tries_left = 3
        while (tries_left > 0):
            try:
                r = self.request("hello")
            except:
                print('port busy')
                r=0
            if r == ("OK", "IkBenEr!"):
                tries_left = 0
            else:
                tries_left -= 1
                if (tries_left == 0):
                    print("Handshake failed")

    def update(self):
        print(self.request("get_type"))
        if self.type != 0:
            if self.type == 1:
                self.update_light()
            elif self.type == 2:
                self.update_temperature()
            self.update_distance()
        else:
            self.set_type()

    # haal de data van de sonar sensor op en sla het op met de huidige uur:minuut
    def update_distance(self):
        key = time.strftime('%X')[:8]
        r = self.request("get_distance")
        if r[0] == 'OK':
            if len(self.distance_history)>9:
                tempHistcopy = self.distance_history.copy()
                i=len(self.distance_history)-9
                for x in tempHistcopy:
                    if i>0:
                        i-=1
                        self.distance_history={}
                    else:
                        self.distance_history[x] = tempHistcopy[x]
            self.distance_history[key] = float(r[1])

    # haal de data van de photocell sensor op en sla het op met de huidige uur:minuut
    def update_light(self):
        key = time.strftime('%X')[:8]
        r = self.request("get_light")
        if r[0] == 'OK':
            if len(self.light_history)>9:
                tempHistcopy = self.light_history.copy()
                i=len(self.light_history)-9
                for x in tempHistcopy:
                    if i>0:
                        i-=1
                        self.light_history={}
                    else:
                        self.light_history[x] = tempHistcopy[x]
                    self.light_history[key] = float(r[1])


    # haal de data van de thermometer op en sla het op met de huidige uur:minuut
    def update_temperature(self):
        key = time.strftime('%X')[:8]
        r = self.request("get_temp")
        print(r)
        if r[0] == 'OK':
            if len(self.temperature_history)>9:
                tempHistcopy = self.temperature_history.copy()
                i=len(self.temperature_history)-9
                for x in tempHistcopy:
                    if i>0:
                        i-=1
                        self.temperature_history={}
                    else:
                        self.temperature_history[x] = tempHistcopy[x]
            self.temperature_history[key] = float(r[1])


    def get_light_threshold(self):
        lightThres = self.request("get_light_thres")
        return lightThres[1][:-3]

    def set_light_thres(self, thres):
        oldThres=int(self.get_light_threshold())
        thres = int(thres)
        if oldThres>thres:
            times = oldThres-thres
            while times!=0:
                self.request("light_thres_min")
                times-=1
        elif oldThres<thres:
            times = thres-oldThres
            while times!=0:
                self.request("light_thres_plus")
                times -= 1
    def get_temp_threshold(self):
        tempThres = self.request("get_temp_thres")
        print(tempThres)
        return tempThres[1][:-2]
    def set_temp_thres(self, thres):
        oldThres=int(self.get_temp_threshold())
        thres = int(thres)
        if oldThres>thres:
            times = oldThres-thres
            while times!=0:
                self.request("temp_thres_min")
                times-=1
        elif oldThres<thres:
            times = thres-oldThres
            while times!=0:
                self.request("temp_thres_plus")
                times -=1


    def get_distance_threshold(self):
        dist_thres = self.request("get_dist_thres")
        return dist_thres[1][:-2]
    def set_distance_thres(self, thres):
        oldThres=int(self.get_distance_threshold())
        thres = int(thres)
        if oldThres>thres:
            times = oldThres-thres
            while times!=0:
                self.request("dist_thres_min")
                times-=1
        elif oldThres<thres:
            times = thres-oldThres
            while times!=0:
                self.request("dist_thres_plus")
                times -= 1







