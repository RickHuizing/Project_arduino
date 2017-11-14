from Project.Model import controller
from Project.View.GUI import *


class Main():
    def __init__(self):
        print("creating controller")
        self.controller = controller.Controller()
        self.controller.updateArduinoList()
        #self.base = Tk()
        #self.base.geometry('550x400+200+200')
        print("initialising view")
        self.root = MainView(self.controller)
        self.root.config(background='black')
        self.root.after(200, self.root.doUpdate())

        self.root.mainloop()

main = Main()



