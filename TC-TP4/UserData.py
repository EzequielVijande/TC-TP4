class UserData(object):
    """Guarda la informacion ingresada por el usuario"""
    def __init__(self):
        #Se incializa con los siguientes valores por default
        self.type_of_filter=1 #Empieza por default con el numero del filtro LP
        self.Aproximation="Butterworth"
        self.Ap=0
        self.As=0
        self.wp=0
        self.ws=0
        self.wo=0
        self.wpMinus=0
        self.wpPlus=0
        self.wsMinus=0
        self.wsPlus=0
        self.Q=0
        self.NormRange=0 #Rango de desnormalizacion
        self.t0=0
        self.wrg=0
        self.Y=0
        self.StepTime=[0]
        self.StepResp=[0]
        self.ImpResp=[0]
        self.ImpTime=[0]
    #Setters
    def setFilter(self,filter):
        self.type_of_filter=filter

    def setAprox(self,Aprox):
        self.Aproximation=Aprox

    def setAp(self,Ap):
        self.Ap=Ap

    def setAs(self,As):
        self.As=As

    def setwp(self,wp):
        self.wp=wp

    def setws(self,ws):
        self.ws=ws
    def sett0(self,t0):
        self.sett0=t0
    def setwrg(self,wrg):
        self.wrg=wrg
    def setY(self,Y):
        self.Y=Y
    #Datos para graficar
    def setMag(self,mag):
        self.mag=mag

    def setPhase(self,phase):
        self.phase=phase
    def setfVector(self,f):
        self.f = f
    def setImpData(self,time,h):
        self.ImpTime=time
        self.ImpResp= h
    def setStepData(self,time,u):
        self.StepTime=time
        self.StepResp=u
    def GetPhaseMax(self):
        return self.phase.max()
    def GetPhaseMin(self):
        return self.phase.min()
    def SetZeroesAndPoles(self,zeroes,poles):
        self.zeroes_real=zeroes.real
        self.zeroes_imag=zeroes.imag
        self.poles_real= poles.real
        self.poles_imag=poles.imag
    def SetQValues(self,q):
        self.qs = q
        self.qs[(self.qs)<0]=0
    def SetGroupDelay(self,gd):
        self.gd= gd
    def SetAttnVector(self,Attn):
        self.Attn= Attn
    def SetfnVector(self,fn):
        self.fn= fn

    #Para BP Y BR
    def setwo(self,wo):
        self.wo=wo
    
    def setwpMinus(self,wpMinus):
        self.wpMinus=wpMinus

    def setwpPlus(self,wpPlus):
        self.wpPlus=wpPlus

    def setwsMinus(self,wsMinus):
        self.wsMinus=wsMinus

    def setwsPlus(self,wsPlus):
        self.wsPlus=wsPlus

    def setQ(self,Q):
        self.Q=Q

    #Getters
    def GetFilter(self):
        return self.type_of_filter

    def GetAprox(self):
        return self.Aproximation

    def GetAp(self):
       return self.Ap

    def GetAs(self):
        return self.As

    def GetAp(self):
        return self.wo

    def GetQ(self):
        return self.Q


