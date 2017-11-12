import arduino
import controller
from GUI import *
from tkinter import *

class Main():
    def __init__(self):
        self.controller = controller.Controller()
        root = Tk()
        root.geometry('550x400+200+200')

        self.besturing = Besturing(root, self.controller, self.controller.getConnectedArduinolist())
        root.mainloop()

main = Main()



