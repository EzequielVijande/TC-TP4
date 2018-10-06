import tkinter as tk
from tkinter import ttk
from tkinter import *

#Filtros
LP=1
HP=2
BP=3
BR=4
GR=5
#Aproximaciones
BUTTER=1
CHEBY=2
INV_CHEBY=3
BESSEL=4
GAUSS=5
CAUER=6
LEGENDRE=7

class ApGUI(object):
    """Clase que se encarga de crear,posicionar y actualizar botones y graficas"""
    def __init__(self, *args, **kwargs):
        self.root = Tk()
        self.root.geometry('1920x1080')
        self.root.resizable(width=True, height=True)
        self.root.title("Aproximador de filtros")
        self.placeFilterButtons()
        self.placeAproximationButtons()
        self.placeSpecifications()
        #self.PlaceGraphic()
        self.placeMiscButtons()
        self.placeSliders()

        self.root.mainloop()

    #Funciones de inicializacion
    def placeFilterButtons(self):
        self.ButtonsFrame = LabelFrame(self.root, text="Tipo de filtro", labelanchor="n")
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
        self.AproxButtonsFrame = LabelFrame(self.root, text="Aproximacion", labelanchor="n")
        self.AproxButtonsFrame.pack(anchor=NW)
        self.Aprox=tk.IntVar()
        self.rButton_butter = tk.Radiobutton(self.AproxButtonsFrame, text="Butterworth", 
            variable = self.Aprox, value = BUTTER).pack()
        self.rButton_cheby = tk.Radiobutton(self.AproxButtonsFrame, text="Chebycheff", 
            variable = self.Aprox, value = CHEBY).pack()
        self.rButton_cheby_inv = tk.Radiobutton(self.AproxButtonsFrame, text="Chebycheff inverso", 
            variable = self.Aprox, value = INV_CHEBY).pack()
        self.rButton_bessel = tk.Radiobutton(self.AproxButtonsFrame, text="Bessel", 
            variable = self.Aprox, value = BESSEL).pack()
        self.rButton_gauss = tk.Radiobutton(self.AproxButtonsFrame, text="Gauss", 
            variable = self.Aprox, value = GAUSS).pack()
        self.rButton_cauer = tk.Radiobutton(self.AproxButtonsFrame, text="Cauer", 
            variable = self.Aprox, value = CAUER).pack()
        self.rButton_legendre = tk.Radiobutton(self.AproxButtonsFrame, text="Legendre", 
            variable = self.Aprox, value = LEGENDRE).pack()

    def placeSpecifications(self):
        self.ApString= StringVar()
        self.AsString= StringVar()
        self.wpString= StringVar()
        self.wsString= StringVar()
        self.w0String= StringVar()
        self.qString= StringVar()

        self.SpecsFrame = LabelFrame(self.root, text="Especificaciones", labelanchor="n")
        self.SpecsFrame.pack(anchor=NW)
        #Entrada de Ap
        Label(master=self.SpecsFrame,text="Ap(dB)=",anchor=W).pack(anchor=NW)
        entry_ap=Entry(master=self.SpecsFrame,textvariable=self.ApString).pack(anchor=NE)
        #Entrada de As
        Label(master=self.SpecsFrame,text="As(dB)=",anchor=W).pack(anchor=NW)
        entry_ap=Entry(master=self.SpecsFrame,textvariable=self.AsString).pack(anchor=NE)
        #Entrada de wp
        Label(master=self.SpecsFrame,text="wp(rad/seg)=",anchor=W).pack(anchor=NW)
        entry_ap=Entry(master=self.SpecsFrame,textvariable=self.wpString).pack(anchor=NE)
        #entrada de ws
        Label(master=self.SpecsFrame,text="ws(rad/seg)=",anchor=W).pack(anchor=NW)
        entry_ap=Entry(master=self.SpecsFrame,textvariable=self.wsString).pack(anchor=NE)
        #entrada de w0
        Label(master=self.SpecsFrame,text="wo(rad/seg)=",anchor=W).pack(anchor=NW)
        entry_ap=Entry(master=self.SpecsFrame,textvariable=self.w0String).pack(anchor=NE)
        #entrada de Q
        Label(master=self.SpecsFrame,text="Q=",anchor=W).pack(anchor=NW)
        entry_ap=Entry(master=self.SpecsFrame,textvariable=self.qString).pack(anchor=NE)

    def PlaceGraphic(self):
        return
    def placeMiscButtons(self):
        self.MiscFrame = Frame(self.root)
        self.MiscFrame.pack(anchor=S)
        #Boton de save
        self.SaveButton= Button(master=self.MiscFrame,text="Save").pack(side=LEFT)
        self.NextButton= Button(master=self.MiscFrame,text="Next").pack(side=RIGHT)

    def placeSliders(self):
        self.SliderFrame = LabelFrame(self.root, text="Rango de desnormalización(%)", labelanchor="n")
        self.SliderFrame.pack(anchor=SW)
        self.SlideNorm = Scale(master=self.SliderFrame, from_=0, to=100,orient=HORIZONTAL)
        self.SlideNorm.pack()


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