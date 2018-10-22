
import UserData
import ApGUI as ap
import aproximacionesFuncs as a
import numpy as np

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
        return

    def OnLoadEv(self):
        return

    def OnNextEv(self):
        #self.IsNextValid()
        self.estado=ETAPA2
        self.GUI.Change_to_stage2()

    def OnChangeGraphEv(self):
        self.DisplaySelectedGraph()
        WantsTempl= self.GUI.PutTemplate.get()
        sel= self.GUI.SelectedGraph.get()
        if(WantsTempl and sel== ap.ATT):
           self.GUI.placeTemplate(self.data.Ap,self.data.As,self.data.wp,self.data.ws,self.data.wo,self.data.Q,
                                      self.data.wpMinus,self.data.wpPlus,self.data.wsMinus,self.data.wsPlus)
        elif(self.GUI.TemplateOn):
            self.GUI.destroyTemplate()

    def OnPutTemplate(self):
        WantsTempl= self.GUI.PutTemplate.get()
        sel_graph= self.GUI.SelectedGraph.get()
        if(sel_graph==ap.ATT):
            
            if(WantsTempl):
                result_str= self.ValidateInputs()
                if(result_str!="Ok"):
                    self.GUI.TemplateButton.deselect()
                    self.GUI.DisplayError(result_str)
                else:
                    self.SetUserData()
                    self.GUI.placeTemplate(self.data.Ap,self.data.As,self.data.wp,self.data.ws,self.data.wo,self.data.Q,
                                            self.data.wpMinus,self.data.wpPlus,self.data.wsMinus,self.data.wsPlus)
            else:
                self.GUI.destroyTemplate()
        
    def Error(self):
        return
    #Funciones auxiliares
    def ShowGraph(self):
        sel= self.GUI.SelectedGraph.get()
        WantsTempl= self.GUI.PutTemplate.get()
        self.SetUserData()
        
        self.CalculateGraphs()
        #Actualizo todas las graficas
        att=-self.data.mag
        self.GUI.Axes_Stage1.cla()
        self.GUI.plotAtte((self.data.w),att)
        self.GUI.plotAtteNorm(self.data.w,self.data.mag)
        self.GUI.plotPhase(self.data.w,self.data.phase)
        #self.GUI.plotQ(Y)
        self.GUI.plotStep(self.data.StepTime,self.data.StepResp)
        self.GUI.plotImpulse(self.data.ImpTime,self.data.ImpResp)
        self.GUI.plotZeros(self.data.w,self.data.mag)
        self.GUI.PlotGroupDelay(self.data.w,self.data.mag)
        
        self.DisplaySelectedGraph()
        if(WantsTempl and sel== ap.ATT):
           self.GUI.placeTemplate(self.data.Ap,self.data.As,self.data.wp,self.data.ws,self.data.wo,self.data.Q,
                                      self.data.wpMinus,self.data.wpPlus,self.data.wsMinus,self.data.wsPlus)
        elif(self.GUI.TemplateOn):
            self.GUI.destroyTemplate()

    def SetUserData(self):
        As= float(self.GUI.AsString.get())
        Ap= float(self.GUI.ApString.get())

        self.data.setAp(Ap)
        self.data.setAs(As)
        filt= self.GUI.filter.get()
        aprox= self.GUI.selected_aprox.get()
        self.data.setFilter(filt)
        self.data.NormRange= (self.GUI.SlideNorm.get())/100
        self.data.Aproximation= aprox

        if(filt==ap.LP or filt==ap.HP):
            ws= float(self.GUI.wsString.get())
            wp= float(self.GUI.wpString.get())
            self.data.setws(ws)
            self.data.setwp(wp)
        elif(filt==ap.BP or filt==ap.BR):
            wo= float(self.GUI.w0String.get())
            Q= float(self.GUI.qString.get())
            Δwp= float(self.GUI.ΔwpString.get())
            Δws= float(self.GUI.ΔwsString.get())

            (wpMinus,wpPlus,wsMinus,wsPlus)=  self.calculate_w(wo,Δwp,Δws)
            self.data.setwpMinus(wpMinus) #setteo userData
            self.data.setwpPlus(wpPlus)
            self.data.setwsMinus(wsMinus)
            self.data.setwsPlus(wsPlus)
            self.data.setwo(wo)
            self.data.setQ(Q)

    def calculate_w(self,wo,Δwp,Δws):
        wpMinus=(-Δwp+(( (Δwp**2)+(4*(wo**2)))**0.5))/2
        wpPlus= wpMinus+Δwp
        wsMinus=(-Δws+(( (Δws**2)+(4*(wo**2)))**0.5))/2
        wsPlus= wsMinus+Δws
        return (wpMinus,wpPlus,wsMinus,wsPlus)




    def ValidateInputs(self):
        fil=self.GUI.filter.get()
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
                    return ΔwoSTR

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
            self.GUI.DisplayGraph(Xmin,Xmax,Ymin,Ymax)

    def ObtainScaleLimits(self):
        filt=self.data.GetFilter()
        selected= self.GUI.SelectedGraph.get()
        if(selected==ap.ATT or selected==ap.ATT_N):

            if(filt == ap.LP):
                if(selected != ap.ATT_N):
                    xleft= (self.data.wp)/100
                    xright= (self.data.ws)*100
                    ybot=0
                    ytop=(self.data.As)*1.5
                    return xleft, xright,ybot,ytop
                else:
                    return 0, ((self.data.ws)/(self.data.wp)),0,((self.data.As)*1.5)

            elif(filt == ap.HP):
                if(selected != ap.ATT_N):
                    xleft= (self.data.ws)/100
                    xright= (self.data.wp)*100
                    ybot=0
                    ytop=(self.data.As)*1.5
                    return xleft, xright,ybot,ytop
                else:
                    return 0, ((self.data.wp)/(self.data.ws)),0,((self.data.As)*1.5)
            elif(filt == ap.BP):
                if(selected != ap.ATT_N):
                    xleft= (self.data.wo)-(2*(float(self.GUI.entry_Δws.get())))
                    xright= (self.data.wo)+(20*(float(self.GUI.entry_Δws.get())))
                    ybot=0
                    ytop=(self.data.As)*1.5
                    return xleft, xright,ybot,ytop
                else:
                    return 0, ((float(self.GUI.entry_Δws.get()))/(float(self.GUI.entry_Δwp.get()))),0,((self.data.As)*1.5)

            elif(filt == ap.BR):
                if(selected != ap.ATT_N):
                    xleft= (self.data.wo)-(2*(float(self.GUI.entry_Δwp.get())))
                    xright= (self.data.wo)+(20*(float(self.GUI.entry_Δwp.get())))
                    ybot=0
                    ytop=(self.data.As)*1.5
                    return xleft, xright,ybot,ytop
                else:
                    return 0, (float(self.GUI.entry_Δwp.get()))/float((self.GUI.entry_Δwp.get())),0,((self.data.As)*1.5)
        elif(selected ==ap.FASE): #Limites de escala para el grafico de fase
            ymax= self.data.GetPhaseMax()
            ymin= self.data.GetPhaseMin()
            if(filt == ap.LP):
                    xleft= (self.data.wp)/100
                    xright= (self.data.ws)*100
                    ybot=0
                    ybot=ymin
                    ytop=ymax
                    return xleft, xright,ybot,ytop

            elif(filt == ap.HP):
                    xleft= (self.data.ws)/100
                    xright= (self.data.wp)*100
                    ybot=ymin
                    ytop=ymax
                    return xleft, xright,ybot,ytop
            elif(filt == ap.BP):
                    xleft= (self.data.wo)-(2*(float(self.GUI.entry_Δws.get())))
                    xright= (self.data.wo)+(20*(float(self.GUI.entry_Δws.get())))
                    ybot=ymin
                    ytop=ymax
                    return xleft, xright,ybot,ytop

            elif(filt == ap.BR):
                    xleft= (self.data.wo)-(2*(float(self.GUI.entry_Δwp.get())))
                    xright= (self.data.wo)+(20*(float(self.GUI.entry_Δwp.get())))
                    ybot=ymin
                    ytop=ymax
                    return xleft, xright,ybot,ytop
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


    def CalculateGraphs(self):
        As=self.data.As
        Ap=self.data.Ap
        wp=self.data.wp
        ws=self.data.ws
        wpMinus=self.data.wpMinus
        wpPlus=self.data.wpPlus
        wsMinus=self.data.wsMinus
        wsPlus=self.data.wsPlus
        type= self.GetTypeString()
        a=self.data.NormRange

        self.Aproximator.SetParams(As,Ap,wp,ws,wpMinus,wpPlus,wsMinus,wsPlus,type,a)
        aprox= self.data.GetAprox()
        if(aprox == ap.APROXIMACIONES[0]):
            self.Aproximator.butterworthAnalysis()
        elif(aprox == ap.APROXIMACIONES[1]):
            self.Aproximator.chebyshevAnalysis()
        elif(aprox == ap.APROXIMACIONES[2]):
            self.Aproximator.chebyshevInverseAnalysis()
        elif(aprox == ap.APROXIMACIONES[3]):
            self.Aproximator.besselAnalysis()
        finalFunc = self.Aproximator.getFunction()
        #Datos para la atenuacion y la fase
        w = np.logspace(-2, 10, 50000, endpoint=True)
        w, mag, phase = self.Aproximator.CalcBodePlot(w,finalFunc)
        self.data.setwVector(w)
        self.data.setMag(mag)
        self.data.setPhase(phase)
        #Respuest al impulso
        t_imp,h=(self.Aproximator.getFunction()).impulse()
        h=h.real
        self.data.setImpData(t_imp,h)
        t_step,u=(self.Aproximator.getFunction()).step()
        u=u.real
        self.data.setStepData(t_step,u)
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
    #Funciones que manejan eventos de la segunda etapa

    def OnPrevEv(self):
        if(self.GUI.ShowPrevMessage()):
            self.GUI.Change_to_stage1()
            self.estado=ETAPA1
    def OnSave2Ev(self):
        return
    def OnLoad2Ev(self):
        return