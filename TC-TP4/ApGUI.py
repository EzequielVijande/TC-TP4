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
#Grafica activa
ATT=1
ATT_N=2
FASE=3
CEROS=4
RETARDO=5
IMPULSE=6
STEP=7


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
        self.ButtonsFrame = LabelFrame(self.root, text="Tipo de filtro", labelanchor="n",background="goldenrod")
        self.ButtonsFrame.pack(anchor=NW,fill=BOTH,expand=True)
        self.filter=tk.IntVar()
        self.rButton_low_pass = tk.Radiobutton(self.ButtonsFrame, text="Pasa bajos", 
            variable = self.filter, value = LP,background="light goldenrod",command=self.filter_call)
        self.rButton_low_pass.pack(fill=BOTH,expand=True)
        self.rButton_high_pass = tk.Radiobutton(self.ButtonsFrame, text="Pasa altos",command=self.filter_call,
            variable = self.filter, value = HP,background="light goldenrod")
        self.rButton_high_pass.pack(fill=BOTH,expand=True)
        self.rButton_band_pass = tk.Radiobutton(self.ButtonsFrame, text="Pasa banda", command=self.filter_call,
            variable = self.filter, value = BP,background="light goldenrod")
        self.rButton_band_pass.pack(fill=BOTH,expand=True)
        self.rButton_band_reject = tk.Radiobutton(self.ButtonsFrame, text="Rechaza banda", command=self.filter_call,
            variable = self.filter, value = BR,background="light goldenrod")
        self.rButton_band_reject.pack(fill=BOTH,expand=True)
        self.rButton_group_delay = tk.Radiobutton(self.ButtonsFrame, text="Retardo de grupo", command=self.filter_call,
            variable = self.filter, value = GR,background="light goldenrod")
        self.rButton_group_delay.pack(fill=BOTH,expand=True)
        self.rButton_low_pass.select() #Por default comienza seleccionado el filtro low_pass


    def placeAproximationButtons(self):
        self.AproxButtonsFrame = LabelFrame(self.root, text="Aproximacion", labelanchor="n",background="goldenrod")
        self.AproxButtonsFrame.pack(anchor=NW,fill=BOTH,expand=True)
        self.selected_aprox = StringVar(master=self.AproxButtonsFrame)
        self.selected_aprox.set(APROXIMACIONES[0]) # Empieza conButterworth como default

        self.pull_down_menu = OptionMenu(self.AproxButtonsFrame, self.selected_aprox, *APROXIMACIONES)
        self.pull_down_menu.config(bg="light goldenrod")
        self.pull_down_menu.pack(side=TOP,fill=BOTH,expand=True)
        self.GraphButton= Button(master=self.AproxButtonsFrame,text="Graph",command=self.graph_button_call
                                 ,background="light goldenrod").pack(side=BOTTOM,fill=BOTH,expand=True)

    def placeSpecifications(self):
        self.ApString= StringVar()
        self.AsString= StringVar()
        self.wpString= StringVar()
        self.wsString= StringVar()
        self.w0String= StringVar()
        self.qString= StringVar()
        self.ΔwpString= StringVar()
        self.ΔwsString= StringVar()

        self.SpecsFrame = LabelFrame(self.root, text="Especificaciones", labelanchor="n",background="goldenrod")
        self.SpecsFrame.pack(anchor=NW,fill=BOTH,expand=True)
        #Entrada de Ap
        Label(master=self.SpecsFrame,text="Ap(dB)",anchor=W,background="light goldenrod").pack(fill=BOTH,expand=True)
        self.entry_ap=Entry(master=self.SpecsFrame,textvariable=self.ApString)
        self.entry_ap.pack(anchor=NE,fill=BOTH,expand=True)
        #Entrada de As
        Label(master=self.SpecsFrame,text="As(dB)",anchor=W,background="light goldenrod").pack(fill=BOTH,expand=True)
        self.entry_as=Entry(master=self.SpecsFrame,textvariable=self.AsString)
        self.entry_as.pack(anchor=NE,fill=BOTH,expand=True)
        #Entrada de wp
        Label(master=self.SpecsFrame,text="wp(rad/seg)",anchor=W
              ,background="light goldenrod").pack(fill=BOTH,expand=True)
        self.entry_wp=Entry(master=self.SpecsFrame,textvariable=self.wpString)
        self.entry_wp.pack(anchor=NE,fill=BOTH,expand=True)
        #entrada de ws
        Label(master=self.SpecsFrame,text="ws(rad/seg)",anchor=W
              ,background="light goldenrod").pack(fill=BOTH,expand=True)
        self.entry_ws=Entry(master=self.SpecsFrame,textvariable=self.wsString)
        self.entry_ws.pack(anchor=NE,fill=BOTH,expand=True)
        #entrada de w0
        Label(master=self.SpecsFrame,text="wo(rad/seg)",anchor=W
              ,background="light goldenrod").pack(fill=BOTH,expand=True)
        self.entry_wo=Entry(master=self.SpecsFrame,textvariable=self.w0String,state='disabled')
        self.entry_wo.pack(anchor=NE,fill=BOTH,expand=True)
        #entrada de Q
        Label(master=self.SpecsFrame,text="Q",anchor=W,background="light goldenrod").pack(fill=BOTH,expand=True)
        self.entry_Q=Entry(master=self.SpecsFrame,textvariable=self.qString,state='disabled')
        self.entry_Q.pack(anchor=NE,fill=BOTH,expand=True)
        #entrada de Δwp
        Label(master=self.SpecsFrame,text="Δwp(rad/seg)",anchor=W
              ,background="light goldenrod").pack(fill=BOTH,expand=True)
        self.entry_Δwp=Entry(master=self.SpecsFrame,textvariable=self.ΔwpString,state='disabled')
        self.entry_Δwp.pack(anchor=NE,fill=BOTH,expand=True)
        #entrada de Δws
        Label(master=self.SpecsFrame,text="Δws(rad/seg)",anchor=W
              ,background="light goldenrod").pack(fill=BOTH,expand=True)
        self.entry_Δws=Entry(master=self.SpecsFrame,textvariable=self.ΔwsString,state='disabled')
        self.entry_Δws.pack(anchor=NE,fill=BOTH,expand=True)

    def PlaceGraphic(self):
        self.GraphicsFrame = LabelFrame(self.root, text="Graficas", labelanchor="n",background="goldenrod")
        self.GraphicsFrame.pack(anchor=NE,side=RIGHT,fill=BOTH,expand=True)
        self.Graph = Canvas(master=self.GraphicsFrame, width=GRAPH_WIDTH, height=GRAPH_HEIGHT)
        self.Graph.config(bg="snow2")
        self.Graph.pack(side=TOP,fill=BOTH,expand=True)
        #Botones para cambiar de graficas
        self.SelectedGraph= tk.IntVar()
        self.AttRButton= Radiobutton(master=self.GraphicsFrame,text="Atenuacion",background="pale turquoise",
                                     indicatoron=False,variable=self.SelectedGraph,value=ATT)
        self.AttRButton.pack(side=LEFT,fill=BOTH,expand=True)
        self.AttNRButton = Radiobutton(master=self.GraphicsFrame,text="Atenuacion Norm",background="pale turquoise",
                                     indicatoron=False,variable=self.SelectedGraph,value=ATT_N)
        self.AttNRButton.pack(side=LEFT,fill=BOTH,expand=True)
        self.FaseRButton = Radiobutton(master=self.GraphicsFrame,text="Fase",background="pale turquoise",
                                     indicatoron=False,variable=self.SelectedGraph,value=FASE)
        self.FaseRButton.pack(side=LEFT,fill=BOTH,expand=True)
        self.ZeroesRButton =Radiobutton(master=self.GraphicsFrame,text="Polos y ceros",background="pale turquoise",
                                     indicatoron=False,variable=self.SelectedGraph,value=CEROS)
        self.ZeroesRButton.pack(side=LEFT,fill=BOTH,expand=True)
        self.ImpulseRButton = Radiobutton(master=self.GraphicsFrame,text="Resp al impulso",background="pale turquoise",
                                     indicatoron=False,variable=self.SelectedGraph,value=IMPULSE)
        self.ImpulseRButton.pack(side=LEFT,fill=BOTH,expand=True)
        self.StepRButton = Radiobutton(master=self.GraphicsFrame,text="Resp al Escalon",background="pale turquoise",
                                     indicatoron=False,variable=self.SelectedGraph,value=STEP)
        self.StepRButton.pack(side=LEFT,fill=BOTH,expand=True)
        self.AttRButton.select() #por default empieza seleccionado el grafico de atenuacion

        #Boton que superpone plantilla
        self.PutTemplate= IntVar()
        self.TemplateButton = Checkbutton(master=self.GraphicsFrame, text="Superponer plantilla",
                        variable=self.PutTemplate,onvalue=1, offvalue=0,command=self.put_template_call,background="pale turquoise")
        self.TemplateButton.pack(side=LEFT,fill=BOTH,expand=True)
        self.SaveButton= Button(master=self.GraphicsFrame,text="Save",command=self.save_call
                                ,background="pale turquoise").pack(side=LEFT,fill=BOTH,expand=True)
        self.LoadButton= Button(master=self.GraphicsFrame,text="Load",command=self.load_call
                                ,background="pale turquoise").pack(side=LEFT,fill=BOTH,expand=True)
        self.NextButton= Button(master=self.GraphicsFrame,text="Next",command=self.next_call
                                ,background="pale turquoise").pack(side=LEFT,fill=BOTH,expand=True)


    def placeSliders(self):
        self.SliderFrame = LabelFrame(self.root, text="Rango de desnormalización(%)", labelanchor="n",background="goldenrod")
        self.SliderFrame.pack(side=LEFT,anchor=NW,fill=BOTH,expand=True)
        self.SlideNorm = Scale(master=self.SliderFrame, from_=0, to=100,orient=HORIZONTAL)
        self.SlideNorm.config(bg="light goldenrod")
        self.SlideNorm.pack(fill=BOTH,expand=True)


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
    def filter_call(self):
        fil=self.filter.get()
        if(fil==BP or fil==BR):
            self.entry_wp.config(state='disabled') #Desabilito entradas invalidas
            self.entry_ws.config(state='disabled')
            self.entry_Δwp.config(state='normal') #Habilito entradas validas
            self.entry_Δws.config(state='normal')
            self.entry_wo.config(state='normal')
            self.entry_Q.config(state='normal')
        elif(fil==LP or fil==HP):
            self.entry_wp.config(state='normal') #Habilito entradas validas
            self.entry_ws.config(state='normal')
            self.entry_Δwp.config(state='disabled') #Desabilito entradas invalidas
            self.entry_Δws.config(state='disabled')
            self.entry_wo.config(state='disabled')
            self.entry_Q.config(state='disabled')
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
    def DisplayError(self,result_str):
        messagebox.showinfo("Error en las especificaciones", result_str)