
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
        return

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

