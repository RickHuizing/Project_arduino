import arduino
import sys
import time
from serial.tools import list_ports_windows
import sched


class Controller:
    def __init__(self):
        self.views = 0
        self.arduino_list = {}
        self.connectedArduinoList = {}
        self.disconnectedArduinoList = []

        self.updateTime = 0

    def add_arduino(self, port):
        if port not in self.arduino_list.keys():
            try:
                self.arduino_list[port] = arduino.Arduino(port)
                self.connectedArduinoList[port] = self.arduino_list[port]
                print('added arduino on port: '+port)
                self.arduino_list[port].start()
            except OSError:
                print (type(port))
                print(sys.exc_info()[1])
                print('Could not add arduino on port: ' + port)
        else:
            print('Port '+port+' already in use')

    def connectArduino(self, conn_arduino):
        self.connectedArduinoList[conn_arduino] = self.arduino_list[conn_arduino]
        self.connectedArduinoList[conn_arduino].ser_init()
        print('connected arduino')

    def disconnectArduino(self, port):
        self.arduino_list[port].ser_close()
        del self.connectedArduinoList[port]
        print('disconnected arduino')

    def update(self):
        # update the list of active arduino's
        controller.updateArduinoList()
        # update arduino's and detect ones that are disconnected
        for a in controller.connectedArduinoList.values():
            try:
                a.request("info")
            except arduino.serial.SerialException:
                print('The device on port ' +a.port+' can not be found or can not be configured.')
                print(sys.exc_info())


    # add arduino's to the active arduino list by COM port
    def updateArduinoList(self):
        port_list = controller.findarduino()
        #find and disconnect disconnected arduino's
        disconnectedArduinoList = []
        for x in controller.connectedArduinoList:
            if x not in port_list:
                disconnectedArduinoList.append(x)
        [controller.disconnectArduino(x) for x in disconnectedArduinoList]

        # find and add newly connected arduino's
        iterate_port_list = port_list.copy()
        for x in iterate_port_list:
            if x in controller.connectedArduinoList:
                port_list.remove(x)
            elif x in controller.arduino_list:
                controller.connectArduino(x)
                port_list.remove(x)

        for x in port_list:
            controller.add_arduino(x)

    # find arduino's by going through all active usb ports
    def findarduino(self):
        ports = list_ports_windows.comports()
        port_list = []
        for x in ports:
            if 'Arduino' in x.__str__():
                port_list.append(x.__str__()[:5].strip())
        return port_list


controller = Controller()
s = sched.scheduler(time.time, time.sleep)
#s.enterabs()
while True:
    try:
        controller.update()
    except:
        print('oeps')
        print(sys.exc_info())
    arduino.time.sleep(1)

