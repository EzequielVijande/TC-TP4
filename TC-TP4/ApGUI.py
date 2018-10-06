import tkinter as tk
from tkinter import ttk
from tkinter import *

#Filtros
LP=1
HP=2
BP=3
BR=4
GR=5

class ApGUI(object):
    """Clase que se encarga de crear,posicionar y actualizar botones y graficas"""
    def __init__(self, *args, **kwargs):
        self.root = Tk()
        self.root.geometry('600x500')
        self.root.resizable(width=True, height=True)
        self.root.title("Aproximador de filtros")
        self.placeFilterButtons()
        #self.placeAproximationButtons()
        #self.placeSpecifications()
        #self.PlaceGraphic()
        #self.placeMiscButtons()
        #self.placeSliders()

        self.root.mainloop()

    #Funciones de inicializacion
    def placeFilterButtons(self):
        self.ButtonsFrame = LabelFrame(self.root, text="Tipos de filtro", labelanchor="n")
        self.ButtonsFrame.pack(anchor=NW)
        self.filter=tk.IntVar()
        self.rButton_low_pass = tk.Radiobutton(self.ButtonsFrame, text="Pasa bajos", 
            variable = self.filter, value = LP).pack()
        self.rButton_high_pass = tk.Radiobutton(self.ButtonsFrame, text="Pasa altos", 
            variable = self.filter, value = HP).pack()
        self.rButton_band_pass = tk.Radiobutton(self.ButtonsFrame, text="Pasa banda", 
            variable = self.filter, value = BP).pack()
        self.rButton_band_reject = tk.Radiobutton(self.ButtonsFrame, text="Rechaza banda", 
            variable = self.filter, value = BR).pack()
        self.rButton_group_delay = tk.Radiobutton(self.ButtonsFrame, text="Retardo de grupo", 
            variable = self.filter, value = GR).pack()




    def placeAproximationButtons(self):
        return
    def placeSpecifications(self):
        return
    def PlaceGraphic(self):
        return
    def placeMiscButtons(self):
        return
    def placeSliders(self):
        return

    #Funciones relacionadas a graficas
    def plotPhase(self, w,fase):
        return
    def plotAtteNorm(self, w,attN):
        return
    def plotAtte(self, w,att):
        return
    def placeTemplate(self,wp,ws,Ap,As,wo,Q):
        return
    def plotZeros(self,sigma,w):
        return
    def plotImpulse(t,y):
        return
    def plotStep(t,y):
        return