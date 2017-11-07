import serial
import time
import sys
import sched

# >>> b'a string'.decode('ascii')
# 'a string'
# >>> 'a string'.encode('ascii')
# b'a string'

class Arduino:

    def __init__(self, port):
        #except:
        #    print('seriele connectie met arduino niet gelukt')
        #    print(sys.exc_info())

        self.port = port
        self.serial_connection = False
        self.ser_init()


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


    def ser_init(self):
        # initieer seriele connectie
        self.ser = serial.Serial(self.port, 19200, timeout=1)
        self.serial_connection = True

    def ser_close(self):
        self.ser.close()
        self.serial_connection = False

    # Functie request
    #    argment: command -> commando voor Arduino
    #    return value: tuple met daarin statuscode (OK of ERR) en evt. aanvullende info
    '''
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
    '''
    def request(self, command):
        self.ser.write((command + "\n").encode('ascii'))  # Let op! pyserial heeft geen writeline, zelf \n aan string toevoegen!
        #print((command + "\n").encode('ascii'))
        extra_info = None
        l = self.ser.readline().decode('ascii').strip()
        if l not in ["OK", "ERR"]:
            extra_info = l
            l = self.ser.readline().decode('ascii').strip()
            if l not in ["OK", "ERR"]:
                l = None
        return (l, extra_info)

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

        # Informatie opvragen
        '''
        r = self.request("info")
        if (r[0] == "OK"):
            print("Informatie embedded software: " + r[1]);
        else:
            print("Fout opgetreden bij opvragen informatie embedded software");
        '''

    def update_distance(self):
        key = time.strftime('%X')[:8]
        r = self.request("get_distance")
        if r[0] == 'OK':
            self.distance_history[key] = r[1] + 'cm'

    def update_light(self):
        print('hai')
        key = time.strftime('%X')[:8]
        r = self.request("get_light")
        if r[0] == 'OK':
            self.light_history[key] = r[1]

    def update_temperature(self):
        key = time.strftime('%X')[:8]
        r = self.request("get_temp")
        if r[0] == 'OK':
            self.temperature_history[key] = r[1]




