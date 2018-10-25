from scipy import signal
import math
import numpy as np
import control as c

class AproxAnalysis(object):

    def __init__(self, As=0, Ap=0, wp=0, ws=0, wpMinus=0, wpPlus=0, wsMinus=0, wsPlus=0, type="LP", a=0,tauZero=0,wrg=0,gamma=0,nMin = 0,nMax = 0,nUser = 0):
        
        return

    def SetParams(self,As=0, Ap=0, wp=0, ws=0, wpMinus=0, wpPlus=0, wsMinus=0, wsPlus=0, type="LP", a=0,tauZero=0,wrg=0,gamma=0):
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
        self.filterType = 'butterworth'
        self.poles = []
        self.zeros = []
        self.function = 0
        self.normFunction = 0
        self.tauZero = tauZero
        self.wrg = wrg
        self.gamma = gamma
        self.nMode = 'normal'
        self.nExceeded = False
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
        return

    def woCalc(self):
        if self.filterType == 'butterworth':
            if (self.type == 'LP'):
                wsf = (((10**(self.Ap/10)-1)/(10**(self.As/10)-1))**(1/(2*self.n)))*self.ws
                wpf = self.wp
                wo = (wsf**(self.a))*(wpf**(1-(self.a)))
            elif self.type == 'HP':
                wsf = (((10**(self.As/10)-1)/(10**(self.Ap/10)-1))**(1/(2*self.n)))*self.ws
                wpf = self.wp
                wo = (wsf**(self.a))*(wpf**(1-(self.a)))
            elif self.type == 'BP':
                wsDelta = (((10**(self.Ap/10)-1)/(10**(self.As/10)-1))**(1/(2*self.n)))*(self.wsPlus-self.wsMinus)
                wpDelta = self.wpPlus-self.wpMinus
                wo= (self.wpPlus*self.wpMinus)**(1/2)
                self.b = (wsDelta**(self.a))*(wpDelta**(1-(self.a)))/wo
            elif self.type == 'BR':
                wsDelta = (((10**(self.As/10)-1)/(10**(self.Ap/10)-1))**(1/(2*self.n)))*(self.wsPlus-self.wsMinus)
                wpDelta = self.wpPlus-self.wpMinus
                wo= (self.wpPlus*self.wpMinus)**(1/2)
                self.b = (wsDelta**(self.a))*(wpDelta**(1-(self.a)))/wo
        elif self.filterType == 'chebyshev':
            if (self.type == 'LP'):
                wo = self.wp
            elif self.type == 'HP':
                wo = self.wp
            elif self.type == 'BP':
                wo= (self.wpPlus*self.wpMinus)**(1/2)
            elif self.type == 'BR':
                wo= (self.wpPlus*self.wpMinus)**(1/2)
        elif self.filterType == 'inverseChebyshev':
            if (self.type == 'LP'):
                wo = self.wp
            elif self.type == 'HP':
                wo = self.wp
            elif self.type == 'BP':
                wo= (self.wpPlus*self.wpMinus)**(1/2)
            elif self.type == 'BR':
                wo= (self.wpPlus*self.wpMinus)**(1/2)
        return wo

    def kCalc(self,den,num):
        if self.filterType == 'butterworth' or self.filterType == 'inverseChebyshev':
            if den[len(den)-1] == 0 or num[len(num)-1] == 0:
                k=1
            else:
                k=den[len(den)-1]/num[len(num)-1]
        elif self.filterType == 'chebyshev':
            multiplier = (1 if (self.n%2==0) else 0)
            if den[len(den)-1] == 0 or num[len(num)-1] == 0:
                k=(10**(-self.Ap/20))**multiplier
            else:
                k=((10**(-self.Ap/20))**multiplier)*den[len(den)-1]/num[len(num)-1]
        return k

    def createFunction(self):

        wo = self.woCalc() #calculo wo para desnormalizacion
        pzFunction = signal.ZerosPolesGain(self.zeros,self.poles,1)
        coefFunction = pzFunction.to_tf() # num/den
        den = coefFunction.den
        num = coefFunction.num
        for i in range(0, len(den)):
            den[i] = den[i].real
        for i in range(0, len(num)):
            num[i] = num[i].real
        k = self.kCalc(den,num) #calculo constante
        self.normFunction = signal.ZerosPolesGain(self.zeros,self.poles,k) #guardo funcion normalizada
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
        return

    # BUTTERWORTH

    def butterworthAnalysis(self,type):
        self.nMode = type
        self.filterType = 'butterworth'
        self.poles = []
        self.zeros = []
        self.epsilonButterworth()
        if self.nMode == 'normal':
            self.nButterworth()
            if self.n > 20:
                self.n = 20
                self.nExceeded = True
        elif self.nMode == 'fixed':
            self.n = self.nUser
        elif self.nMode == 'range':
            self.nButterworth()
            if self.n > self.nMax:
                self.n = self.nMax
            elif self.n < self.nMin:
                self.n = self.nMin
        self.polesButterworth()
        self.createFunction()
        return

    def epsilonButterworth(self):
        self.epsilon = math.sqrt(math.pow(10,self.Ap/10)-1)
        return

    def nButterworth(self):
        log1 = math.log10((math.pow(10,self.As/10)-1)/(math.pow(self.epsilon,2)))
        log2 = math.log10(self.wsn)
        self.n = math.ceil(log1/(2*log2))
        return

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
        return

    # CHEBYSHEV

    def chebyshevAnalysis(self,type):
        self.nMode = type
        self.filterType = 'chebyshev'
        self.poles = []
        self.zeros = []
        self.epsilonChebyshev()
        if self.nMode == 'normal':
            self.nChebyshev()
            if self.n > 20:
                self.n = 20
                self.nExceeded = True
        elif self.nMode == 'fixed':
            self.n = self.nUser
        elif self.nMode == 'range':
            self.nChebyshev()
            if self.n > self.nMax:
                self.n = self.nMax
            elif self.n < self.nMin:
                self.n = self.nMin
        self.polesChebyshev()
        self.createFunction()
        return

    def epsilonChebyshev(self):
        self.epsilon = math.sqrt(math.pow(10,self.Ap/10)-1)
        return

    def nChebyshev(self):
        arcosh1 = math.acosh(math.sqrt(math.pow(10,self.As/10)-1)/self.epsilon)
        arcosh2 = math.acosh(self.wsn)
        self.n = math.ceil(arcosh1/arcosh2)
        return

    def polesChebyshev(self):
        for i in range(1, self.n+1):
            auxRe = math.sin(math.pi*((2*i-1)/(2*self.n)))*math.sinh(math.asinh(1/self.epsilon)/self.n)
            auxIm = math.cos(math.pi*((2*i-1)/(2*self.n)))*math.cosh(math.asinh(1/self.epsilon)/self.n)
            auxPole1 = complex(auxRe,auxIm)
            auxPole2 = complex(-auxRe,auxIm)
            if (auxPole1.real<0):
                self.poles.append(auxPole1)
            if (auxPole2.real<0):
                self.poles.append(auxPole2)
        return

    # CHEBYSHEV INVERSE

    def chebyshevInverseAnalysis(self,type):
        self.nMode = type
        self.filterType = 'inverseChebyshev'
        self.poles = []
        self.zeros = []
        self.epsilonChebyshevInverse()
        if self.nMode == 'normal':
            self.nChebyshevInverse()
            if self.n > 20:
                self.n = 20
                self.nExceeded = True
        elif self.nMode == 'fixed':
            self.n = self.nUser
        elif self.nMode == 'range':
            self.nChebyshevInverse()
            if self.n > self.nMax:
                self.n = self.nMax
            elif self.n < self.nMin:
                self.n = self.nMin
        self.polesChebyshevInverse()
        self.zerosChebyshevInverse()
        self.createFunction()
        return

    def epsilonChebyshevInverse(self):
        self.epsilon = 1/math.sqrt(math.pow(10,self.As/10)-1)
        return

    def nChebyshevInverse(self):
        arcosh1 = math.acosh(1/(self.epsilon*(math.sqrt(math.pow(10,self.Ap/10)-1))))
        arcosh2 = math.acosh(self.wsn)
        self.n = math.ceil(arcosh1/arcosh2)
        return

    def polesChebyshevInverse(self):
        beta = math.asinh(1/self.epsilon)/self.n
        for i in range(1, 2*self.n+1):
            alpha = math.pi*((2*i-1)/(2*self.n))
            auxRe = self.wsn*math.sin(alpha)*math.sinh(beta)/(math.pow(math.sin(alpha)*math.sinh(beta),2)+math.pow(math.cos(alpha)*math.cosh(beta),2))
            auxIm = -self.wsn*math.cos(alpha)*math.cosh(beta)/(math.pow(math.sin(alpha)*math.sinh(beta),2)+math.pow(math.cos(alpha)*math.cosh(beta),2))
            auxPole = complex(auxRe,auxIm)
            if (auxPole.real<0):
                self.poles.append(auxPole)
        return

    def zerosChebyshevInverse(self):
        for i in range(1, self.n+1):
            alpha = math.pi*((2*i-1)/(2*self.n))
            auxIm = self.wsn/math.cos(alpha)
            auxZero = complex(0,auxIm)
            if auxIm < 10**10:
                self.zeros.append(auxZero)
        return

    # BESSEL

    def besselAnalysis(self,type):
        self.nMode = type
        self.filterType = 'bessel'
        self.poles = []
        self.zeros = []
        self.createBesselFunction()
        return

    def createBesselFunction(self):
        self.n = 1
        condition = False
        wrgn= self.wrg*self.tauZero
        if self.nMode == 'normal' or self.nMode == 'range':
            while condition == False:
                AkArray = self.calcAkArray()
                #ahora creo funcion normalizada
                self.normFunction = signal.TransferFunction([1],AkArray)
                #calculo retardo de grupo y evaluo en wrgn
                w, h = signal.freqs([1], AkArray)
                groupDelay = -np.diff(np.unwrap(np.angle(h))) / np.diff(w)
                diff = abs(w - wrgn)
                diff = list(diff)
                index = diff.index(min(diff))
                tauWrgn = groupDelay[index]
                if tauWrgn >= 1-self.gamma:
                    condition = True
                else:
                    self.n = self.n + 1
        elif self.nMode == 'fixed':
            self.n = self.nUser
            AkArray = self.calcAkArray()
        if self.nMode == 'range':
            if self.n > self.nMax:
                self.n = self.nMax
                AkArray = self.calcAkArray()
            elif self.n < self.nMin:
                self.n = self.nMin
                AkArray = self.calcAkArray()
        if self.n > 20:
            self.n = 20
            AkArray = self.calcAkArray()
            self.nExceeded = True
        #tengo el n correcto, desnormalizo
        for i in range(0,len(AkArray)):
            AkArray[len(AkArray)-1-i]=AkArray[len(AkArray)-1-i]*(self.tauZero**i)
        self.function = signal.TransferFunction([1],AkArray)
        return

    def calcAkArray(self):
        AkArray = [1]
        for i in range(1,self.n+1):
            Ak = (math.factorial(2*self.n-i)/(math.factorial(i)*math.factorial(self.n-i)*(2**(self.n-i))))*(((2**self.n)*(math.factorial(self.n)))/math.factorial(2*self.n))
            AkArray.insert(0,Ak)
        return AkArray

    # GAUSS

    def gaussAnalysis(self,type):
        self.nMode = type
        self.filterType = 'gauss'
        self.poles = []
        self.zeros = []
        self.createGaussFunction()
        return

    def gaussDenGenerator(self):
        coef = self.gaussPolynomialCoef()
        auxPoles = np.roots(coef)
        poles = []
        for i in range(0,auxPoles.size):
            if auxPoles[i].real < 0:
                poles.append(auxPoles[i])
        pzfunc = signal.ZerosPolesGain([],poles,1)
        self.normFunction = pzfunc.to_tf()
        den = self.normFunction.den
        return den

    def createGaussFunction(self):
        self.n = 1
        condition = False
        wrgn= self.wrg*self.tauZero
        if self.nMode == 'normal' or self.nMode == 'range':
            while condition == False:
                #armo polinomio de orden n y calculo polos
                den = self.gaussDenGenerator()
                #calculo retardo de grupo y evaluo en wrgn
                w, h = signal.freqs([1], den)
                groupDelay = -np.diff(np.unwrap(np.angle(h))) / np.diff(w)
                diff = abs(w - wrgn)
                diff = list(diff)
                index = diff.index(min(diff))
                tauWrgn = groupDelay[index-1]
                if tauWrgn >= 1-self.gamma:
                    condition = True
                else:
                    self.n = self.n + 1
        elif self.nMode == 'fixed':
            self.n = self.nUser
            den = self.gaussDenGenerator()
        if self.nMode == 'range':
            if self.n > self.nMax:
                self.n = self.nMax
                den = self.gaussDenGenerator()
            elif self.n < self.nMin:
                self.n = self.nMin
                den = self.gaussDenGenerator()
        if self.n > 20:
            self.n = 20
            den = self.gaussDenGenerator()
            self.nExceeded = True
        #tengo el n correcto, desnormalizo
        for i in range(0,len(den)):
            den[len(den)-1-i]=den[len(den)-1-i]*(self.tauZero**i)
        self.function = signal.TransferFunction([1],den)
        return

    def gaussPolynomialCoef(self):
        p = [1]
        for i in range(1,self.n+1):
            p.insert(0,0)
            pAux = 1/math.factorial(i)
            p.insert(0,pAux)
        return p;

    # Getters

    def getFunction(self):
        return self.function

    def getNormFunction(self):
        return self.normFunction

    # Setter 

    def setnRange(self,nMin,nMax):
        self.nMin = int(nMin)
        self.nMax = int(nMax)
        return

    def setnFixed(self,num):
        self.nUser = int(num)
        return

    def resetnExceeded(self):
        self.nExceeded = False
        return

    #Extras
    def CalcBodePlot(self,w,func):
        wFinal, magFinal, phaseFinal = signal.bode(func,w)
        return wFinal,magFinal,phaseFinal

    def CalcGroupDelay(self,w,func):
        w, h = signal.freqs(func.num, func.den,w)
        gdFinal = -np.diff(np.unwrap(np.angle(h))) / np.diff(w)
        gdFinal = np.append(gdFinal,gdFinal[len(gdFinal)-1])
        return w, gdFinal

    