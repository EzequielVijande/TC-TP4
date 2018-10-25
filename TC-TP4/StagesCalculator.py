from scipy import signal
import math
import numpy
import control as c

class StagesCalculator(object):
    """clase que se encarga de dividir la transferencia en etapas y realizar
        todas las cuentas relacionadas a la segunda etapa del diseño"""
    def __init__(self,func):
        self.total_transf= func
        self.stages=[]
        self.GatherPolesAndZeroes() #junto los polos con sus ceros mas cercanos
        self.DefineCascadeOrder() #ordeno de menor q a mayor q
        self.ObtainStagesGains() #encuentro las constantes de cada etapa para maximizar rango dinamico

    def GatherPolesAndZeroes(self):
        #Funcion que junta los polos y ceros cercanos en una misma transferencia
        self.pairs=list()
        dist= list()
        zeros= list(self.total_transf.zeros)
        poles= list(self.total_transf.poles)
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

        return
    def DefineCascadeOrder(self):
        return
        #funcion que ordena las etapas en orden de menor Q a mayor Q
    def ObtainStagesGains(self):
        return
        #Funcion que calcula la constante que corresponde a cada etapa

    #Funciones de calculo
    def CalculateDistance(self,x1,y1,x2,y2):
        delta_x= abs(x1-x2)
        delta_y= abs(y1-y2)
        distance= ((delta_x**2)+(delta_y**2))**(0.5)
        return distance
    #def RemovePoleFromCOn



