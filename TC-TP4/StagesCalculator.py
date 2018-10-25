from scipy import signal
import math
import numpy as np
import control as c

class StagesCalculator(object):
    """clase que se encarga de dividir la transferencia en etapas y realizar
        todas las cuentas relacionadas a la segunda etapa del diseño"""
    def __init__(self,func):
        self.total_transf= func
        self.stages=[]
        self.Q = []
        self.GatherPolesAndZeroes() #junto los polos con sus ceros mas cercanos
        self.DefineCascadeOrder() #ordeno de menor q a mayor q
        self.ObtainStagesGains() #encuentro las constantes de cada etapa para maximizar rango dinamico

    def GatherPolesAndZeroes(self):
        #Funcion que junta los polos y ceros cercanos en una misma transferencia
        self.pairs=list()
        dist= list()
        zeros= list(self.total_transf.zeros)
        poles= list(self.total_transf.poles)
        poles= self.RemovePoleFromComplexPair(poles)
        for j in range(0, len(zeros)):
            zero_act= zeros[j]
            for i in range(0, len(poles)):
                pole_act= poles[i]
                dist.append(self.CalculateDistance(zero_act.real,zero_act.imag,pole_act.real,pole_act.imag))
            min_index= dist.index(min(dist))
            pair=(zero_act,poles.pop(min_index))
            self.pairs.append(pair)
            dist.clear()
        #Junto los polos que me quedan en otras funciones transferencia
        self.remainingPoles= poles
        self.GetStagesTransferFunctions()
        return

    def DefineCascadeOrder(self):
        for i in range(0,len(self.stages)):
            Qaux = -abs(self.stages[i].poles[0])/(2*self.stages[i].poles[0].real)
            self.Q.append(Qaux)
        # tengo en Q los Qi correspondientes a cada etapa
        self.Q, self.stages = zip(*sorted(zip(self.Q, self.stages)))
        return
        #funcion que ordena las etapas en orden de menor Q a mayor Q

    def ObtainStagesGains(self):
        M = []
        K = []
        for i in range(0,len(self.stages)):
            Mj = self.calcMaxGain(self.stages[i])
            M.append(Mj)
        pzFunc = self.total_transf.to_zpk()
        Ko = pzFunc.gain*(M[len(M)-1]/M[0])
        K.append(Ko)
        for i in range(1,len(self.stages)):
            auxK = (M[i-1])/(M[i])
            K.append(auxK)
        for i in range(0,len(self.stages)):
            (self.stages[i]).gain= (K[i].real)
        return
        #Funcion que calcula la constante que corresponde a cada etapa

    def calcMaxGain(self,func):
        w, mag, phase = signal.bode(func)
        Mj = max(mag)
        return Mj

    #Funciones de calculo
    def CalculateDistance(self,x1,y1,x2,y2):
        delta_x= abs(x1-x2)
        delta_y= abs(y1-y2)
        distance= ((delta_x**2)+(delta_y**2))**(0.5)
        return distance
    def RemovePoleFromComplexPair(self,poles):
        i=0
        while (i<(len(poles))):
            pole_act= poles[i]
            j=i+1
            while( (j<len(poles)) and (abs(pole_act.real-((poles[j]).real))>0.1) ):
                j=j+1
            if((j<len(poles)) and abs(pole_act.imag+(poles[j]).imag)<=0.1):
                poles.pop(j)
            i=i+1
        return poles

    def GetStagesTransferFunctions(self):
        funcs=[]
        for i in range(0,len(self.pairs)):
            zero,pole1=self.pairs[i]
            pole2= complex(pole1.real,-(pole1.imag))
            aux= signal.ZerosPolesGain(zero,[pole1,pole2],1)
            funcs.append(aux)
        for i in range(0,len(self.remainingPoles)):
            p1= self.remainingPoles[i]
            p2= complex(p1.real,-(p1.imag))
            aux= signal.ZerosPolesGain([],[p1,p2],1)
            funcs.append(aux)
        self.stages=funcs
    def GetNumberOfStages(self):
        return len(self.stages)

    def CalculateBode(self,index):
        #Calcula lo necesario para graficar el bode de la etapa i-esima
        w= np.logspace(-1, 7, 90000, endpoint=True)
        w,mag,fase= signal.bode( (self.stages[index]),w)
        return (w/(2*math.pi)),mag

    def UpdateParameters(self,index):
        transf_act= self.stages[index]
        poles=transf_act.poles
        zeros=transf_act.zeros
        Qp=-(abs(poles[0])/(2*poles[0].real))
        wp=abs(poles[0])
        fp= wp/(2*math.pi)
        num= (transf_act.to_tf()).num
        den= (transf_act.to_tf()).den
        k=num[len(num)-1]/den[len(den)-1]
        return fp,Qp,k




