
import UserData
import ApGUI as ap

#Estados
EXIT=0
ETAPA1=1


class Manager(object):
    """Clase que se ocupa de vincular la logica con la GUI"""
    def __init__(self, data,GUI):
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

            self.GUI.EventSolved()    #Settea que ya no hay evento a resolver   

    #Funciones que manejan eventos
    def OnNoEv(self):
        return

    def OnGraphEv(self):
        result_str= self.ValidateInputs()
        if(result_str!="Ok"):
            self.GUI.DisplayError(result_str)
        #else:
        #   self.ShowGraph()

    def OnQuitEv(self):
        self.GUI.CloseGUI()
        self.estado=EXIT
        return

    def OnSaveEv(self):
        return

    def OnLoadEv(self):
        return

    def OnNextEv(self):
        return
    def OnChangeGraphEv(self):
        return
    def OnPutTemplate(self):
        return
    def Error(self):
        return
    #Funciones auxiliares
    def ValidateInputs(self):
        fil=self.GUI.filter.get()
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
                if(ws<=wp):
                    return "wp debe ser menor que ws"
            else: #Si es un HP el wp debe ser mayor al ws
                if(ws>=wp):
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