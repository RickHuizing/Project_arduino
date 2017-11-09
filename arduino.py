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
        extra_info = None
        l = self.ser.readline().decode('ascii').strip()
        if l not in ["OK", "ERR"]:
            extra_info = l
            l = self.ser.readline().decode('ascii').strip()
            if l not in ["OK", "ERR"]:
                l = None
        return (l, extra_info)

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
            self.distance_history[key] = r[1]

    # haal de data van de photocell sensor op en sla het op met de huidige uur:minuut
    def update_light(self):
        key = time.strftime('%X')[:8]
        r = self.request("get_light")
        if r[0] == 'OK':
            self.light_history[key] = r[1]

    # haal de data van de thermometer op en sla het op met de huidige uur:minuut
    def update_temperature(self):
        key = time.strftime('%X')[:8]
        r = self.request("get_temp")
        if r[0] == 'OK':
            self.temperature_history[key] = r[1]

    def get_light_threshold(self):
        lightThres = self.request("get_light_thres")
        return lightThres
    def light_threshold_plus(self):
        self.request("light_thres_plus")
    def light_threshold_min(self):
        self.request("light_thres_min")

    def get_temp_threshold(self):
        tempThres = self.request("get_temp_thres")
        return tempThres
    def temperature_threshold_plus(self):
        self.request("temp_thres_plus")
    def temperature_threshold_min(self):
        self.request("temp_thres_min")

    def get_distance_threshold(self):
        dist_thres = self.request("get_dist_thres")
        return dist_thres

    def distance_threshold_plus(self):
        self.request("dist_thres_plus")

    def distance_threshold_min(self):
        self.request("dist_thres_min")




