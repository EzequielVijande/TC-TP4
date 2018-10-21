import matplotlib
matplotlib.use('TkAgg')
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.backend_bases import key_press_handler
from matplotlib.figure import Figure

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

        self.SpecsFrame = LabelFrame(self.root, text="Especificaciones", labelanchor="n",background="goldenrod")
        self.SpecsFrame.pack(anchor=NW,fill=BOTH,expand=True)
        #Entrada de Ap
        self.ApLabel= Label(master=self.SpecsFrame,text="Ap(dB)",anchor=W,background="light goldenrod")
        self.ApLabel.pack(fill=BOTH,expand=True)
        self.entry_ap=Entry(master=self.SpecsFrame,textvariable=self.ApString)
        self.entry_ap.pack(anchor=NE,fill=BOTH,expand=True)
        #Entrada de As
        self.AsLabel= Label(master=self.SpecsFrame,text="As(dB)",anchor=W,background="light goldenrod")
        self.AsLabel.pack(fill=BOTH,expand=True)
        self.entry_as=Entry(master=self.SpecsFrame,textvariable=self.AsString)
        self.entry_as.pack(anchor=NE,fill=BOTH,expand=True)
        #Entrada de wp
        self.wpLabel= Label(master=self.SpecsFrame,text="wp(rad/seg)",anchor=W,background="light goldenrod")
        self.wpLabel.pack(fill=BOTH,expand=True)
        self.entry_wp=Entry(master=self.SpecsFrame,textvariable=self.wpString)
        self.entry_wp.pack(anchor=NE,fill=BOTH,expand=True)
        #entrada de ws
        self.wsLabel= Label(master=self.SpecsFrame,text="ws(rad/seg)",anchor=W,background="light goldenrod")
        self.wsLabel.pack(fill=BOTH,expand=True)
        self.entry_ws=Entry(master=self.SpecsFrame,textvariable=self.wsString)
        self.entry_ws.pack(anchor=NE,fill=BOTH,expand=True)
        #entrada de w0
        self.w0Label= Label(master=self.SpecsFrame,text="wo(rad/seg)",anchor=W,background="light goldenrod")
        self.entry_wo=Entry(master=self.SpecsFrame,textvariable=self.w0String,state='disabled')
        #entrada de Q
        self.QLabel= Label(master=self.SpecsFrame,text="Q",anchor=W,background="light goldenrod")
        self.entry_Q=Entry(master=self.SpecsFrame,textvariable=self.qString,state='disabled')
        #entrada de Δwp
        self.ΔwpLabel= Label(master=self.SpecsFrame,text="Δwp(rad/seg)",anchor=W,background="light goldenrod")
        self.entry_Δwp=Entry(master=self.SpecsFrame,textvariable=self.ΔwpString,state='disabled')
        #entrada de Δws
        self.ΔwsLabel= Label(master=self.SpecsFrame,text="Δws(rad/seg)",anchor=W,background="light goldenrod")
        self.entry_Δws=Entry(master=self.SpecsFrame,textvariable=self.ΔwsString,state='disabled')
        #entrada de τ(0)
        self.τ0Label= Label(master=self.SpecsFrame,text="τ(0) (seg)",anchor=W,background="light goldenrod")
        self.entry_τ0=Entry(master=self.SpecsFrame,textvariable=self.τ0String,state='disabled')
        #Entrada de wrg
        self.wrgLabel=Label(master=self.SpecsFrame,text="wrg (rad/seg)",anchor=W,background="light goldenrod")
        self.entry_wrg=Entry(master=self.SpecsFrame,textvariable=self.wrgString,state='disabled')
        #Entrada de Y
        self.YLabel=Label(master=self.SpecsFrame,text="Y",anchor=W,background="light goldenrod")
        self.entry_Y=Entry(master=self.SpecsFrame,textvariable=self.YString,state='disabled')

    def PlaceGraphic(self):
        self.GraphicsFrame = LabelFrame(self.root, text="Graficas", labelanchor="n",background="goldenrod")
        self.GraphicsFrame.pack(anchor=NE,side=RIGHT,fill=BOTH,expand=True)
        self.fig=Figure(figsize=(1,1), dpi=200,facecolor="lavender",constrained_layout=True)
        self.Graph = FigureCanvasTkAgg(self.fig,master=self.GraphicsFrame)
        self.Graph.get_tk_widget().config( width=GRAPH_WIDTH, height=GRAPH_HEIGHT)
        self.Graph.get_tk_widget().pack(side=TOP,fill=BOTH,expand=True)
        #Setteo de los axes
        self.InitializeAxes()

        #Creo una toolbar para los graficos
        toolbarFrame = Frame(master=self.GraphicsFrame)
        toolbarFrame.pack(side=TOP,fill=BOTH,expand=True)
        toolbar = NavigationToolbar2Tk(self.Graph, toolbarFrame)
        toolbar.pack(fill=BOTH,expand=True)
        #Botones para cambiar de graficas
        self.SelectedGraph= tk.IntVar()
        self.AttRButton= Radiobutton(master=self.GraphicsFrame,text="Atenuacion",background="pale turquoise",
                                     indicatoron=False,variable=self.SelectedGraph,value=ATT,command=self.change_graph_button_call)
        self.AttRButton.pack(side=LEFT,fill=BOTH,expand=True)
        self.AttNRButton = Radiobutton(master=self.GraphicsFrame,text="Atenuacion Norm",background="pale turquoise",
                                     indicatoron=False,variable=self.SelectedGraph,value=ATT_N,command=self.change_graph_button_call)
        self.AttNRButton.pack(side=LEFT,fill=BOTH,expand=True)
        self.FaseRButton = Radiobutton(master=self.GraphicsFrame,text="Fase",background="pale turquoise",
                                     indicatoron=False,variable=self.SelectedGraph,value=FASE,command=self.change_graph_button_call)
        self.FaseRButton.pack(side=LEFT,fill=BOTH,expand=True)
        self.ZeroesRButton =Radiobutton(master=self.GraphicsFrame,text="Polos y ceros",background="pale turquoise",
                                     indicatoron=False,variable=self.SelectedGraph,value=CEROS,command=self.change_graph_button_call)
        self.ZeroesRButton.pack(side=LEFT,fill=BOTH,expand=True)
        self.ImpulseRButton = Radiobutton(master=self.GraphicsFrame,text="Resp al impulso",background="pale turquoise",
                                     indicatoron=False,variable=self.SelectedGraph,value=IMPULSE,command=self.change_graph_button_call)
        self.ImpulseRButton.pack(side=LEFT,fill=BOTH,expand=True)
        self.StepRButton = Radiobutton(master=self.GraphicsFrame,text="Resp al Escalon",background="pale turquoise",
                                     indicatoron=False,variable=self.SelectedGraph,value=STEP,command=self.change_graph_button_call)
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
    def InitializeAxes(self):
        #Atenuacion
        self.Att_axes= self.fig.add_subplot(111,xlabel="f(Hz)",ylabel="|A(f)|(dB)")
        #Atenuacion normalizada
        self.AttN_axes= self.fig.add_subplot(111,xlabel="fN(Hz)",ylabel="|A(fN)|(dB)")
        #Diagrama de polos y ceros
        self.PZ_axes= self.fig.add_subplot(111,xlabel="Re(s)",ylabel="Im(s)")
        #Fase
        self.Fase_axes= self.fig.add_subplot(111,xlabel="f(Hz)",ylabel="fase de H(deg)")
        #Q
        self.Q_axes= self.fig.add_subplot(111,xlabel="Numero de curva",ylabel="Qmaximo")
        #Rechaza Banda
        self.RG_axes= self.fig.add_subplot(111,xlabel="f(Hz)",ylabel="τ(seg)")
        #Respuesta al impulso
        self.Imp_axes= self.fig.add_subplot(111,xlabel="t(seg)",ylabel="h(t)")
        #Respuesta al escalon
        self.Step_axes= self.fig.add_subplot(111,xlabel="t(seg)",ylabel="u(t)")

        self.Att_axes.set_axis_off()
        self.AttN_axes.set_axis_off()
        self.PZ_axes.set_axis_off()
        self.Fase_axes.set_axis_off()
        self.Q_axes.set_axis_off()
        self.RG_axes.set_axis_off()
        self.Imp_axes.set_axis_off()
        self.Step_axes.set_axis_off()

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
            
    #Funciones relacionadas a graficas
    def plotPhase(self, w,fase):
        self.Fase_axes.cla()
        self.Fase_lines=self.Fase_axes.plot(w,fase)

    def plotAtteNorm(self, w,attN):
        self.AttN_axes.cla()
        self.AttN_lines=self.AttN_axes.plot(w,attN)

    def plotAtte(self, w,att):
        self.Att_axes.cla()
        self.Att_lines=self.Att_axes.plot(w,att)

    def plotQ(self,qs):
        self.Q_axes.cla()
        self.q_lines=self.Q_axes.stem(qs)

    def DisplayGraph(self,axis):
        self.TurnOffAxes()
        axis.grid(b=True,axis='both')
        axis.set_axis_on()
        self.Graph.draw()

    def placeTemplate(self,Ap,As,wp,ws,wo,Q,wpMinus,wpPlus,wsMinus,wsPlus):
        fil= self.filter.get()
        if(fil==LP):
            self.NumRect=2

            x0,y0= self.TransformToCanvasCoords(100*ws,2*As,0,2*As) #Vertice izquierdo superior
            x1,y1= self.TransformToCanvasCoords(100*ws,2*As,wp,Ap) #Vertice derecho inferior
            self.first_rect= self.Graph.create_rectangle(x0, y0,x1, y1, fill="firebrick")

            x2,y2= self.TransformToCanvasCoords(100*ws,2*As,ws,As) #Vertice izquierdo superior
            x3,y3= self.TransformToCanvasCoords(100*ws,2*As,100*ws,0) #Vertice derecho inferior
            self.second_rect= self.Graph.create_rectangle(x0, y0,x1, y1, fill="firebrick")
        elif(fil==HP):
            self.NumRect=2
            x0,y0= self.TransformToCanvasCoords(100*wp,2*As,0,As) #Vertice izquierdo superior
            x1,y1= self.TransformToCanvasCoords(100*wp,2*As,ws,0) #Vertice derecho inferior
            self.first_rect= self.Graph.create_rectangle(x0, y0,x1, y1, fill="firebrick")

            x2,y2= self.TransformToCanvasCoords(100*wp,2*As,wp,2*As) #Vertice izquierdo superior
            x3,y3= self.TransformToCanvasCoords(100*wp,2*As,100*wp,Ap) #Vertice derecho inferior
            self.second_rect= self.Graph.create_rectangle(x0, y0,x1, y1, fill="firebrick")

    def destroyTemplate(self):
        if(self.NumRect==2):
            self.Graph.delete(self.first_rect)
            self.Graph.delete(self.second_rect)

            
    def plotZeros(self,sigma,w):
        self.PZ_axes.cla()
        self.PZ_lines=self.PZ_axes.plot(sigma,w)

    def plotImpulse(self,t,y):
        self.Imp_axes.cla()
        self.Imp_lines=self.Imp_axes.plot(t,y)

    def plotStep(self,t,y):
        self.Step_axes.cla()
        self.Step_lines=self.Step_axes.plot(t,y)

    def PlotGroupDelay(self,f,t):
        self.RG_axes.cla()
        self.RG_lines= self.RG_axes.plot(f,t)

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

    #Extras
    def CloseGUI(self):
        self.root.destroy()
    def Update(self):
        self.root.update()
    def EventSolved(self):
        self.Ev = NO_EV
    def DisplayError(self,result_str):
        messagebox.showinfo("Error en las especificaciones", result_str)
    def TransformToCanvasCoords(self,max_X,max_Y,x,y):
        y_out=GRAPH_HEIGHT-( (y*GRAPH_HEIGHT)/max_Y)
        x_out=((x*GRAPH_WIDTH)/max_X)
        return (x_out,y_out)
    def TurnOffAxes(self):
        self.Att_axes.set_axis_off()
        self.AttN_axes.set_axis_off()
        self.PZ_axes.set_axis_off()
        self.Fase_axes.set_axis_off()
        self.Q_axes.set_axis_off()
        self.RG_axes.set_axis_off()
        self.Imp_axes.set_axis_off()
        self.Step_axes.set_axis_off()
    

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
        self.vMaxString= StringVar() #Valor maximo posible a la salida
        self.RDString= StringVar() #Variable donde se guarda el rango dinamico
        self.OptionsFrame = LabelFrame(self.root, text="Opciones",background="goldenrod")
        self.OptionsFrame.pack(side="left",fill=BOTH,expand=True)
        self.PrevButton= Button(master=self.OptionsFrame,text="Previous",command=self.prev_call
                                ,background="pale turquoise")
        self.PrevButton.pack(anchor=SW,side=BOTTOM,fill=BOTH,expand=True)
        self.Save2Button= Button(master=self.OptionsFrame,text="Save",command=self.save_call
                                ,background="pale turquoise")
        self.Save2Button.pack(anchor=SW,side=BOTTOM,fill=BOTH,expand=True)
        self.Load2Button= Button(master=self.OptionsFrame,text="Load",command=self.load_call
                                ,background="pale turquoise")
        self.Load2Button.pack(anchor=SW,side=BOTTOM,fill=BOTH,expand=True)
        self.ExportButton= Button(master=self.OptionsFrame,text="Export H(s) as txt",command=self.load_call
                                ,background="pale turquoise")
        self.ExportButton.pack(anchor=SW,side=BOTTOM,fill=BOTH,expand=True)

        self.VminLabel= Label(master=self.OptionsFrame,text="Vmin(mV)",background="light goldenrod")
        self.VminLabel.pack(anchor=SW,fill=BOTH,expand=True)
        self.entry_Vmin=Entry(master=self.OptionsFrame,textvariable=self.vMinString)
        self.entry_Vmin.pack(anchor=SE,fill=BOTH,expand=True)

        self.VmaxLabel= Label(master=self.OptionsFrame,text="Vmax(V)",background="light goldenrod")
        self.VmaxLabel.pack(anchor=SW,fill=BOTH,expand=True)
        self.entry_Vmax=Entry(master=self.OptionsFrame,textvariable=self.vMaxString)
        self.entry_Vmax.pack(anchor=SE,fill=BOTH,expand=True)

        self.RangoDText= Message(master=self.OptionsFrame, text="Rango dinamico(dB)="+self.RDString.get(),textvariable=self.RDString)
        self.RangoDText.pack(side="top",fill=BOTH,expand=True)

    def PlaceTransferFunctionGraph(self):
        self.fzString= StringVar()
        self.fpString= StringVar()
        self.QzString= StringVar()
        self.QpString= StringVar()
        self.G0String= StringVar()

        self.TransferGraphsFrame= LabelFrame(master=self.root, text="Ganancias",background="goldenrod")
        self.TransferGraphsFrame.pack(side="right",fill=BOTH,expand=True)

        #Seccion con la etapa seleccionada
        self.StageGraphFrame= LabelFrame(master=self.TransferGraphsFrame, text="Etapa seleccionada",background="goldenrod")
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
        self.CurrentStageCanvas.draw()
        #Parametros de interes de la etapa seleccionada
        self.StageParamsFrame= LabelFrame(self.StageGraphFrame,text="Parametros de interes",background="goldenrod")
        self.StageParamsFrame.pack(side="top",fill=BOTH,expand=True)
        #fz
        self.TransfwzLabel= Label(master=self.StageParamsFrame,text="fz(Hz)",background="light goldenrod")
        self.TransfwzLabel.pack(fill=BOTH,expand=True)
        self.entry_Transfwz=Entry(master=self.StageParamsFrame,textvariable=self.fzString)
        self.entry_Transfwz.pack(anchor=NE,fill=BOTH,expand=True)
        #fp
        self.TransfwpLabel= Label(master=self.StageParamsFrame,text="fp(Hz)",background="light goldenrod")
        self.TransfwpLabel.pack(fill=BOTH,expand=True)
        self.entry_Transfwz=Entry(master=self.StageParamsFrame,textvariable=self.fpString)
        self.entry_Transfwz.pack(anchor=NE,fill=BOTH,expand=True)
        #H(0)
        self.G0Label= Label(master=self.StageParamsFrame,text="H(0)(dB)",background="light goldenrod")
        self.G0Label.pack(fill=BOTH,expand=True)
        self.entry_G0=Entry(master=self.StageParamsFrame,textvariable=self.G0String)
        self.entry_G0.pack(anchor=NE,fill=BOTH,expand=True)
        #Qp
        self.QpLabel= Label(master=self.StageParamsFrame,text="Qp",background="light goldenrod")
        self.QpLabel.pack(fill=BOTH,expand=True)
        self.entry_Qp=Entry(master=self.StageParamsFrame,textvariable=self.QpString)
        self.entry_Qp.pack(anchor=NE,fill=BOTH,expand=True)
        #Qz
        self.QzLabel= Label(master=self.StageParamsFrame,text="Qz",background="light goldenrod")
        self.QzLabel.pack(fill=BOTH,expand=True)
        self.entry_Qz=Entry(master=self.StageParamsFrame,textvariable=self.QzString)
        self.entry_Qz.pack(anchor=NE,fill=BOTH,expand=True)

        #Seccion con la ganancia de todas las etapas en cascada
        self.CascadeGraphFrame= LabelFrame(master=self.TransferGraphsFrame, text="Ganancia total(cascada)",background="goldenrod")
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
        self.TransfTotalCanvas.draw()

    def PlaceStagesMenu(self):
        self.StagesMenuFrame= LabelFrame(self.root, text="Etapas",background="goldenrod")
        self.StagesMenuFrame.pack(side="bottom",fill=BOTH,expand=True)
        self.etapa1button= Button(master=self.StagesMenuFrame,text="Etapa1",background="light goldenrod")
        self.etapa1button.pack(side="left",fill=BOTH,expand=True)
    #Callbacks de la segunda etapa
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