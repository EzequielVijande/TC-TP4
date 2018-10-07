import tkinter as tk
from tkinter import ttk
from tkinter import *
from tkinter import messagebox

#Filtros
LP=1
HP=2
BP=3
BR=4
GR=5
#Aproximaciones
APROXIMACIONES=[
"Butterworth",
"Chebycheff",
"Chebycheff inverso",
"Bessel",
"Gauss",
"Cauer",
"Legendre"
]
#Largos y Anchos
GRAPH_WIDTH=800
GRAPH_HEIGHT=600
#Eventos
NO_EV=0
GRAPH_EV=1
QUIT_EV=2
SAVE_EV=3
LOAD_EV=4
NEXT_EV=5
CHANGE_GRAPH_EV=6
PUT_TEMPLATE_EV=7


class ApGUI(object):
    """Clase que se encarga de crear,posicionar y actualizar botones y graficas"""
    def __init__(self):
        self.Ev=NO_EV
        self.root = Tk()
        self.root.geometry('1620x780')
        self.root.resizable(width=True, height=True)
        self.root.title("Aproximador de filtros")
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.PlaceGraphic()
        self.placeFilterButtons()
        self.placeAproximationButtons()
        self.placeSpecifications()
        self.placeSliders()


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
        self.selected_aprox = StringVar(master=self.AproxButtonsFrame)
        self.selected_aprox.set(APROXIMACIONES[0]) # Empieza conButterworth como default

        self.pull_down_menu = OptionMenu(self.AproxButtonsFrame, self.selected_aprox, *APROXIMACIONES)
        self.pull_down_menu.pack(side=TOP)
        self.GraphButton= Button(master=self.AproxButtonsFrame,text="Graph",command=self.graph_button_call).pack(side=BOTTOM)

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
        self.GraphicsFrame = LabelFrame(self.root, text="Graficas", labelanchor="n")
        self.GraphicsFrame.pack(anchor=NE,side=RIGHT,fill=BOTH,expand=True)
        self.Graph = Canvas(master=self.GraphicsFrame, width=GRAPH_WIDTH, height=GRAPH_HEIGHT)
        self.Graph.pack(side=TOP,fill=BOTH,expand=True)
        #Botones para cambiar de graficas
        self.AttButton = Button(master=self.GraphicsFrame,text="Atenuacion")
        self.AttButton.pack(side=LEFT,fill=BOTH,expand=True)
        self.AttNButton = Button(master=self.GraphicsFrame,text="Atenuacion Norm")
        self.AttNButton.pack(side=LEFT,fill=BOTH,expand=True)
        self.FaseButton = Button(master=self.GraphicsFrame,text="Fase")
        self.FaseButton.pack(side=LEFT,fill=BOTH,expand=True)
        self.ZeroesButton = Button(master=self.GraphicsFrame,text="Polos y ceros")
        self.ZeroesButton.pack(side=LEFT,fill=BOTH,expand=True)
        self.ImpulseButton = Button(master=self.GraphicsFrame,text="Resp al impulso")
        self.ImpulseButton.pack(side=LEFT,fill=BOTH,expand=True)
        self.StepButton = Button(master=self.GraphicsFrame,text="Resp al Escalon")
        self.StepButton.pack(side=LEFT,fill=BOTH,expand=True)
        #Boton que superpone plantilla
        self.PutTemplate= IntVar()
        self.TemplateButton = Checkbutton(master=self.GraphicsFrame, text="Superponer plantilla",
                        variable=self.PutTemplate,onvalue=1, offvalue=0,command=self.put_template_call)
        self.TemplateButton.pack(side=LEFT,fill=BOTH,expand=True)
        self.SaveButton= Button(master=self.GraphicsFrame,text="Save",command=self.save_call).pack(side=LEFT,fill=BOTH,expand=True)
        self.LoadButton= Button(master=self.GraphicsFrame,text="Load",command=self.load_call).pack(side=LEFT,fill=BOTH,expand=True)
        self.NextButton= Button(master=self.GraphicsFrame,text="Next",command=self.next_call).pack(side=LEFT,fill=BOTH,expand=True)


    def placeSliders(self):
        self.SliderFrame = LabelFrame(self.root, text="Rango de desnormalización(%)", labelanchor="n")
        self.SliderFrame.pack(side=LEFT,anchor=NW)
        self.SlideNorm = Scale(master=self.SliderFrame, from_=0, to=100,orient=HORIZONTAL)
        self.SlideNorm.pack()


    #Getters
    def GetEvent(self):
        return self.Ev

    def GetFilter(self):
        return self.filter

    def GetAprox(self):
        return self.selected_aprox

    #Callbacks
    def on_closing(self):
        if messagebox.askokcancel("Cerrar", "Desea cerrar el programa?"):
            self.Ev=QUIT_EV

    def graph_button_call(self):
        self.Ev=GRAPH_EV

    def change_graph_button_call(self):
        self.Ev=CHANGE_GRAPH_EV

    def save_call(self):
        self.Ev=SAVE_EV

    def load_call(self):
        self.Ev=LOAD_EV

    def next_call(self):
        self.Ev=NEXT_EV

    def put_template_call(self):
        self.Ev=PUT_TEMPLATE_EV


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

    #Extras
    def CloseGUI(self):
        self.root.destroy()
    def Update(self):
        self.root.update()
    def EventSolved(self):
        self.Ev = NO_EV