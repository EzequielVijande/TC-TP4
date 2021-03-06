import matplotlib
import matplotlib.patches as patches
matplotlib.use('TkAgg')
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.backend_bases import key_press_handler
from matplotlib.figure import Figure
from pathlib import Path
from UserData import UserData
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
#Eventos de la primera etapa
NO_EV=0
GRAPH_EV=1
QUIT_EV=2
SAVE_EV=3
LOAD_EV=4
NEXT_EV=5
CHANGE_GRAPH_EV=6
PUT_TEMPLATE_EV=7
#Eventos de la segunda eetapa
PREV_EV=8
CREATE_STAGE_EV=9
DELETE_STAGE_EV=10
SELECT_STAGE_EV=11
CHANGED_V_LIMITS_EV=12
CHANGED_STAGE_PARAMS=13
RESET=14
EXPORT=15
TRANSFER_FUNCTION_CHECK_EV=16
#Grafica activa
ATT=1
ATT_N=2
FASE=3
CEROS=4
RETARDO=5
IMPULSE=6
STEP=7
Q_GRAPH=8
#Check_BUTTONS
NORMAL_CHECK=1
N_CHECK=2
N_RANGE_CHECK=3
#Colores principales
FRAME_COLOR= "goldenrod"
FRAME_TEXT_COLOR="black"
BUTTON_COLOR= "light goldenrod"
BUTTON_FONT_COLOR="black"
GRAPH_BUTTON_COLOR="Cyan1"
GRAPH_BUTTON_TEXT_COLOR="black"
#Colores de las graficas
AXIS_COLOR= "black"
GRID_COLOR= "blue"
AXES_BACKGROUND="white"
LABEL_COLOR="blue"





class ApGUI(object):
    """Clase que se encarga de crear,posicionar y actualizar botones y graficas"""
    def __init__(self):
        self.Graph_enable=False
        self.q_is_in_plot=False
        self.TemplateOn=False
        self.q_container=[]
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
        self.ButtonsFrame = LabelFrame(self.root, text="Tipo de filtro", labelanchor="n",background=FRAME_COLOR,fg=FRAME_TEXT_COLOR)
        self.ButtonsFrame.pack(anchor=NW,fill=BOTH,expand=True)
        self.filter=tk.IntVar()
        self.rButton_low_pass = tk.Radiobutton(self.ButtonsFrame, text="Pasa bajos", 
            variable = self.filter, value = LP,background=BUTTON_COLOR,fg=BUTTON_FONT_COLOR,command=self.filter_call)
        self.rButton_low_pass.pack(fill=BOTH,expand=True)
        self.rButton_high_pass = tk.Radiobutton(self.ButtonsFrame, text="Pasa altos",command=self.filter_call,
            variable = self.filter, value = HP,background=BUTTON_COLOR,fg=BUTTON_FONT_COLOR)
        self.rButton_high_pass.pack(fill=BOTH,expand=True)
        self.rButton_band_pass = tk.Radiobutton(self.ButtonsFrame, text="Pasa banda", command=self.filter_call,
            variable = self.filter, value = BP,background=BUTTON_COLOR,fg=BUTTON_FONT_COLOR)
        self.rButton_band_pass.pack(fill=BOTH,expand=True)
        self.rButton_band_reject = tk.Radiobutton(self.ButtonsFrame, text="Rechaza banda", command=self.filter_call,
            variable = self.filter, value = BR,background=BUTTON_COLOR,fg=BUTTON_FONT_COLOR)
        self.rButton_band_reject.pack(fill=BOTH,expand=True)
        self.rButton_group_delay = tk.Radiobutton(self.ButtonsFrame, text="Retardo de grupo", command=self.filter_call,
            variable = self.filter, value = GR,background=BUTTON_COLOR,fg=BUTTON_FONT_COLOR)
        self.rButton_group_delay.pack(fill=BOTH,expand=True)
        self.rButton_low_pass.select() #Por default comienza seleccionado el filtro low_pass


    def placeAproximationButtons(self):
        self.AproxButtonsFrame = LabelFrame(self.root, text="Aproximacion", labelanchor="n",background=FRAME_COLOR,fg=FRAME_TEXT_COLOR)
        self.AproxButtonsFrame.pack(anchor=NW,fill=BOTH,expand=True)
        self.selected_aprox = StringVar(master=self.AproxButtonsFrame)
        self.selected_aprox.set(APROXIMACIONES[0]) # Empieza con Butterworth como default

        self.pull_down_menu = OptionMenu(self.AproxButtonsFrame, self.selected_aprox, *APROXIMACIONES)
        self.pull_down_menu.config(bg=BUTTON_COLOR)
        self.pull_down_menu.pack(side=TOP,fill=BOTH,expand=True)
        self.GraphButton= Button(master=self.AproxButtonsFrame,text="Graph",command=self.graph_button_call
                                 ,background=BUTTON_COLOR,fg=BUTTON_FONT_COLOR).pack(side=BOTTOM,fill=BOTH,expand=True)

    def placeSpecifications(self):
        self.PrevState= LP
        self.ApString= StringVar()
        self.AsString= StringVar()
        self.wpString= StringVar()
        self.wsString= StringVar()
        self.w0String= StringVar()
        self.qString= StringVar()
        self.nString= StringVar()
        self.nMinString= StringVar()
        self.nMaxString= StringVar()
        self.ΔwpString= StringVar()
        self.ΔwsString= StringVar()
        self.τ0String= StringVar()
        self.wrgString= StringVar()
        self.YString= StringVar()
        #Variables de los checkbuttons
        self.SelectedCheck = IntVar()


        self.SpecsFrame = LabelFrame(self.root, text="Especificaciones", labelanchor="n",background=FRAME_COLOR,fg=FRAME_TEXT_COLOR)
        self.SpecsFrame.pack(anchor=NW,fill=BOTH,expand=True)
        #Entrada de Ap
        self.ApLabel= Label(master=self.SpecsFrame,text="Ap(dB)",anchor=W,background=BUTTON_COLOR,fg=BUTTON_FONT_COLOR)
        self.ApLabel.pack(fill=BOTH,expand=True)
        self.entry_ap=Entry(master=self.SpecsFrame,textvariable=self.ApString)
        self.entry_ap.pack(anchor=NE,fill=BOTH,expand=True)
        #Entrada de As
        self.AsLabel= Label(master=self.SpecsFrame,text="As(dB)",anchor=W,background=BUTTON_COLOR,fg=BUTTON_FONT_COLOR)
        self.AsLabel.pack(fill=BOTH,expand=True)
        self.entry_as=Entry(master=self.SpecsFrame,textvariable=self.AsString)
        self.entry_as.pack(anchor=NE,fill=BOTH,expand=True)
        #Entrada de wp
        self.wpLabel= Label(master=self.SpecsFrame,text="fp(Hz)",anchor=W,background=BUTTON_COLOR,fg=BUTTON_FONT_COLOR)
        self.wpLabel.pack(fill=BOTH,expand=True)
        self.entry_wp=Entry(master=self.SpecsFrame,textvariable=self.wpString)
        self.entry_wp.pack(anchor=NE,fill=BOTH,expand=True)
        #entrada de ws
        self.wsLabel= Label(master=self.SpecsFrame,text="fs(Hz)",anchor=W,background=BUTTON_COLOR,fg=BUTTON_FONT_COLOR)
        self.wsLabel.pack(fill=BOTH,expand=True)
        self.entry_ws=Entry(master=self.SpecsFrame,textvariable=self.wsString)
        self.entry_ws.pack(anchor=NE,fill=BOTH,expand=True)
        #entrada de w0
        self.w0Label= Label(master=self.SpecsFrame,text="fo(Hz)",anchor=W,background=BUTTON_COLOR,fg=BUTTON_FONT_COLOR)
        self.entry_wo=Entry(master=self.SpecsFrame,textvariable=self.w0String,state='disabled')
        #entrada de Δwp
        self.ΔwpLabel= Label(master=self.SpecsFrame,text="Δfp(Hz)",anchor=W,background=BUTTON_COLOR,fg=BUTTON_FONT_COLOR)
        self.entry_Δwp=Entry(master=self.SpecsFrame,textvariable=self.ΔwpString,state='disabled')
        #entrada de Δws
        self.ΔwsLabel= Label(master=self.SpecsFrame,text="Δfs(Hz)",anchor=W,background=BUTTON_COLOR,fg=BUTTON_FONT_COLOR)
        self.entry_Δws=Entry(master=self.SpecsFrame,textvariable=self.ΔwsString,state='disabled')
        #entrada de τ(0)
        self.τ0Label= Label(master=self.SpecsFrame,text="τ(0) (seg)",anchor=W,background=BUTTON_COLOR,fg=BUTTON_FONT_COLOR)
        self.entry_τ0=Entry(master=self.SpecsFrame,textvariable=self.τ0String,state='disabled')
        #Entrada de wrg
        self.wrgLabel=Label(master=self.SpecsFrame,text="frg (Hz)",anchor=W,background=BUTTON_COLOR,fg=BUTTON_FONT_COLOR)
        self.entry_wrg=Entry(master=self.SpecsFrame,textvariable=self.wrgString,state='disabled')
        #Entrada de Y
        self.YLabel=Label(master=self.SpecsFrame,text="Y",anchor=W,background=BUTTON_COLOR,fg=BUTTON_FONT_COLOR)
        self.entry_Y=Entry(master=self.SpecsFrame,textvariable=self.YString,state='disabled')
        #Alternativas de calculo
        self.ChecksFrame= Frame(master=self.SpecsFrame,background=FRAME_COLOR)
        self.ChecksFrame.pack(side="top",fill=BOTH,expand=True)
        #Normal
        self.NormalFrame= Frame(master=self.ChecksFrame,background=FRAME_COLOR)
        self.NormalFrame.pack(side="top",fill=BOTH,expand=True)
        self.NormalCheck= Radiobutton(master=self.NormalFrame,text="Normal",background=BUTTON_COLOR,fg=BUTTON_FONT_COLOR,
                                     indicatoron=False,variable=self.SelectedCheck,value=NORMAL_CHECK,command=self.check_button_call)
        self.NormalCheck.pack(side="left",fill=BOTH,expand=True)
        #N fijo
        self.NFrame= Frame(master=self.ChecksFrame,background=FRAME_COLOR)
        self.NFrame.pack(side="top",fill=BOTH,expand=True)
        self.NCheck= Radiobutton(master=self.NFrame,text="Habilitar",background=BUTTON_COLOR,fg=BUTTON_FONT_COLOR,
                                     indicatoron=False,variable=self.SelectedCheck,value=N_CHECK,command=self.check_button_call)
        self.NCheck.pack(side="left",fill=BOTH,expand=True)
        self.NLabel= Label(master=self.NFrame,text="N",anchor=W,background=BUTTON_COLOR,fg=BUTTON_FONT_COLOR)
        self.NLabel.pack(side="left",fill=BOTH,expand=True)
        self.entry_N=Entry(master=self.NFrame,textvariable=self.nString,state='disabled')
        self.entry_N.pack(side="left",fill=BOTH,expand=True)
        #Rango de n
        self.N_rangeFrame= Frame(master=self.ChecksFrame,background=FRAME_COLOR)
        self.N_rangeFrame.pack(side="top",fill=BOTH,expand=True)
        self.N_rangeCheck= Radiobutton(master=self.NFrame,text="Habilitar",background=BUTTON_COLOR,fg=BUTTON_FONT_COLOR,
                                     indicatoron=False,variable=self.SelectedCheck,value=N_RANGE_CHECK,command=self.check_button_call)
        self.N_rangeCheck.pack(side="left",fill=BOTH,expand=True)
        #Hago otro frame para las entries de n
        self.N_entriesFrame= Frame(master=self.N_rangeFrame,background=BUTTON_COLOR)
        self.N_entriesFrame.pack(side="left",fill=BOTH,expand=True)

        N_maxFrame =Frame(master=self.N_entriesFrame,background=BUTTON_COLOR)
        N_maxFrame.pack(side="top",fill=BOTH,expand=True)
        self.N_maxLabel= Label(master=N_maxFrame,text="N max",anchor=W,background=BUTTON_COLOR,fg=BUTTON_FONT_COLOR)
        self.N_maxLabel.pack(side="left",fill=BOTH,expand=True)
        self.entry_N_max=Entry(master=N_maxFrame,textvariable=self.nMaxString,state='disabled')
        self.entry_N_max.pack(side="right",fill=BOTH,expand=True)

        N_minFrame =Frame(master=self.N_entriesFrame,background=BUTTON_COLOR)
        N_minFrame.pack(side="top",fill=BOTH,expand=True)
        self.N_minLabel= Label(master=N_minFrame,text="N min",anchor=W,background=BUTTON_COLOR,fg=BUTTON_FONT_COLOR)
        self.N_minLabel.pack(side="left",fill=BOTH,expand=True)
        self.entry_N_min=Entry(master=N_minFrame,textvariable=self.nMinString,state='disabled')
        self.entry_N_min.pack(side="right",fill=BOTH,expand=True)


    

    def PlaceGraphic(self):
        self.NString_Graph= StringVar()
        self.NString_Graph.set("N =")
        self.GraphicsFrame = LabelFrame(self.root, text="Graficas", labelanchor="n",background=FRAME_COLOR,fg=FRAME_TEXT_COLOR)
        self.GraphicsFrame.pack(anchor=NE,side=RIGHT,fill=BOTH,expand=True)
        self.fig=Figure(figsize=(1,1), dpi=200,facecolor="lavender",constrained_layout=True)
        self.Graph = FigureCanvasTkAgg(self.fig,master=self.GraphicsFrame)
        self.Graph.get_tk_widget().config( width=GRAPH_WIDTH, height=GRAPH_HEIGHT)
        self.Graph.get_tk_widget().pack(side=TOP,fill=BOTH,expand=True)
        self.N_Label= Label(master=self.GraphicsFrame,textvariable=self.NString_Graph,bg=BUTTON_COLOR)
        self.N_Label.pack(side=TOP,fill=BOTH,expand=True)

        #Setteo de los axes
        self.InitializeAxes()

        #Creo una toolbar para los graficos
        toolbarFrame = Frame(master=self.GraphicsFrame)
        toolbarFrame.pack(side=TOP,fill=BOTH,expand=True)
        toolbar = NavigationToolbar2Tk(self.Graph, toolbarFrame)
        toolbar.pack(fill=BOTH,expand=True)
        #Botones para cambiar de graficas
        self.SelectedGraph= tk.IntVar()
        self.AttRButton= Radiobutton(master=self.GraphicsFrame,text="Atenuacion",background=GRAPH_BUTTON_COLOR,fg=GRAPH_BUTTON_TEXT_COLOR,
                                     indicatoron=False,variable=self.SelectedGraph,value=ATT,command=self.change_graph_button_call)
        self.AttRButton.pack(side=LEFT,fill=BOTH,expand=True)
        self.AttNRButton = Radiobutton(master=self.GraphicsFrame,text="Atenuacion Norm",background=GRAPH_BUTTON_COLOR,fg=GRAPH_BUTTON_TEXT_COLOR,
                                     indicatoron=False,variable=self.SelectedGraph,value=ATT_N,command=self.change_graph_button_call)
        self.AttNRButton.pack(side=LEFT,fill=BOTH,expand=True)
        self.FaseRButton = Radiobutton(master=self.GraphicsFrame,text="Fase",background=GRAPH_BUTTON_COLOR,fg=GRAPH_BUTTON_TEXT_COLOR,
                                     indicatoron=False,variable=self.SelectedGraph,value=FASE,command=self.change_graph_button_call)
        self.FaseRButton.pack(side=LEFT,fill=BOTH,expand=True)
        self.ZeroesRButton =Radiobutton(master=self.GraphicsFrame,text="Polos y ceros",background=GRAPH_BUTTON_COLOR,fg=GRAPH_BUTTON_TEXT_COLOR,
                                     indicatoron=False,variable=self.SelectedGraph,value=CEROS,command=self.change_graph_button_call)
        self.ZeroesRButton.pack(side=LEFT,fill=BOTH,expand=True)
        self.QGraphButton =Radiobutton(master=self.GraphicsFrame,text="Q",background=GRAPH_BUTTON_COLOR,fg=GRAPH_BUTTON_TEXT_COLOR,
                                     indicatoron=False,variable=self.SelectedGraph,value=Q_GRAPH,command=self.change_graph_button_call)
        self.QGraphButton.pack(side=LEFT,fill=BOTH,expand=True)
        self.ImpulseRButton = Radiobutton(master=self.GraphicsFrame,text="Resp al impulso",background=GRAPH_BUTTON_COLOR,fg=GRAPH_BUTTON_TEXT_COLOR,
                                     indicatoron=False,variable=self.SelectedGraph,value=IMPULSE,command=self.change_graph_button_call)
        self.ImpulseRButton.pack(side=LEFT,fill=BOTH,expand=True)
        self.StepRButton = Radiobutton(master=self.GraphicsFrame,text="Resp al Escalon",background=GRAPH_BUTTON_COLOR,fg=GRAPH_BUTTON_TEXT_COLOR,
                                     indicatoron=False,variable=self.SelectedGraph,value=STEP,command=self.change_graph_button_call)
        self.StepRButton.pack(side=LEFT,fill=BOTH,expand=True)
       
        self.GroupDelayButton = Radiobutton(master=self.GraphicsFrame,text="Retardo",background=GRAPH_BUTTON_COLOR,fg=GRAPH_BUTTON_TEXT_COLOR,
                                     indicatoron=False,variable=self.SelectedGraph,value=RETARDO,command=self.change_graph_button_call)
        self.GroupDelayButton.pack(side=LEFT,fill=BOTH,expand=True)
        self.AttRButton.select() #por default empieza seleccionado el grafico de atenuacion


        #Boton que superpone plantilla
        self.PutTemplate= IntVar()
        self.TemplateButton = Checkbutton(master=self.GraphicsFrame, text="Superponer plantilla",
                        variable=self.PutTemplate,onvalue=1, offvalue=0,command=self.put_template_call,background=GRAPH_BUTTON_COLOR,fg=GRAPH_BUTTON_TEXT_COLOR)
        self.TemplateButton.pack(side=LEFT,fill=BOTH,expand=True)
        self.SaveButton= Button(master=self.GraphicsFrame,text="Save",command=self.save_call
                                ,background=GRAPH_BUTTON_COLOR).pack(side=LEFT,fill=BOTH,expand=True)
        self.LoadButton= Button(master=self.GraphicsFrame,text="Load",command=self.load_call
                                ,background=GRAPH_BUTTON_COLOR).pack(side=LEFT,fill=BOTH,expand=True)
        self.NextButton= Button(master=self.GraphicsFrame,text="Next",command=self.next_call
                                ,background=GRAPH_BUTTON_COLOR).pack(side=LEFT,fill=BOTH,expand=True)


    def placeSliders(self):
        self.SliderFrame = LabelFrame(self.root, text="Rango de desnormalización(%)", labelanchor="n",background=FRAME_COLOR,fg=FRAME_TEXT_COLOR)
        self.SliderFrame.pack(side=LEFT,anchor=NW,fill=BOTH,expand=True)
        self.SlideNorm = Scale(master=self.SliderFrame, from_=0, to=100,orient=HORIZONTAL)
        self.SlideNorm.config(bg=BUTTON_COLOR)
        self.SlideNorm.pack(fill=BOTH,expand=True)
    def InitializeAxes(self):
        #Atenuacion
        self.Axes_Stage1= self.fig.add_subplot(111)
        self.Axes_Stage1.set_axis_off()
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
    def check_button_call(self):
        if(self.SelectedCheck.get() == NORMAL_CHECK):
            self.entry_N.config(state="disabled")
            self.entry_N_max.config(state="disabled")
            self.entry_N_min.config(state="disabled")
        elif(self.SelectedCheck.get() == N_CHECK):
            self.entry_N.config(state="normal")
            self.entry_N_max.config(state="disabled")
            self.entry_N_min.config(state="disabled")
        elif(self.SelectedCheck.get() == N_RANGE_CHECK):
            self.entry_N.config(state="disabled")
            self.entry_N_max.config(state="normal")
            self.entry_N_min.config(state="normal")
        #N
        if(self.NCheckVar):
            self.entry_N.config(state="normal")
        else:
            self.entry_N.config(state="disbaled")
        #N_range
        if(self.N_rangeCheck):
            self.entry_N_max.config(state="normal")
            self.entry_N_min.config(state="normal")
        else:
            self.entry_N_max.config(state="disabled")
            self.entry_N_min.config(state="disabled")


    def filter_call(self):
        fil=self.filter.get()
        if(self.PrevState!=fil):
            if(self.PrevState==LP or self.PrevState==HP):
                self.DestroyLP_HP_Specs()
            elif(self.PrevState==BP or self.PrevState==BR):
                self.DestroyBP_BR_Specs()
            elif(self.PrevState== GR):
                self.DestroyGR_Specs()
            if(fil==BP or fil==BR):
                self.PlaceBP_BR_Specs()
            elif(fil==LP or fil==HP):
                self.PlaceLP_HP_Specs()
            elif(fil==GR):
                self.PlaceGR_Specs()
        self.PrevState=fil
    def validate_save_call(self):
        file_string = self.SaveFileName.get() +".txt"
        file = Path(file_string)
        if file.is_file():
            messagebox.showinfo("","El archivo seleccionado ya existe")
        else:
            self.SaveWindowReturn="Ok"
            self.SaveWindow.destroy()
            
    def validate_load_call(self):
        file_string = self.LoadFileName.get() +".txt"
        file = Path(file_string)
        if file.is_file():
            self.LoadWindowReturn="Ok"
            self.LoadWindow.destroy()
        else:
            messagebox.showinfo("","El archivo seleccionado no existe")

            
    #Funciones relacionadas a graficas
    def plotPhase(self, f,fase):
        self.Fase_lines, =self.Axes_Stage1.semilogx(f,fase)

    def plotAtteNorm(self, fn,attN):
        self.AttN_lines, =self.Axes_Stage1.semilogx(fn,attN)

    def plotAtte(self, f,att):
        self.Att_lines, =self.Axes_Stage1.semilogx(f,att)

    def plotQ(self,qs):
        self.q_container =self.Axes_Stage1.stem(qs,basefmt='')
        self.q_is_in_plot=True

    def DisplayGraph(self,Xmin,Xmax,Ymin,Ymax,q):
        type_of_graph= self.SelectedGraph.get()
        self.HideAllLines()
        self.Axes_Stage1.grid(b=True,axis='both')
        self.Axes_Stage1.set_axis_on()

        if(type_of_graph == ATT):
            self.Axes_Stage1.set_xscale("log")
            self.Axes_Stage1.set_xlabel("f(Hz)")
            self.Axes_Stage1.set_ylabel("|A(f)| (dB)")
            self.Axes_Stage1.set_title("Atenuacion")
            self.Axes_Stage1.set_xlim(left=Xmin,right=Xmax)
            self.Axes_Stage1.set_ylim(bottom=Ymin,top=Ymax)
            self.Att_lines.set_visible(True)
        elif(type_of_graph == ATT_N):
            self.Axes_Stage1.set_xscale("log")
            self.Axes_Stage1.set_xlabel("fN(Hz)")
            self.Axes_Stage1.set_ylabel("|A(fN)| (dB)")
            self.Axes_Stage1.set_title("Atenuacion Normalizada")
            self.Axes_Stage1.set_xlim(left=Xmin,right=Xmax)
            self.Axes_Stage1.set_ylim(bottom=Ymin,top=Ymax)
            self.AttN_lines.set_visible(True)
        elif(type_of_graph == FASE):
            self.Axes_Stage1.set_xscale("log")
            self.Axes_Stage1.set_xlabel("f(Hz)")
            self.Axes_Stage1.set_ylabel("fase (deg)")
            self.Axes_Stage1.set_title("Fase de H(f)")
            self.Axes_Stage1.set_xlim(left=Xmin,right=Xmax)
            self.Axes_Stage1.set_ylim(bottom=Ymin,top=Ymax)
            self.Fase_lines.set_visible(True)
        elif(type_of_graph == CEROS):
            self.Axes_Stage1.set_xscale("linear")
            self.Axes_Stage1.set_xlabel("Re(s)")
            self.Axes_Stage1.set_ylabel("Im(s)")
            self.Axes_Stage1.set_title("Diagrama de polos y ceros")
            self.Axes_Stage1.set_xlim(left=Xmin,right=Xmax)
            self.Axes_Stage1.set_ylim(bottom=Ymin,top=Ymax)
            self.zeros_path.set_visible(True)
            self.poles_path.set_visible(True)
        elif(type_of_graph == RETARDO):
            self.Axes_Stage1.set_xscale("log")
            self.Axes_Stage1.set_xlabel("f(Hz)")
            self.Axes_Stage1.set_ylabel("τ (seg)")
            self.Axes_Stage1.set_title("Retardo")
            self.Axes_Stage1.set_xlim(left=Xmin,right=Xmax)
            self.Axes_Stage1.set_ylim(bottom=Ymin,top=Ymax)
            self.RG_lines.set_visible(True)  
        elif(type_of_graph == IMPULSE):
            self.Axes_Stage1.set_xscale("linear")
            self.Axes_Stage1.set_xlabel("t(seg)")
            self.Axes_Stage1.set_ylabel("h(t)")
            self.Axes_Stage1.set_title("Respuesta al impulso")
            self.Axes_Stage1.set_xlim(left=Xmin,right=Xmax)
            if(Ymax ==float('NaN') or Ymax == float('inf') or Ymin ==float('NaN') or Ymin == float('inf')):
                self.Axes_Stage1.set_ylim(bottom=-100,top=100)
            else:
                self.Axes_Stage1.set_ylim(bottom=Ymin,top=Ymax)
                self.Imp_lines.set_visible(True) 
        elif(type_of_graph == STEP):
            self.Axes_Stage1.set_xscale("linear")
            self.Axes_Stage1.set_xlabel("t(seg)")
            self.Axes_Stage1.set_ylabel("u(t)")
            self.Axes_Stage1.set_title("Respuesta al escalon")
            self.Axes_Stage1.set_xlim(left=Xmin,right=Xmax)
            if(Ymax ==float('NaN') or Ymax == float('inf') or Ymin ==float('NaN') or Ymin == float('inf')):
                self.Axes_Stage1.set_ylim(bottom=-100,top=100)
            else:
                self.Axes_Stage1.set_ylim(bottom=Ymin,top=Ymax)
                self.Step_lines.set_visible(True)

        elif(type_of_graph == Q_GRAPH):
            if(Ymax ==float('NaN') or Ymax == float('inf')):
                self.Axes_Stage1.set_xlim(left=Xmin,right=Xmax)
                self.Axes_Stage1.set_ylim(bottom=-100,top=100)
                return
            else:
                self.Axes_Stage1.set_xlim(left=Xmin,right=Xmax)
                self.Axes_Stage1.set_ylim(bottom=Ymin,top=Ymax)
            self.Axes_Stage1.set_xscale("linear")
            self.Axes_Stage1.set_xlabel("Numero de polo")
            self.Axes_Stage1.set_ylabel("Q")
            self.Axes_Stage1.set_title("Grafica del factor de calidad")
            self.Axes_Stage1.set_xlim(left=Xmin,right=Xmax)
            self.Axes_Stage1.set_ylim(bottom=Ymin,top=Ymax)
            self.plotQ(q)
            


    def placeTemplate(self,Ap,As,wp,ws,wo,Q,wpMinus,wpPlus,wsMinus,wsPlus,filt,aprox,t0,frg,Y):
        #Aunque dice w, trabaja en hertz
        fil= filt
        selected= self.SelectedGraph.get()
        if(self.TemplateOn == False):
            if((aprox!= APROXIMACIONES[3]) and (aprox!= APROXIMACIONES[4]) and selected == ATT):
                if(fil==LP):
                    self.NumRect=2
                    x0=0
                    y0=Ap #Vertice izquierdo inferior
                    ymin,ymax= self.Axes_Stage1.get_ylim()
                    width1,height1= wp,(ymax-Ap)
                    self.first_rect= patches.Rectangle((x0,y0),width1,height1,linewidth=1,edgecolor='crimson',facecolor='tomato')
                    self.Axes_Stage1.add_patch(self.first_rect)

                    x2,y2= ws,0  #Vertice izquierdo inferior del segundo rectangulo
                    xmin,xmax=self.Axes_Stage1.get_xlim()
                    width2= xmax-ws
                    height2= As
                    self.second_rect= patches.Rectangle((x2,y2),width2,height2,linewidth=1,edgecolor='crimson',facecolor='tomato')
                    self.Axes_Stage1.add_patch(self.second_rect)
                    self.TemplateOn= True
                elif(fil==HP):
                    self.NumRect=2
                    x0=0
                    y0=0 #Vertice izquierdo inferior
                    width1,height1= ws,(As)
                    self.first_rect= patches.Rectangle((x0,y0),width1,height1,linewidth=1,edgecolor='crimson',facecolor='tomato')
                    self.Axes_Stage1.add_patch(self.first_rect)

                    x2,y2= wp,Ap  #Vertice izquierdo inferior del segundo rectangulo
                    xmin,xmax=self.Axes_Stage1.get_xlim()
                    ymin,ymax= self.Axes_Stage1.get_ylim()
                    width2= xmax-wp
                    height2= ymax
                    self.second_rect= patches.Rectangle((x2,y2),width2,height2,linewidth=1,edgecolor='crimson',facecolor='tomato')
                    self.Axes_Stage1.add_patch(self.second_rect)
                    self.TemplateOn= True
                elif(fil==BP):
                    self.NumRect=3
                    xmin,xmax=self.Axes_Stage1.get_xlim()
                    ymin,ymax= self.Axes_Stage1.get_ylim()
                    x0=0
                    y0=0 #Vertice izquierdo inferior
                    width1,height1= wsMinus,(As)
                    self.first_rect= patches.Rectangle((x0,y0),width1,height1,linewidth=1,edgecolor='crimson',facecolor='tomato')
                    self.Axes_Stage1.add_patch(self.first_rect)

                    x2,y2= wpMinus,Ap  #Vertice izquierdo inferior del segundo rectangulo
                    width2= wpPlus-wpMinus
                    height2= ymax-Ap
                    self.second_rect= patches.Rectangle((x2,y2),width2,height2,linewidth=1,edgecolor='crimson',facecolor='tomato')
                    self.Axes_Stage1.add_patch(self.second_rect)

                    x3,y3= wsPlus,0  #Vertice izquierdo inferior del segundo rectangulo
                    width3= xmax-wsPlus
                    height3= As
                    self.third_rect= patches.Rectangle((x3,y3),width3,height3,linewidth=1,edgecolor='crimson',facecolor='tomato')
                    self.Axes_Stage1.add_patch(self.third_rect)
                    self.TemplateOn= True
                elif(fil==BR):
                    self.NumRect=3
                    xmin,xmax=self.Axes_Stage1.get_xlim()
                    ymin,ymax= self.Axes_Stage1.get_ylim()
                    x0=0
                    y0=Ap #Vertice izquierdo inferior
                    width1,height1= wpMinus,(ymax-Ap)
                    self.first_rect= patches.Rectangle((x0,y0),width1,height1,linewidth=1,edgecolor='crimson',facecolor='tomato')
                    self.Axes_Stage1.add_patch(self.first_rect)

                    x2,y2= wsMinus,0  #Vertice izquierdo inferior del segundo rectangulo
                    width2= wsPlus-wsMinus
                    height2= As
                    self.second_rect= patches.Rectangle((x2,y2),width2,height2,linewidth=1,edgecolor='crimson',facecolor='tomato')
                    self.Axes_Stage1.add_patch(self.second_rect)

                    x3,y3= wpPlus,Ap  #Vertice izquierdo inferior del segundo rectangulo
                    width3= xmax-wpPlus
                    height3= ymax-Ap
                    self.third_rect= patches.Rectangle((x3,y3),width3,height3,linewidth=1,edgecolor='crimson',facecolor='tomato')
                    self.Axes_Stage1.add_patch(self.third_rect)
                    self.TemplateOn= True
            elif((aprox== APROXIMACIONES[3]) or (aprox== APROXIMACIONES[4])):
                if(fil == GR):
                    self.NumRect=1
                    xmin,xmax=self.Axes_Stage1.get_xlim()
                    ymin,ymax= self.Axes_Stage1.get_ylim()
                    x0=0
                    y0=0
                    width1=frg
                    height1=(1-Y)*t0
                    self.first_rect= patches.Rectangle((x0,y0),width1,height1,linewidth=1,edgecolor='crimson',facecolor='tomato')
                    self.Axes_Stage1.add_patch(self.first_rect)
                    self.TemplateOn= True

            elif(self.TemplateOn):
                self.destroyTemplate()
        

    def destroyTemplate(self):
        if(self.NumRect==1):
            self.first_rect.remove()
            self.TemplateOn= False
        if(self.NumRect==2):
            self.first_rect.remove()
            self.second_rect.remove()
            self.TemplateOn=False
        elif(self.NumRect==3):
            self.first_rect.remove()
            self.second_rect.remove()
            self.third_rect.remove()
            self.TemplateOn=False

            
    def plotZeros(self,zeroes_r,zeroes_im,poles_r,poles_im):
        self.zeros_path=self.Axes_Stage1.scatter(zeroes_r,zeroes_im,marker="o")
        self.poles_path=self.Axes_Stage1.scatter(poles_r,poles_im,marker="x")

    def plotImpulse(self,t,y):
        self.Imp_lines, =self.Axes_Stage1.plot(t,y)

    def plotStep(self,t,y):
        self.Step_lines, =self.Axes_Stage1.plot(t,y)

    def PlotGroupDelay(self,f,t):
        self.RG_lines, = self.Axes_Stage1.plot(f,t)

    #Funciones que cambian las especificaciones
    def PlaceLP_HP_Specs(self):
        #Entrada de Ap
        self.ApLabel.pack(fill=BOTH,expand=True)
        self.entry_ap.pack(fill=BOTH,expand=True)
        #Entrada de As
        self.AsLabel.pack(fill=BOTH,expand=True)
        self.entry_as.pack(fill=BOTH,expand=True)
        #Entrada de wp
        self.wpLabel.pack(fill=BOTH,expand=True)
        self.entry_wp.pack(fill=BOTH,expand=True)
        #entrada de ws
        self.wsLabel.pack(fill=BOTH,expand=True)
        self.entry_ws.pack(fill=BOTH,expand=True)
        #checks
        self.ChecksFrame.pack(fill=BOTH,expand=True)

    def PlaceBP_BR_Specs(self):
        #Entrada de Ap
        self.ApLabel.pack(fill=BOTH, expand=True)
        self.entry_ap.pack(fill=BOTH,expand=True)
        #Entrada de As
        self.AsLabel.pack(fill=BOTH, expand=True)
        self.entry_as.pack(fill=BOTH,expand=True)
        #entrada de w0
        self.w0Label.pack(fill=BOTH, expand=True)
        self.entry_wo.config(state="normal")
        self.entry_wo.pack(fill=BOTH,expand=True)
        #entrada de Δwp
        self.ΔwpLabel.pack(fill=BOTH, expand=True)
        self.entry_Δwp.config(state='normal')
        self.entry_Δwp.pack(fill=BOTH,expand=True)
        #entrada de Δws
        self.ΔwsLabel.pack(fill=BOTH, expand=True)
        self.entry_Δws.config(state='normal')
        self.entry_Δws.pack(fill=BOTH,expand=True)
        #checks
        self.ChecksFrame.pack(fill=BOTH,expand=True)

    def PlaceGR_Specs(self):
        self.τ0Label.pack(fill=BOTH,expand=True)
        self.entry_τ0.config(state="normal")
        self.entry_τ0.pack(fill=BOTH,expand=True)
        self.wrgLabel.pack(fill=BOTH,expand=True)
        self.entry_wrg.config(state="normal")
        self.entry_wrg.pack(fill=BOTH,expand=True)
        self.YLabel.pack(fill=BOTH,expand=True)
        self.entry_Y.config(state="normal")
        self.entry_Y.pack(fill=BOTH,expand=True)
        #checks
        self.ChecksFrame.pack(fill=BOTH,expand=True)

    def DestroyLP_HP_Specs(self):
        self.ApLabel.pack_forget()
        self.AsLabel.pack_forget()
        self.entry_ap.pack_forget()
        self.entry_as.pack_forget()
        self.wpLabel.pack_forget()
        self.entry_wp.pack_forget()
        self.wsLabel.pack_forget()
        self.entry_ws.pack_forget()
        #checks
        self.ChecksFrame.pack_forget()

    def DestroyBP_BR_Specs(self):
        self.ApLabel.pack_forget()
        self.AsLabel.pack_forget()
        self.entry_ap.pack_forget()
        self.entry_as.pack_forget()
        self.w0Label.pack_forget()
        self.entry_wo.pack_forget()
        self.ΔwpLabel.pack_forget()
        self.entry_Δwp.pack_forget()
        self.ΔwsLabel.pack_forget()
        self.entry_Δws.pack_forget()
        #checks
        self.ChecksFrame.pack_forget()


    def DestroyGR_Specs(self):
        self.τ0Label.pack_forget()
        self.entry_τ0.pack_forget()
        self.wrgLabel.pack_forget()
        self.entry_wrg.pack_forget()
        self.YLabel.pack_forget()
        self.entry_Y.pack_forget()
        #checks
        self.ChecksFrame.pack_forget()


    #Ventana de save y load
    def CreateFileEntryWindow(self):
        self.SaveFileName= StringVar()
        self.SaveWindowReturn="Error"
        self.SaveWindow = Toplevel()
        self.SaveWindow.title("Save Window")
        self.SaveWindow.config(bg=BUTTON_COLOR)
        self.SaveWindowFrame= Frame(master=self.SaveWindow,bg=FRAME_COLOR)
        self.SaveWindowFrame.pack(fill=BOTH,expand=True)
        EnterButton= Button(master=self.SaveWindowFrame,text="Enter",command=self.validate_save_call
                                ,background=GRAPH_BUTTON_COLOR)
        EnterButton.pack(side="bottom",fill=BOTH,expand=True)
        NombreLabel = Label(master=self.SaveWindowFrame,text="Nombre:")
        NombreLabel.pack(side="left")
        entry = Entry(master=self.SaveWindowFrame,textvariable=self.SaveFileName,state='normal')
        entry.pack(side="right")
        self.root.wait_window(self.SaveWindow)
        return self.SaveWindowReturn
    def OpenLoadWindow(self):
        self.LoadFileName= StringVar()
        self.LoadWindowReturn="Error"
        self.LoadWindow = Toplevel()
        self.LoadWindow.title("Load Window")
        self.LoadWindow.config(bg=BUTTON_COLOR)
        self.LoadWindowFrame= Frame(master=self.LoadWindow,bg=FRAME_COLOR)
        self.LoadWindowFrame.pack(fill=BOTH,expand=True)
        EnterButton= Button(master=self.LoadWindowFrame,text="Enter",command=self.validate_load_call
                                ,background=GRAPH_BUTTON_COLOR)
        EnterButton.pack(side="bottom",fill=BOTH,expand=True)
        NombreLabel = Label(master=self.LoadWindowFrame,text="Nombre:")
        NombreLabel.pack(side="left")
        entry = Entry(master=self.LoadWindowFrame,textvariable=self.LoadFileName,state='normal')
        entry.pack(side="right")
        self.root.wait_window(self.LoadWindow)
        return self.LoadWindowReturn
    def ShowData(self,data):
        Δwp= (data.wpPlus)-(data.wpMinus)
        Δws= (data.wsPlus)-(data.wsMinus)
        self.selected_aprox.set(data.Aproximation)
        self.filter.set(data.type_of_filter)
        self.ApString.set(data.Ap)
        self.AsString.set(data.As)
        self.wpString.set(data.wp)
        self.wsString.set(data.ws)
        self.w0String.set(data.wo)
        self.ΔwpString.set(Δwp)
        self.ΔwsString.set(Δws)
        self.qString.set(data.Q)
        self.τ0String.set(data.t0)
        self.YString.set(data.Y)
        self.wrgString.set(data.wrg)
        self.SlideNorm.set(data.NormRange)


    #Extras
    def CloseGUI(self):
        self.root.destroy()
    def Update(self):
        self.Graph.draw()
        self.root.update()
    def EventSolved(self):
        self.Ev = NO_EV
    def DisplayError(self,result_str):
        messagebox.showinfo("Error en las especificaciones", result_str)

    def ShowMessage(self,string):
         messagebox.showinfo("",string)

    def HideAllLines(self):
        self.Att_lines.set_visible(False)
        self.AttN_lines.set_visible(False)
        self.Fase_lines.set_visible(False)
        self.Imp_lines.set_visible(False)
        self.zeros_path.set_visible(False)
        self.poles_path.set_visible(False)
        self.Step_lines.set_visible(False)
        self.RG_lines.set_visible(False)
        if(self.q_is_in_plot):
            self.q_container.remove()
            self.q_is_in_plot=False
    #
    #
    #
    #
    #
    #
    #
    #


    #Funciones de la segunda etapa

    def Change_to_stage2(self):
        self.AproxButtonsFrame.pack_forget()
        self.ButtonsFrame.pack_forget()
        self.SpecsFrame.pack_forget()
        self.GraphicsFrame.pack_forget()
        self.SliderFrame.pack_forget()
        self.InitializeSecondStage()

    def InitializeSecondStage(self):
        self.FullTransferFunction= IntVar()
        self.StageVar= IntVar()
        matplotlib.rcParams.update({'font.size': 8})
        self.PlaceStagesMenu()
        self.PlaceTransferFunctionGraph()
        self.PlaceOptions()

    def PlaceOptions(self):
        self.vMinString= StringVar() #Valor minimo posible a la entrada
        self.vMinString.set("vMin = 10mV")
        self.vMaxString= StringVar() #Valor maximo posible a la salida
        self.vMaxString.set("vMax = 14V")
        self.RDString= StringVar() #Variable donde se guarda el rango dinamico
        self.RDString.set("Rango dinamico = ")
        self.OptionsFrame = LabelFrame(self.root, text="Opciones",background=FRAME_COLOR,fg=FRAME_TEXT_COLOR)
        self.OptionsFrame.pack(side="right",fill=BOTH,expand=True)
        self.PrevButton= Button(master=self.OptionsFrame,text="Previous",command=self.prev_call
                                ,background=GRAPH_BUTTON_COLOR,fg=GRAPH_BUTTON_TEXT_COLOR)
        self.PrevButton.pack(anchor=SW,side=BOTTOM,fill=BOTH,expand=True)
        self.CreateStageButon= Button(master=self.OptionsFrame,text="Create Stage",command=self.create_stage_call
                                ,background=GRAPH_BUTTON_COLOR,fg=GRAPH_BUTTON_TEXT_COLOR)
        self.CreateStageButon.pack(side=BOTTOM,fill=BOTH,expand=True)
        self.DeleteStageButon= Button(master=self.OptionsFrame,text="Delete Stage",command=self.delete_stage_call
                                ,background=GRAPH_BUTTON_COLOR,fg=GRAPH_BUTTON_TEXT_COLOR)
        self.DeleteStageButon.pack(side=BOTTOM,fill=BOTH,expand=True)
        

        self.VminLabel= Label(master=self.OptionsFrame,textvariable=self.vMinString,background=BUTTON_COLOR,fg=GRAPH_BUTTON_TEXT_COLOR)
        self.VminLabel.pack(anchor=SW,fill=BOTH,expand=True)

        self.VmaxLabel= Label(master=self.OptionsFrame,textvariable=self.vMaxString,background=BUTTON_COLOR,fg=GRAPH_BUTTON_TEXT_COLOR)
        self.VmaxLabel.pack(anchor=SW,fill=BOTH,expand=True)

        self.RangoDText= Label(master=self.OptionsFrame,bg=BUTTON_COLOR,textvariable=self.RDString,
                               fg=BUTTON_FONT_COLOR)
        self.RangoDText.pack(side="top",fill=BOTH,expand=True)

    def PlaceTransferFunctionGraph(self):
        self.fzString= StringVar()
        self.fpString= StringVar()
        self.QzString= StringVar()
        self.QpString= StringVar()
        self.G0String= StringVar()

        self.TransferGraphsFrame= LabelFrame(master=self.root, text="Graficos de Ganancias",background=FRAME_COLOR,fg=FRAME_TEXT_COLOR)
        self.TransferGraphsFrame.pack(side="left",fill=BOTH,expand=True)

        #Seccion con la etapa seleccionada
        self.StageGraphFrame= LabelFrame(master=self.TransferGraphsFrame,background=FRAME_COLOR,fg=FRAME_TEXT_COLOR)
        self.StageGraphFrame.pack(side="left",fill=BOTH,expand=True)
        self.CurrentStageFig=Figure(figsize=(1,1), dpi=200,facecolor="lavender",constrained_layout=True)
        self.CurrentStageCanvas = FigureCanvasTkAgg(self.CurrentStageFig,master=self.StageGraphFrame)
        self.CurrentStageCanvas.get_tk_widget().config( width=(GRAPH_WIDTH/2), height=(GRAPH_HEIGHT/2))
        self.CurrentStageCanvas.get_tk_widget().pack(side="right",fill=BOTH,expand=True)
        self.AxesSelectedStage = self.CurrentStageFig.add_subplot(111)

        #Creo una toolbar para los graficos
        self.SelStagetoolbarFrame = Frame(master=self.StageGraphFrame)
        self.SelStagetoolbarFrame.pack(side="bottom")

        self.SelStagetoolbar = NavigationToolbar2Tk(self.CurrentStageCanvas, self.SelStagetoolbarFrame)
        self.SelStagetoolbar.pack()
        #Parametros de interes de la etapa seleccionada
        self.StageParamsFrame= LabelFrame(self.StageGraphFrame,text="Parametros de interes",background=FRAME_COLOR,fg=FRAME_TEXT_COLOR)
        self.StageParamsFrame.pack(side="left")
        #fp
        self.TransfwpLabel= Label(master=self.StageParamsFrame,text="fp(Hz)",background=BUTTON_COLOR,fg=BUTTON_FONT_COLOR)
        self.TransfwpLabel.pack(fill=BOTH,expand=True)
        self.entry_Transfwz=Entry(master=self.StageParamsFrame,textvariable=self.fpString)
        self.entry_Transfwz.pack(fill=BOTH,expand=True)
        #H(0)
        self.G0Label= Label(master=self.StageParamsFrame,text="H(0)(dB)",background=BUTTON_COLOR,fg=BUTTON_FONT_COLOR)
        self.G0Label.pack(fill=BOTH,expand=True)
        self.entry_G0=Entry(master=self.StageParamsFrame,textvariable=self.G0String)
        self.entry_G0.pack(fill=BOTH,expand=True)
        #Qp
        self.QpLabel= Label(master=self.StageParamsFrame,text="Qp",background=BUTTON_COLOR,fg=BUTTON_FONT_COLOR)
        self.QpLabel.pack(fill=BOTH,expand=True)
        self.entry_Qp=Entry(master=self.StageParamsFrame,textvariable=self.QpString)
        self.entry_Qp.pack(fill=BOTH,expand=True)

        self.TotalCheck = Checkbutton(master=self.StageParamsFrame, text="Cascada",
                        variable=self.FullTransferFunction,onvalue=1, offvalue=0,command=self.full_transfer_call,
                        background=BUTTON_COLOR,fg=GRAPH_BUTTON_TEXT_COLOR)
        self.TotalCheck.pack()

    def PlaceStagesMenu(self):
        self.StagesMenuFrame= LabelFrame(self.root, text="Etapas",background=FRAME_COLOR,fg=FRAME_TEXT_COLOR)
        self.StagesMenuFrame.pack(side="bottom")

    def SetStagesButtons(self,n):
        self.StagesButtons=[]
        for i in range(1,n+1):
            aux= "Etapa "+str(i)
            self.StagesButtons.append(Radiobutton(master= self.StagesMenuFrame,text=aux,bg=BUTTON_COLOR,
                                                  indicatoron=False,variable=self.StageVar,value=i,
                                                  command=self.select_stage_call))
            self.StagesButtons[i-1].pack(side="left",fill=BOTH,expand=True)
        self.StagesButtons[0].select()

    #Callbacks de la segunda etapa
    def select_stage_call(self):
        self.Ev=SELECT_STAGE_EV
    def export_call(self):
        self.Ev=EXPORT
    
    def delete_stage_call(self):
        self.Ev= DELETE_STAGE_EV
    def reset_stage_call(self):
        self.Ev=RESET
    def create_stage_call(self):
        self.Ev=CREATE_STAGE_EV
    def prev_call(self):
        self.Ev= PREV_EV
    def ShowPrevMessage(self):
        if messagebox.askokcancel("Volver", "Desea volver a la etapa de diseño previa?"):
            return True
        else:
            return False

    def Change_to_stage1(self):
        #Saco los elementos de la segunda etapa
        self.OptionsFrame.destroy()
        self.TransferGraphsFrame.destroy()
        self.StagesMenuFrame.destroy()
        #Vuelvo a poner los elementos de la primera etapa
        self.GraphicsFrame.pack(anchor=NE,side=RIGHT,fill=BOTH,expand=True)
        self.ButtonsFrame.pack(anchor=NW,fill=BOTH,expand=True)
        self.AproxButtonsFrame.pack(anchor=NW,fill=BOTH,expand=True)
        self.SpecsFrame.pack(anchor=NW,fill=BOTH,expand=True)
        self.SliderFrame.pack(side=LEFT,anchor=NW,fill=BOTH,expand=True)
    def GraphTotalTransference(self,f,mag,xmin,xmax,ymin,ymax):
        self.AxesSelectedStage.cla()
        self.AxesSelectedStage.set_xscale("log")
        self.AxesSelectedStage.set_title("Ganancia en cascada")
        self.AxesSelectedStage.set_xlabel("f(Hz)")
        self.AxesSelectedStage.set_ylabel("|H(f)|(dB)")
        self.AxesSelectedStage.set_xlim(left=xmin,right=xmax)
        self.AxesSelectedStage.set_ylim(bottom=ymin,top=ymax)
        self.AxesSelectedStage.semilogx(f,mag)
        self.AxesSelectedStage.grid(b=True,axis='both')

    def GraphSelectedStage(self,f,mag,xmin,xmax,ymin,ymax,i):
        self.AxesSelectedStage.cla()
        self.AxesSelectedStage.set_xscale("log")
        self.AxesSelectedStage.set_title("Ganancia de la etapa "+str(i))
        self.AxesSelectedStage.set_xlabel("f(Hz)")
        self.AxesSelectedStage.set_ylabel("G"+str(i)+"(dB)")
        self.AxesSelectedStage.set_xlim(left=xmin,right=xmax)
        self.AxesSelectedStage.set_ylim(bottom=ymin,top=ymax)
        self.AxesSelectedStage.semilogx(f,mag)
        self.AxesSelectedStage.grid(b=True,axis='both')
    def UpdateParameters(self,fp,qp,G0,Rd):
        self.fpString.set(str(int(fp)))
        self.QpString.set(str(int(qp)))
        self.G0String.set(str(int(G0)))
        self.RDString.set("Rango dinamico = "+str(int(Rd)))
    def full_transfer_call(self):
        self.Ev=TRANSFER_FUNCTION_CHECK_EV
    def DeleteStageButton(self,i):
        aux= self.StagesButtons.pop(i)
        aux.destroy()