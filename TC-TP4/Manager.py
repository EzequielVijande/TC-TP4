
import UserData
import ApGUI as ap
import aproximacionesFuncs as a
import StagesCalculator as St
import numpy as np
import math
#Estados
EXIT=0
ETAPA1=1
ETAPA2=2


class Manager(object):
    """Clase que se ocupa de vincular la logica con la GUI"""
    def __init__(self, data,GUI):
        self.Aproximator= a.AproxAnalysis()
        self.data=data
        self.GUI=GUI
        self.estado= ETAPA1

    #Getters
    def getState(self):
        return self.estado

    def Dispatch(self, ev):
        if(self.estado == ETAPA1):
            if(ev == ap.NO_EV):
                self.OnNoEv()
            elif(ev == ap.GRAPH_EV):
                self.OnGraphEv()
            elif(ev == ap.QUIT_EV):
                self.OnQuitEv()
            elif(ev == ap.SAVE_EV):
                self.OnSaveEv()
            elif(ev == ap.LOAD_EV):
                self.OnLoadEv()
            elif(ev == ap.NEXT_EV):
                self.OnNextEv()
            elif(ev == ap.CHANGE_GRAPH_EV):
                self.OnChangeGraphEv()
            elif(ev == ap.PUT_TEMPLATE_EV):
                self.OnPutTemplate()
            else:
                self.Error()


        elif(self.estado == ETAPA2):
            if(ev == ap.PREV_EV):
                self.OnPrevEv()
            elif(ev == ap.SAVE_EV):
                self.OnSave2Ev()
            elif(ev == ap.LOAD_EV):
                self.OnLoad2Ev()
            elif(ev == ap.QUIT_EV):
                self.OnQuitEv()
            elif(ev == ap.CREATE_STAGE_EV):
                self.OnCreateStageEv()
            elif(ev == ap.DELETE_STAGE_EV):
                self.OnDeleteStageEv()
            elif(ev == ap.SELECT_STAGE_EV):
                self.OnSelectStageEv()
            elif(ev == ap.CHANGED_V_LIMITS_EV):
                self.OnChangedV()
            elif(ev == ap.CHANGED_STAGE_PARAMS):
                self.OnChangedStageParams()
            elif(ev == ap.RESET):
                self.OnResetEv()
            elif(ev == ap.EXPORT):
                self.OnExportEv()

        self.GUI.EventSolved()    #Settea que ya no hay evento a resolver

    #Funciones que manejan eventos de la primera etapa
    def OnNoEv(self):
        return

    def OnGraphEv(self):
        result_str= self.ValidateInputs()
        if(result_str!="Ok"):
            self.GUI.DisplayError(result_str)
        else:
          self.GUI.Graph_enable=True
          self.ShowGraph()

    def OnQuitEv(self):
        self.GUI.CloseGUI()
        self.estado=EXIT
        return

    def OnSaveEv(self):
        result= self.GUI.CreateFileEntryWindow()
        if(result=="Ok"):
            if(self.GUI.Graph_enable):
                self.SaveData(self.GUI.SaveFileName.get())
            else:
                self.GUI.ShowMessage("No information to save")

    def OnLoadEv(self):
        result= self.GUI.OpenLoadWindow()
        if(result =="Ok"):
            self.LoadData(self.GUI.LoadFileName.get())
            self.GUI.ShowData(self.data)

    def OnNextEv(self):
        if(self.GUI.Graph_enable):
            self.estado=ETAPA2
            self.GUI.Change_to_stage2()
            self.SeparateStages()
        else:
             self.GUI.ShowMessage("Es necesario especificar una plantilla valida primero")

    def OnChangeGraphEv(self):
        self.DisplaySelectedGraph()
        WantsTempl= self.GUI.PutTemplate.get()
        sel= self.GUI.SelectedGraph.get()
        if(WantsTempl):
           self.GUI.placeTemplate(self.data.Ap,self.data.As,(self.data.wp)/(2*math.pi),self.data.ws/(2*math.pi),self.data.wo/(2*math.pi)
                                  ,self.data.Q,self.data.wpMinus/(2*math.pi),self.data.wpPlus/(2*math.pi),self.data.wsMinus/(2*math.pi)
                                  ,self.data.wsPlus/(2*math.pi),self.data.type_of_filter,self.data.Aproximation,self.data.t0,
                                  self.data.wrg/(2*math.pi),self.data.Y)
        elif(self.GUI.TemplateOn):
            self.GUI.destroyTemplate()

    def OnPutTemplate(self):
        WantsTempl= self.GUI.PutTemplate.get()
        sel_graph= self.GUI.SelectedGraph.get()
        if(WantsTempl):
            result_str= self.ValidateInputs()
            if(result_str!="Ok"):
                self.GUI.TemplateButton.deselect()
                self.GUI.DisplayError(result_str)
            else:
                self.SetUserData()
                self.GUI.placeTemplate(self.data.Ap,self.data.As,(self.data.wp)/(2*math.pi),self.data.ws/(2*math.pi),self.data.wo/(2*math.pi)
                                  ,self.data.Q,self.data.wpMinus/(2*math.pi),self.data.wpPlus/(2*math.pi),self.data.wsMinus/(2*math.pi)
                                  ,self.data.wsPlus/(2*math.pi),self.data.type_of_filter,self.data.Aproximation,self.data.t0,
                                  self.data.wrg/(2*math.pi),self.data.Y)
        elif(self.GUI.TemplateOn):
             self.GUI.destroyTemplate()
        
    def Error(self):
        return
    #Funciones auxiliares
    def ShowGraph(self):
        sel= self.GUI.SelectedGraph.get()
        filt= self.GUI.filter.get()
        WantsTempl= self.GUI.PutTemplate.get()
        self.SetUserData()
        
        self.CalculateGraphs()
        #Actualizo todas las graficas
        att=-self.data.mag
        self.GUI.Axes_Stage1.cla()
        self.GUI.plotAtte((self.data.f),att)
        self.GUI.plotAtteNorm(self.data.f,self.data.mag)
        self.GUI.plotPhase(self.data.f,self.data.phase)
        #self.GUI.plotQ(self.data.qs)
        self.GUI.plotStep(self.data.StepTime,self.data.StepResp)
        self.GUI.plotImpulse(self.data.ImpTime,self.data.ImpResp)
        self.GUI.plotZeros(self.data.zeroes_real,self.data.zeroes_imag,self.data.poles_real,self.data.poles_imag)
        self.GUI.PlotGroupDelay(self.data.f,self.data.gd)
        
        self.DisplaySelectedGraph()
        if(WantsTempl):
           self.GUI.placeTemplate(self.data.Ap,self.data.As,(self.data.wp)/(2*math.pi),self.data.ws/(2*math.pi),self.data.wo/(2*math.pi)
                                  ,self.data.Q,self.data.wpMinus/(2*math.pi),self.data.wpPlus/(2*math.pi),self.data.wsMinus/(2*math.pi)
                                  ,self.data.wsPlus/(2*math.pi),filt,self.GUI.selected_aprox.get(),self.data.t0,
                                  self.data.wrg/(2*math.pi),self.data.Y)
        elif(self.GUI.TemplateOn):
            self.GUI.destroyTemplate()

    def SetUserData(self):
        filt= self.GUI.filter.get()
        self.data.setFilter(filt)
        aprox= self.GUI.selected_aprox.get()
        self.data.NormRange= (self.GUI.SlideNorm.get())/100
        self.data.Aproximation= aprox
        if(filt != ap.GR):
            As= float(self.GUI.AsString.get())
            Ap= float(self.GUI.ApString.get())

            self.data.setAp(Ap)
            self.data.setAs(As)

            if(filt==ap.LP or filt==ap.HP):
                ws= (float(self.GUI.wsString.get()))*2*(math.pi)
                wp= float(self.GUI.wpString.get())*2*(math.pi)
                self.data.setws(ws)
                self.data.setwp(wp)
            elif(filt==ap.BP or filt==ap.BR):
                wo= float(self.GUI.w0String.get())*2*(math.pi)
                Q= float(self.GUI.qString.get())
                Δwp= float(self.GUI.ΔwpString.get())*2*(math.pi)
                Δws= float(self.GUI.ΔwsString.get())*2*(math.pi)

                (wpMinus,wpPlus,wsMinus,wsPlus)=  self.calculate_w(wo,Δwp,Δws)
                self.data.setwpMinus(wpMinus) #setteo userData
                self.data.setwpPlus(wpPlus)
                self.data.setwsMinus(wsMinus)
                self.data.setwsPlus(wsPlus)
                self.data.setwo(wo)
                self.data.setQ(Q)

        elif(filt == ap.GR):
            self.data.t0 = float(self.GUI.τ0String.get())
            self.data.wrg = float(self.GUI.wrgString.get()) *2*(math.pi)
            self.data.Y = float(self.GUI.YString.get())

    def calculate_w(self,wo,Δwp,Δws):
        wpMinus=(-Δwp+(( (Δwp**2)+(4*(wo**2)))**0.5))/2
        wpPlus= wpMinus+Δwp
        wsMinus=(-Δws+(( (Δws**2)+(4*(wo**2)))**0.5))/2
        wsPlus= wsMinus+Δws
        return (wpMinus,wpPlus,wsMinus,wsPlus)




    def ValidateInputs(self):
        fil=self.GUI.filter.get()
        #valido los opcionales
        
        if(self.GUI.SelectedCheck.get() == ap.N_CHECK):
            N=self.GUI.nString.get()
            nSTR= self.IsValidNumber(N,"N")
            if(nSTR!="Ok"):
                return nSTR
            N_float=float(N)
            if(N_float>20):
                return "El valor de N debe ser menor a 20"
        elif(self.GUI.SelectedCheck.get() == ap.N_RANGE_CHECK):
            Nmax=self.GUI.nMaxString.get()
            nmaxSTR= self.IsValidNumber(Nmax,"Nmax")
            if(nmaxSTR!="Ok"):
                return nmaxSTR
            Nmin=self.GUI.nMinString.get()
            nminSTR= self.IsValidNumber(Nmin,"Nmin")
            if(nminSTR!="Ok"):
                return nminSTR
            nminfloat= float(Nmin)
            nmaxfloat= float(Nmax)
            if(nmaxfloat<=nminfloat):
                return "Nmin debe ser menor que Nmax"

        if(fil!= ap.GR):
            As= self.GUI.AsString.get()
            Ap= self.GUI.ApString.get()

            ApSTR= self.IsValidNumber(Ap,"Ap")
            if(ApSTR!="Ok"):
                return ApSTR

            AsSTR = self.IsValidNumber(As,"As")
            if(AsSTR!="Ok"):
                return AsSTR
            if((float(Ap))>=(float(As))):
                return "Ap debe ser menor a As"

            if( (fil==ap.LP) or (fil==ap.HP) ): #No es necesario validar especificaciones de rechaza banda ni de pasa banda
                wp= self.GUI.wpString.get()
                ws= self.GUI.wsString.get()

                wpSTR= self.IsValidNumber(wp,"wp") #Valido wp
                if(wpSTR!="Ok"):
                    return wpSTR

                wsSTR= self.IsValidNumber(ws,"ws") #Valido ws
                if(wsSTR!="Ok"):
                    return wsSTR
            
                elif(fil==ap.LP): #Si es un LP el wp debe ser menor al ws
                    if(float(ws)<=float(wp)):
                        return "wp debe ser menor que ws"
                else: #Si es un HP el wp debe ser mayor al ws
                    if(float(ws)>=float(wp)):
                        return "ws debe ser menor que wp"

            elif( (fil==ap.BP) or (fil==ap.BR)):
                Δwp= self.GUI.ΔwpString.get()
                Δws= self.GUI.ΔwsString.get()
                wo= self.GUI.w0String.get()
                Q=self.GUI.qString.get()
            
                ΔwpSTR= self.IsValidNumber(Δwp,"Δwp") #valido Δwp
                if(ΔwpSTR != "Ok"):
                    return ΔwpSTR

                ΔwsSTR= self.IsValidNumber(Δws,"Δws") #valido Δws
                if(ΔwsSTR != "Ok"):
                    return ΔwsSTR

                woSTR= self.IsValidNumber(wo,"wo") #valido wo
                if(woSTR != "Ok"):
                    return woSTR

                QSTR= self.IsValidNumber(Q,"Q") #valido Q
                if(QSTR != "Ok"):
                    return QSTR


                if(fil==ap.BP):
                    if( float(Δwp)>=float(Δws)):
                        return "Δwp debe ser menor que Δws para un filtro pasa banda"
                else:
                    if( float(Δwp)<=float(Δws)):
                        return "Δwp debe ser mayor que Δws para un filtro rechaza banda"

        else:
            t0=self.GUI.τ0String.get()
            wrg=self.GUI.wrgString.get()
            Y=self.GUI.YString.get()

            t0String= self.IsValidNumber(t0,"t(0)")
            if(t0String != "Ok"):
                return t0String
            wrgString= self.IsValidNumber(wrg,"wrg")
            if(wrgString != "Ok"):
                return wrgString
            YString= self.IsValidNumber(Y,"Y")
            if(YString != "Ok"):
                return YString
            elif(float(Y)>1):
                return "Y debe ser un numero entre 0 y 1"
        return "Ok"



    def isfloat(self,value):
      try:
        float(value)
        return True
      except ValueError:
        return False

    def IsValidNumber(self,arg, argstring):
        if( self.isfloat(arg)): #valido el argumento
            arg_f=float(arg)
            if(arg_f<=0):
                return ( argstring+" debe ser positivo")
            elif(arg_f==float("inf")):
                return (argstring+" debe tener un valor finito")

        else:
            return ("Error de sintaxis en "+argstring)

        return "Ok" #El numero parece ser valido

    def DisplaySelectedGraph(self):
        if(self.GUI.Graph_enable):
            Xmin,Xmax,Ymin,Ymax= self.ObtainScaleLimits()
            self.GUI.DisplayGraph(Xmin,Xmax,Ymin,Ymax,self.data.qs)

    def ObtainScaleLimits(self):
        filt=self.data.GetFilter()
        selected= self.GUI.SelectedGraph.get()
        Δfs= (self.data.wsPlus -self.data.wsMinus)/(2*math.pi)
        Δfp= (self.data.wpPlus -self.data.wpMinus)/(2*math.pi)
        if(selected==ap.ATT or selected==ap.ATT_N):

            if(filt == ap.LP):
                if(selected != ap.ATT_N):
                    xleft= (self.data.wp/(2*math.pi))/100
                    xright= (self.data.ws/(2*math.pi))*100
                    ybot=0
                    ytop=(self.data.As)*1.5
                    return xleft, xright,ybot,ytop
                else:
                    return 0, ((self.data.ws/(2*math.pi))/(self.data.wp/(2*math.pi))),0,((self.data.As)*1.5)

            elif(filt == ap.HP):
                if(selected != ap.ATT_N):
                    xleft= (self.data.ws/(2*math.pi))/100
                    xright= (self.data.wp/(2*math.pi))*100
                    ybot=0
                    ytop=(self.data.As)*1.5
                    return xleft, xright,ybot,ytop
                else:
                    return 0, ((self.data.wp/(2*math.pi))/(self.data.ws/(2*math.pi))),0,((self.data.As)*1.5)
            elif(filt == ap.BP):
                if(selected != ap.ATT_N):
                    xleft= (self.data.wo/(2*math.pi))-(2*Δfs)
                    xright= (self.data.wo/(2*math.pi))+(2*Δfs)
                    ybot=0
                    ytop=(self.data.As)*1.5
                    return xleft, xright,ybot,ytop
                else:
                    return 0, (Δfs/Δfp),0,((self.data.As)*1.5)

            elif(filt == ap.BR):
                if(selected != ap.ATT_N):
                    xleft= (self.data.wo/(2*math.pi))-(2*Δfp)
                    xright= (self.data.wo/(2*math.pi))+(2*Δfp)
                    ybot=0
                    ytop=(self.data.As)*1.5
                    return xleft, xright,ybot,ytop
                else:
                    return 0, (Δfp/Δfs),0,((self.data.As)*1.5)
            elif(filt == ap.GR):
                if(selected == ap.ATT):
                    xmin=0
                    xmax=(self.data.wrg)*10
                    ymin=0
                    ymax=60
                    return xmin,xmax,ymin,ymax
                else: 
                    xmin=0
                    xmax=(self.data.wrg)
                    ymin=0
                    ymax=60
                    return xmin,xmax,ymin,ymax
        elif(selected == ap.RETARDO):
            y_max = self.data.gd.max()
            y_min = self.data.gd.min()
            if(filt == ap.LP):
                    xleft= (self.data.wp/(2*math.pi))/100
                    xright= (self.data.ws/(2*math.pi))*100
                    ybot= y_min
                    ytop=(y_max)
                    return xleft, xright,ybot,ytop

            elif(filt == ap.HP):
                    xleft= (self.data.ws/(2*math.pi))/100
                    xright= (self.data.wp/(2*math.pi))*100
                    ybot=y_min
                    ytop=(y_max)*1.1
                    return xleft, xright,ybot,ytop

            elif(filt == ap.BP):
                    xleft= (self.data.wo/(2*math.pi))-(2*Δfs)
                    xright= (self.data.wo/(2*math.pi))+(2*Δfs)
                    ybot=y_min
                    ytop=(y_max)*1.1
                    return xleft, xright,ybot,ytop

            elif(filt == ap.BR):
                    xleft= (self.data.wo/(2*math.pi))-(2*Δfp)
                    xright= (self.data.wo/(2*math.pi))+(2*Δfp)
                    ybot=y_min
                    ytop=(y_max)*1.1
                    return xleft, xright,ybot,ytop
            elif(filt == ap.GR):
                    xleft= 0
                    xright= self.data.wrg *10
                    ymin= y_min
                    ymax= y_max
                    return xleft,xright,ymin,ymax

        elif(selected ==ap.FASE): #Limites de escala para el grafico de fase
            ymax= self.data.GetPhaseMax()
            ymin= self.data.GetPhaseMin()
            if(filt == ap.LP):
                    xleft= (self.data.wp/(2*math.pi))/100
                    xright= (self.data.ws/(2*math.pi))*100
                    ybot=0
                    ybot=ymin
                    ytop=ymax
                    return xleft, xright,ybot,ytop

            elif(filt == ap.HP):
                    xleft= (self.data.ws/(2*math.pi))/100
                    xright= (self.data.wp/(2*math.pi))*100
                    ybot=ymin
                    ytop=ymax
                    return xleft, xright,ybot,ytop
            elif(filt == ap.BP):
                    xleft= (self.data.wo/(2*math.pi))-(2*Δfs)
                    xright= (self.data.wo/(2*math.pi))+(2*Δfs)
                    ybot=ymin
                    ytop=ymax
                    return xleft, xright,ybot,ytop

            elif(filt == ap.BR):
                    xleft= (self.data.wo/(2*math.pi))-(2*Δfp)
                    xright= (self.data.wo/(2*math.pi))+(2*Δfp)
                    ybot=ymin
                    ytop=ymax
                    return xleft, xright,ybot,ytop
            elif(filt == ap.GR):
                xmin=0
                xmax=(self.data.wrg)*10
                return xmin,xmax,ymin,ymax
        elif(selected == ap.STEP):
            ymax=self.data.StepResp.max()
            ymin=self.data.StepResp.min()
            xmax=self.data.StepTime.max()
            xmin=self.data.StepTime.min()
            return xmin,xmax,ymin,ymax
        elif(selected == ap.IMPULSE):
            ymax=self.data.ImpResp.max()
            ymin=self.data.ImpResp.min()
            xmax=self.data.ImpTime.max()
            xmin=self.data.ImpTime.min()
            return xmin,xmax,ymin,ymax
        elif(selected == ap.CEROS):
            #Limites de y
            if(self.data.zeroes_imag.size != 0):
                if(self.data.zeroes_imag.max()>=self.data.poles_imag.max()):
                    ymax=1.1*(self.data.zeroes_imag.max())
                else:
                    ymax=1.1*(self.data.poles_imag.max())
                if(self.data.zeroes_imag.min()>=self.data.poles_imag.min()):
                    ymin=self.data.poles_imag.min()
                else:
                    ymin=self.data.zeroes_imag.min()
            else:
                ymax=1.1*(self.data.poles_imag.max())
                ymin=self.data.poles_imag.min()
            #Limites de x
            if(self.data.zeroes_real.size != 0):
                if(self.data.zeroes_real.max()>=self.data.poles_real.max()):
                    xmax= 1.1*(self.data.zeroes_real.max())
                else:
                    xmax= 1.1*(self.data.poles_real.max())
                #Valores minimos
           
                if(self.data.zeroes_real.min()>=self.data.poles_real.min()):
                    xmin= (self.data.poles_real.min())*1.1
                else:
                    xmin= (self.data.zeroes_real.min())*1.1
            else:
                xmax= (self.data.poles_real.max())
                xmin= self.data.poles_real.min() *1.1

            return xmin,xmax,ymin,ymax
        else:
            xmin=0
            xmax=(self.data.qs.size)+1
            ymin=0
            ymax=self.data.qs.max()
            return xmin,xmax,ymin,ymax



    def CalculateGraphs(self):
        check_option= self.GUI.SelectedCheck.get()
        mode="normal"
        if(check_option == ap.NORMAL_CHECK):
            mode="normal"
        elif(check_option == ap.N_CHECK):
            n=float(self.GUI.nString.get())
            self.Aproximator.setnFixed(n)
            mode="fixed"
        elif(check_option == ap.N_RANGE_CHECK):
            nmax=float(self.GUI.nMaxString.get())
            nmin=float(self.GUI.nMinString.get())
            mode="range"
            self.Aproximator.setnRange(nmin,nmax)

        As=self.data.As
        Ap=self.data.Ap
        wp=self.data.wp
        ws=self.data.ws
        wpMinus=self.data.wpMinus
        wpPlus=self.data.wpPlus
        wsMinus=self.data.wsMinus
        wsPlus=self.data.wsPlus
        wo=self.data.wo
        type= self.GetTypeString()
        tauZero = self.data.t0
        wrg = self.data.wrg
        gamma = self.data.Y
        a=self.data.NormRange

        self.Aproximator.SetParams(As,Ap,wp,ws,wpMinus,wpPlus,wsMinus,wsPlus,type,a,tauZero,wrg,gamma)

        aprox= self.data.GetAprox()
        if(aprox == ap.APROXIMACIONES[0]):
            self.Aproximator.butterworthAnalysis(mode)
        elif(aprox == ap.APROXIMACIONES[1]):
            self.Aproximator.chebyshevAnalysis(mode)
        elif(aprox == ap.APROXIMACIONES[2]):
            self.Aproximator.chebyshevInverseAnalysis(mode)
        elif(aprox == ap.APROXIMACIONES[3]):
            self.Aproximator.besselAnalysis(mode)
        elif(aprox == ap.APROXIMACIONES[4]):
            self.Aproximator.gaussAnalysis(mode)
        finalFunc = self.Aproximator.getFunction()
        #Datos para la atenuacion y la fase
        w = np.logspace(-2, 10, 50000, endpoint=True)
        w, mag, phase = self.Aproximator.CalcBodePlot(w,finalFunc)
        self.data.setfVector(w/(2*math.pi))
        self.data.setMag(mag)
        self.data.setPhase(phase)
        #Respuesta al impulso
        #t_imp,h=(self.Aproximator.getFunction()).impulse(N=8000)
        #h=h.real
        #self.data.setImpData(t_imp,h)
        #Respuesta al escalon
        #t_step,u=(self.Aproximator.getFunction()).step(N=8000)
        #u=u.real
        #self.data.setStepData(t_step,u)
        #Polos y ceros
        zeros = finalFunc.zeros
        poles = finalFunc.poles
        self.data.SetZeroesAndPoles(zeros,poles)
        #Grafica de qs
        parte_real= poles.real
        parte_imag= poles.imag
        modulo= abs(poles)
        qs= -(modulo/(2*parte_real))
        qs= np.asarray(list(set(qs)))
        self.data.SetQValues(qs) #Paso a lista y de nuevo a arreglo para sacar los elementos repetidos
        #Actualizo el n
        n=  (finalFunc.den.size)-1
        auxString= "N = "
        self.GUI.NString_Graph.set(auxString+str(n))
        #calculo del retardo de grupo
        w, gd = self.Aproximator.CalcGroupDelay(w,finalFunc)
        self.data.SetGroupDelay(gd)

    def GetTypeString(self):
        filt=self.data.GetFilter()
        if(filt==ap.LP):
            return "LP"
        elif(filt==ap.HP):
            return "HP"
        elif(filt==ap.BP):
            return "BP"
        elif(filt==ap.BR):
            return "BR"
        elif(filt==ap.GR):
            return "GR"
    #Funcion de Save y Load
    def SaveData(self,name):
        file_name= name+".txt"
        f= open(file_name,"w+")
        f.write("Filtro: %d\n" % (self.data.type_of_filter))
        f.write("Aproximacion: %s\n" % (self.data.Aproximation))
        f.write("Ap: %d\n" % (self.data.Ap))
        f.write("As: %d\n" % (self.data.As))
        f.write("wp: %d\n" % (self.data.wp))
        f.write("ws: %d\n" % (self.data.ws))
        f.write("wo: %d\n" % (self.data.wo))
        f.write("wp_minus: %d\n" % (self.data.wpMinus))
        f.write("wp_plus: %d\n" % (self.data.wpPlus))
        f.write("ws_minus: %d\n" % (self.data.wsMinus))
        f.write("ws_plus: %d\n" % (self.data.wsPlus))
        f.write("Qmax: %d\n" % (self.data.Q))
        f.write("RangNorm: %d\n" % (self.data.NormRange))
        f.write("t0: %d\n" % (self.data.t0))
        f.write("wrg: %d\n" % (self.data.wrg))
        f.write("t0: %d\n" % (self.data.Y))
    def LoadData(self,name):
        file_name= name+".txt"
        file = open(file_name,'r')
        lines= file.readlines()
        self.data.type_of_filter=float((lines[0].split(' ', 1))[1])
        self.data.Aproximation=(lines[1].split(' ', 1))[1]
        self.data.Aproximation= self.data.Aproximation[:-1]
        self.data.Ap=float((lines[2].split(' ', 1))[1])
        self.data.As=float((lines[3].split(' ', 1))[1])
        self.data.wp=float((lines[4].split(' ', 1))[1])
        self.data.ws=float((lines[5].split(' ', 1))[1])
        self.data.wo=float((lines[6].split(' ', 1))[1])
        self.data.wpMinus=float((lines[7].split(' ', 1))[1])
        self.data.wpPlus=float((lines[8].split(' ', 1))[1])
        self.data.wsMinus=float((lines[9].split(' ', 1))[1])
        self.data.wsPlus=float((lines[10].split(' ', 1))[1])
        self.data.Q=float((lines[11].split(' ', 1))[1])
        self.data.NormRange=float((lines[12].split(' ', 1))[1])
        self.data.t0=float((lines[13].split(' ', 1))[1])
        self.data.wrg=float((lines[14].split(' ', 1))[1])
        self.data.Y=float((lines[15].split(' ', 1))[1])

    def SeparateStages(self):
        self.CascadeManager = St.StagesCalculator(self.Aproximator.getFunction())


    #Funciones que manejan eventos de la segunda etapa

    def OnPrevEv(self):
        if(self.GUI.ShowPrevMessage()):
            self.GUI.Change_to_stage1()
            self.estado=ETAPA1
    def OnSave2Ev(self):
        return
    def OnLoad2Ev(self):
        return