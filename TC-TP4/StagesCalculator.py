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

    def GatherPolesAndZeroes(self):
        #Funcion que junta los polos y ceros cercanos en una misma transferencia
        return
    def DefineCascadeOrder(self):
        return
        #funcion que ordena las etapas en orden de menor Q a mayor Q
    def ObtainStagesGains(self):
        return
        #Funcion que calcula la constante que corresponde a cada etapa


