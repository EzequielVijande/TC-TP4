from scipy import signal
import math
import numpy
import control as c

class AproxAnalysis(object):

    def __init__(self, As=0, Ap=0, wp=0, ws=0, wpMinus=0, wpPlus=0, wsMinus=0, wsPlus=0, type="LP", a=0):
        
        return;
    def SetParams(self,As=0, Ap=0, wp=0, ws=0, wpMinus=0, wpPlus=0, wsMinus=0, wsPlus=0, type="LP", a=0):
        self.As = As
        self.Ap = Ap
        self.wp = wp
        self.ws = ws
        self.wpMinus = wpMinus
        self.wpPlus = wpPlus
        self.wsMinus = wsMinus
        self.wsPlus = wsPlus
        self.type = type
        self.epsilon = 0
        self.wsn = 0
        self.n = 0
        self.b = 0 # bandwidth
        self.a = a # porcentaje de desnormalizacion [0-1]
        self.poles = []
        self.zeros = []
        self.function = 0
        self.normFunction = 0
        if (self.type == 'BP') or (self.type == 'BR'):
            self.b = (self.wpPlus-self.wpMinus)/(math.sqrt(self.wpPlus*self.wpMinus))
        self.wsnCalc()
        
    # GENERAL    

    def wsnCalc(self):
        if (self.type == 'LP'):
            self.wsn = self.ws/self.wp
        elif (self.type == 'HP'):
            self.wsn = self.wp/self.ws
        elif (self.type == 'BP'):
            self.wsn = (self.wsPlus-self.wsMinus)/(self.wpPlus-self.wpMinus)
        elif (self.type == 'BR'):
            self.wsn = (self.wpPlus-self.wpMinus)/(self.wsPlus-self.wsMinus)
        else:
            self.wsn = math.nan
        return;

    def createFunction(self):

        if (self.type == 'LP'):
            wsf = (((10**(self.Ap/10)-1)/(10**(self.As/10)-1))**(1/(2*self.n)))*self.ws
            wpf = self.wp
            wo = (wsf**(self.a))*(wpf**(1-(self.a)))
        elif (self.type == 'HP'):
            wsf = (((10**(self.As/10)-1)/(10**(self.Ap/10)-1))**(1/(2*self.n)))*self.ws
            wpf = self.wp
            wo = (wsf**(self.a))*(wpf**(1-(self.a)))
        elif (self.type == 'BP'):
            wsf = (((10**(self.Ap/10)-1)/(10**(self.As/10)-1))**(1/(2*self.n)))*(self.wsPlus-self.wsMinus)
            wpf = self.wpPlus-self.wpMinus
            wo= (self.wpPlus*self.wpMinus)**(1/2)
        elif (self.type == 'BR'):
            wsf = (((10**(self.As/10)-1)/(10**(self.Ap/10)-1))**(1/(2*self.n)))*(self.wsPlus-self.wsMinus)
            wpf = self.wpPlus-self.wpMinus
            wo= (self.wpPlus*self.wpMinus)**(1/2)

        pzFunction = signal.ZerosPolesGain(self.zeros,self.poles,1)
        coefFunction = pzFunction.to_tf() # num/den
        den = coefFunction.den
        num = coefFunction.num
        for i in range(0, len(den)):
            den[i] = den[i].real
        for i in range(0, len(num)):
            num[i] = num[i].real

        #calculo constante
        if den[len(den)-1] == 0:
            k=1
        elif num[len(num)-1] == 0:
            k=1
        else:
            k=den[len(den)-1]/num[len(num)-1]

        self.normFunction = signal.ZerosPolesGain(self.zeros,self.poles,k)


        # desnormalizo segun tipo de filtro
        if self.type == 'LP':
            s = c.tf([1,0],[wo])
        elif self.type == 'HP':
            s = c.tf([wo],[1,0])
        elif self.type == 'BP':
            s = c.tf([1,0,wo**2],[1,0])/(wo*self.b)
        elif self.type == 'BR':
            s = c.tf([1,0],[1,0,wo**2])*wo*self.b
        ft = c.tf([1],[1])
        for i in range(0, len(self.poles)):
            aux = 1/(s-self.poles[i])
            ft = ft*aux
        for i in range(0, len(self.zeros)):
            aux = s - self.zeros[i]
            ft = ft*aux
        #creo funcion final
        self.function = signal.TransferFunction(k*ft.num[0][0],ft.den[0][0])
        return;

    # BUTTERWORTH

    def butterworthAnalysis(self):
        self.poles = []
        self.zeros = []
        self.epsilonButterworth()
        self.nButterworth()
        self.polesButterworth()
        self.createFunction()
        return;

    def epsilonButterworth(self):
        self.epsilon = math.sqrt(math.pow(10,self.Ap/10)-1)
        return;

    def nButterworth(self):
        log1 = math.log10((math.pow(10,self.As/10)-1)/(math.pow(self.epsilon,2)))
        log2 = math.log10(self.wsn)
        self.n = math.ceil(log1/(2*log2))
        return;

    def polesButterworth(self):
        if (self.n%2) == 0:
            multiplier = 2
        else:
            multiplier = 1
        mag = 1/math.pow(self.epsilon,1/self.n)
        for i in range(0, 2*self.n):
            auxRe = mag*math.cos(math.pi*((multiplier*i-1)/(multiplier*self.n)))
            auxIm = mag*math.sin(math.pi*((multiplier*i-1)/(multiplier*self.n)))
            auxPole = complex(auxRe,auxIm)
            if (auxPole.real<0):
                self.poles.append(auxPole)
        return;

    # CHEBYSHEV

    def chebyshevAnalysis(self):
        self.poles = []
        self.zeros = []
        self.epsilonChebyshev()
        self.nChebyshev()
        self.polesChebyshev()
        self.createFunction()
        return;

    def epsilonChebyshev(self):
        self.epsilon = math.sqrt(math.pow(10,self.Ap/10)-1)
        return;

    def nChebyshev(self):
        arcosh1 = math.acosh(math.sqrt(math.pow(10,self.As/10)-1)/self.epsilon)
        arcosh2 = math.acosh(self.wsn)
        self.n = math.ceil(arcosh1/arcosh2)
        return;

    def polesChebyshev(self):
        for i in range(1, self.n+1):
            auxRe = math.sin(math.pi*((2*i-1)/(2*self.n)))*math.sinh(math.acosh(1/self.epsilon)/self.n)
            auxIm = math.cos(math.pi*((2*i-1)/(2*self.n)))*math.cosh(math.acosh(1/self.epsilon)/self.n)
            auxPole1 = complex(auxRe,auxIm)
            auxPole2 = complex(-auxRe,auxIm)
            if (auxPole1.real<0):
                self.poles.append(auxPole1)
            if (auxPole2.real<0):
                self.poles.append(auxPole2)
        return;

    # CHEBYSHEV INVERSE

    def chebyshevInverseAnalysis(self):
        self.poles = []
        self.zeros = []
        self.epsilonChebyshevInverse()
        self.nChebyshevInverse()
        self.polesChebyshevInverse()
        self.zerosChebyshevInverse()
        self.createFunction()
        return;

    def epsilonChebyshevInverse(self):
        self.epsilon = 1/math.sqrt(math.pow(10,self.As/10)-1)
        return;

    def nChebyshevInverse(self):
        arcosh1 = math.acosh(1/(self.epsilon*(math.sqrt(math.pow(10,self.Ap/10)-1))))
        arcosh2 = math.acosh(self.wsn)
        self.n = math.ceil(arcosh1/arcosh2)
        return;

    def polesChebyshevInverse(self):
        beta = math.asinh(1/self.epsilon)/self.n
        for i in range(1, 2*self.n+1):
            alpha = math.pi*((2*i-1)/(2*self.n))
            auxRe = self.wsn*math.sin(alpha)*math.sinh(beta)/(math.pow(math.sin(alpha)*math.sinh(beta),2)+math.pow(math.cos(alpha)*math.cosh(beta),2))
            auxIm = -self.wsn*math.cos(alpha)*math.cosh(beta)/(math.pow(math.sin(alpha)*math.sinh(beta),2)+math.pow(math.cos(alpha)*math.cosh(beta),2))
            auxPole = complex(auxRe,auxIm)
            if (auxPole.real<0):
                self.poles.append(auxPole)
        return;

    def zerosChebyshevInverse(self):
        for i in range(1, 2*self.n+1):
            alpha = math.pi*((2*i-1)/(2*self.n))
            auxIm = self.wsn/math.cos(alpha)
            auxZero = complex(0,auxIm)
            self.zeros.append(auxZero) # VER CUAL DEL PAR AGARRAR
        return;

    # BESSEL

    def besselAnalysis(self):
        self.poles = []
        self.zeros = []
        self.epsilonBessel()
        self.nBessel()
        self.polesBessel()
        self.createFunction()
        return;

    def epsilonBessel(self):
        self.epsilon = math.sqrt(math.pow(10,self.Ap/10)-1)
        return;

    def nBessel(self):
        # por iteracion (wat)
        return;

    def polesBessel(self):
        # hacer
        return;

    # Getters

    def getFunction(self):
        return self.function

    #Extras
    def CalcBodePlot(self,w,func):
        w_r, mag_r, phase_r = signal.bode(func,w)
        return w_r,mag_r,phase_r