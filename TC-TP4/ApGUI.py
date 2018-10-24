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
#Grafica activa
ATT=1
ATT_N=2
FASE=3
CEROS=4
RETARDO=5
IMPULSE=6
STEP=7
Q_GRAPH=8
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
        self.TemplateOn=False
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
        self.selected_aprox.set(APROXIMACIONES[0]) # Empieza conButterworth como default

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
        self.ΔwpString= StringVar()
        self.ΔwsString= StringVar()
        self.τ0String= StringVar()
        self.wrgString= StringVar()
        self.YString= StringVar()

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
        #entrada de Q
        self.QLabel= Label(master=self.SpecsFrame,text="Q",anchor=W,background=BUTTON_COLOR,fg=BUTTON_FONT_COLOR)
        self.entry_Q=Entry(master=self.SpecsFrame,textvariable=self.qString,state='disabled')
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
        self.q_container =self.Axes_Stage1.stem(qs,basefmt=''
                                                )

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
            self.Axes_Stage1.set_ylim(bottom=Ymin,top=Ymax)
            self.Imp_lines.set_visible(True) 
        elif(type_of_graph == STEP):
            self.Axes_Stage1.set_xscale("linear")
            self.Axes_Stage1.set_xlabel("t(seg)")
            self.Axes_Stage1.set_ylabel("u(t)")
            self.Axes_Stage1.set_title("Respuesta al escalon")
            self.Axes_Stage1.set_xlim(left=Xmin,right=Xmax)
            self.Axes_Stage1.set_ylim(bottom=Ymin,top=Ymax)
            self.Step_lines.set_visible(True)
        elif(type_of_graph == Q_GRAPH):
            self.Axes_Stage1.set_xscale("linear")
            self.Axes_Stage1.set_xlabel("Numero de polo")
            self.Axes_Stage1.set_ylabel("Q")
            self.Axes_Stage1.set_title("Grafica del factor de calidad")
            self.Axes_Stage1.set_xlim(left=Xmin,right=Xmax)
            self.Axes_Stage1.set_ylim(bottom=Ymin,top=Ymax)
            #self.plotQ(q)


    def placeTemplate(self,Ap,As,wp,ws,wo,Q,wpMinus,wpPlus,wsMinus,wsPlus):
        #Aunque dce w, trabaja en hertz
        fil= self.filter.get()
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
        

    def destroyTemplate(self):
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
        #entrada de Q
        self.QLabel.pack(fill=BOTH, expand=True)
        self.entry_Q.config(state='normal')
        self.entry_Q.pack(fill=BOTH,expand=True)
        #entrada de Δwp
        self.ΔwpLabel.pack(fill=BOTH, expand=True)
        self.entry_Δwp.config(state='normal')
        self.entry_Δwp.pack(fill=BOTH,expand=True)
        #entrada de Δws
        self.ΔwsLabel.pack(fill=BOTH, expand=True)
        self.entry_Δws.config(state='normal')
        self.entry_Δws.pack(fill=BOTH,expand=True)

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

    def DestroyLP_HP_Specs(self):
        self.ApLabel.pack_forget()
        self.AsLabel.pack_forget()
        self.entry_ap.pack_forget()
        self.entry_as.pack_forget()
        self.wpLabel.pack_forget()
        self.entry_wp.pack_forget()
        self.wsLabel.pack_forget()
        self.entry_ws.pack_forget()

    def DestroyBP_BR_Specs(self):
        self.ApLabel.pack_forget()
        self.AsLabel.pack_forget()
        self.entry_ap.pack_forget()
        self.entry_as.pack_forget()
        self.w0Label.pack_forget()
        self.entry_wo.pack_forget()
        self.QLabel.pack_forget()
        self.entry_Q.pack_forget()
        self.ΔwpLabel.pack_forget()
        self.entry_Δwp.pack_forget()
        self.ΔwsLabel.pack_forget()
        self.entry_Δws.pack_forget()

    def DestroyGR_Specs(self):
        self.τ0Label.pack_forget()
        self.entry_τ0.pack_forget()
        self.wrgLabel.pack_forget()
        self.entry_wrg.pack_forget()
        self.YLabel.pack_forget()
        self.entry_Y.pack_forget()
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
        self.PlaceStagesMenu()
        self.PlaceTransferFunctionGraph()
        self.PlaceOptions()

    def PlaceOptions(self):
        self.vMinString= StringVar() #Valor minimo posible a la entrada
        self.vMinString.set("10")
        self.vMaxString= StringVar() #Valor maximo posible a la salida
        self.vMaxString.set("14")
        self.RDString= StringVar() #Variable donde se guarda el rango dinamico
        self.RDString.set("")
        self.OptionsFrame = LabelFrame(self.root, text="Opciones",background=FRAME_COLOR,fg=FRAME_TEXT_COLOR)
        self.OptionsFrame.pack(side="left",fill=BOTH,expand=True)
        self.PrevButton= Button(master=self.OptionsFrame,text="Previous",command=self.prev_call
                                ,background=GRAPH_BUTTON_COLOR,fg=GRAPH_BUTTON_TEXT_COLOR)
        self.PrevButton.pack(anchor=SW,side=BOTTOM,fill=BOTH,expand=True)
        self.Save2Button= Button(master=self.OptionsFrame,text="Save",command=self.save_call
                                ,background=GRAPH_BUTTON_COLOR,fg=GRAPH_BUTTON_TEXT_COLOR)
        self.Save2Button.pack(anchor=SW,side=BOTTOM,fill=BOTH,expand=True)
        self.Load2Button= Button(master=self.OptionsFrame,text="Load",command=self.load_call
                                ,background=GRAPH_BUTTON_COLOR,fg=GRAPH_BUTTON_TEXT_COLOR)
        self.Load2Button.pack(anchor=SW,side=BOTTOM,fill=BOTH,expand=True)
        self.ExportButton= Button(master=self.OptionsFrame,text="Export H(s) as txt",command=self.export_call
                                ,background=GRAPH_BUTTON_COLOR,fg=GRAPH_BUTTON_TEXT_COLOR)
        self.ExportButton.pack(anchor=SW,side=BOTTOM,fill=BOTH,expand=True)
        self.CreateStageButon= Button(master=self.OptionsFrame,text="Create Stage",command=self.create_stage_call
                                ,background=GRAPH_BUTTON_COLOR,fg=GRAPH_BUTTON_TEXT_COLOR)
        self.CreateStageButon.pack(side=BOTTOM,fill=BOTH,expand=True)
        self.DeleteStageButon= Button(master=self.OptionsFrame,text="Delete Stage",command=self.delete_stage_call
                                ,background=GRAPH_BUTTON_COLOR,fg=GRAPH_BUTTON_TEXT_COLOR)
        self.DeleteStageButon.pack(side=BOTTOM,fill=BOTH,expand=True)
        self.ResetStageButon= Button(master=self.OptionsFrame,text="Reset",command=self.reset_stage_call
                                ,background=GRAPH_BUTTON_COLOR,fg=GRAPH_BUTTON_TEXT_COLOR)
        self.ResetStageButon.pack(side=BOTTOM,fill=BOTH,expand=True)
        

        self.VminLabel= Label(master=self.OptionsFrame,text="Vmin(mV)",background=GRAPH_BUTTON_COLOR,fg=GRAPH_BUTTON_TEXT_COLOR)
        self.VminLabel.pack(anchor=SW,fill=BOTH,expand=True)
        self.entry_Vmin=Entry(master=self.OptionsFrame,textvariable=self.vMinString)
        self.entry_Vmin.pack(anchor=SE,fill=BOTH,expand=True)

        self.VmaxLabel= Label(master=self.OptionsFrame,text="Vmax(V)",background=GRAPH_BUTTON_COLOR,fg=GRAPH_BUTTON_TEXT_COLOR)
        self.VmaxLabel.pack(anchor=SW,fill=BOTH,expand=True)
        self.entry_Vmax=Entry(master=self.OptionsFrame,textvariable=self.vMaxString)
        self.entry_Vmax.pack(anchor=SE,fill=BOTH,expand=True)

        self.RangoDText= Label(master=self.OptionsFrame, text="RangoDin(dB)="+self.RDString.get(),
                               bg=BUTTON_COLOR,textvariable=self.RDString,fg=BUTTON_FONT_COLOR)
        self.RangoDText.pack(side="top",fill=BOTH,expand=True)

    def PlaceTransferFunctionGraph(self):
        self.fzString= StringVar()
        self.fpString= StringVar()
        self.QzString= StringVar()
        self.QpString= StringVar()
        self.G0String= StringVar()

        self.TransferGraphsFrame= LabelFrame(master=self.root, text="Ganancias",background=FRAME_COLOR,fg=FRAME_TEXT_COLOR)
        self.TransferGraphsFrame.pack(side="right",fill=BOTH,expand=True)

        #Seccion con la etapa seleccionada
        self.StageGraphFrame= LabelFrame(master=self.TransferGraphsFrame, text="Etapa seleccionada",background=FRAME_COLOR,fg=FRAME_TEXT_COLOR)
        self.StageGraphFrame.pack(side="right",fill=BOTH,expand=True)
        self.CurrentStageFig=Figure(figsize=(0.1,0.1), dpi=200,facecolor="lavender",constrained_layout=True)
        self.CurrentStageCanvas = FigureCanvasTkAgg(self.CurrentStageFig,master=self.StageGraphFrame)
        self.CurrentStageCanvas.get_tk_widget().config( width=(GRAPH_WIDTH/3), height=(GRAPH_HEIGHT/3))
        self.CurrentStageCanvas.get_tk_widget().pack(side=TOP,fill=BOTH,expand=True)
        #Creo una toolbar para los graficos
        self.SelStagetoolbarFrame = Frame(master=self.StageGraphFrame)
        self.SelStagetoolbarFrame.pack(side=TOP,fill=BOTH,expand=True)
        self.SelStagetoolbar = NavigationToolbar2Tk(self.CurrentStageCanvas, self.SelStagetoolbarFrame)
        self.SelStagetoolbar.pack(fill=BOTH,expand=True)
        #Parametros de interes de la etapa seleccionada
        self.StageParamsFrame= LabelFrame(self.StageGraphFrame,text="Parametros de interes",background=FRAME_COLOR,fg=FRAME_TEXT_COLOR)
        self.StageParamsFrame.pack(side="top",fill=BOTH,expand=True)
        #fz
        self.TransfwzLabel= Label(master=self.StageParamsFrame,text="fz(Hz)",background=BUTTON_COLOR,fg=BUTTON_FONT_COLOR)
        self.TransfwzLabel.pack(fill=BOTH,expand=True)
        self.entry_Transfwz=Entry(master=self.StageParamsFrame,textvariable=self.fzString)
        self.entry_Transfwz.pack(anchor=NE,fill=BOTH,expand=True)
        #fp
        self.TransfwpLabel= Label(master=self.StageParamsFrame,text="fp(Hz)",background=BUTTON_COLOR,fg=BUTTON_FONT_COLOR)
        self.TransfwpLabel.pack(fill=BOTH,expand=True)
        self.entry_Transfwz=Entry(master=self.StageParamsFrame,textvariable=self.fpString)
        self.entry_Transfwz.pack(anchor=NE,fill=BOTH,expand=True)
        #H(0)
        self.G0Label= Label(master=self.StageParamsFrame,text="H(0)(dB)",background=BUTTON_COLOR,fg=BUTTON_FONT_COLOR)
        self.G0Label.pack(fill=BOTH,expand=True)
        self.entry_G0=Entry(master=self.StageParamsFrame,textvariable=self.G0String)
        self.entry_G0.pack(anchor=NE,fill=BOTH,expand=True)
        #Qp
        self.QpLabel= Label(master=self.StageParamsFrame,text="Qp",background=BUTTON_COLOR,fg=BUTTON_FONT_COLOR)
        self.QpLabel.pack(fill=BOTH,expand=True)
        self.entry_Qp=Entry(master=self.StageParamsFrame,textvariable=self.QpString)
        self.entry_Qp.pack(anchor=NE,fill=BOTH,expand=True)
        #Qz
        self.QzLabel= Label(master=self.StageParamsFrame,text="Qz",background=BUTTON_COLOR,fg=BUTTON_FONT_COLOR)
        self.QzLabel.pack(fill=BOTH,expand=True)
        self.entry_Qz=Entry(master=self.StageParamsFrame,textvariable=self.QzString)
        self.entry_Qz.pack(anchor=NE,fill=BOTH,expand=True)

        #Seccion con la ganancia de todas las etapas en cascada
        self.CascadeGraphFrame= LabelFrame(master=self.TransferGraphsFrame, text="Ganancia total(cascada)",background=FRAME_COLOR,fg=FRAME_TEXT_COLOR)
        self.CascadeGraphFrame.pack(side="left",fill=BOTH,expand=True)
        self.TransfTotalFig=Figure(figsize=(0.1,0.1), dpi=200,facecolor="lavender",constrained_layout=True)
        self.TransfTotalCanvas = FigureCanvasTkAgg(self.TransfTotalFig,master=self.CascadeGraphFrame)
        self.TransfTotalCanvas.get_tk_widget().config( width=(GRAPH_WIDTH/3), height=(GRAPH_HEIGHT/3))
        self.TransfTotalCanvas.get_tk_widget().pack(side=TOP,fill=BOTH,expand=True)
        #Creo una toolbar para la grafica de cascada
        self.TransfTotToolbarFrame = Frame(master=self.CascadeGraphFrame)
        self.TransfTotToolbarFrame.pack(side=TOP,fill=BOTH,expand=True)
        self.TransfTotToolbar = NavigationToolbar2Tk(self.TransfTotalCanvas, self.TransfTotToolbarFrame)
        self.TransfTotToolbar.pack(fill=BOTH,expand=True)

    def PlaceStagesMenu(self):
        self.StagesMenuFrame= LabelFrame(self.root, text="Etapas",background=FRAME_COLOR,fg=FRAME_TEXT_COLOR)
        self.StagesMenuFrame.pack(side="bottom",fill=BOTH,expand=True)
        self.etapa1button= Button(master=self.StagesMenuFrame,text="Etapa1",background=BUTTON_COLOR,fg=BUTTON_FONT_COLOR)
        self.etapa1button.pack(side="left",fill=BOTH,expand=True)
    #Callbacks de la segunda etapa
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