import arduino
import controller
from GUI import *
from tkinter import *

class Main():
    def __init__(self):
        self.controller = controller.Controller()
        self.controller.updateArduinoList()
        #self.base = Tk()
        #self.base.geometry('550x400+200+200')
        print("hai")
        self.root = MainView( self.controller)
        #self.root.grid(row=0, column=0)

        print("hhoi")
        self.root.mainloop()

main = Main()



