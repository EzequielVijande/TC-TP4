class UserData(object):
    """Guarda la informacion ingresada por el usuario"""
    def __init__(self):
        #Se incializa con los siguientes valores por default
        self.type_of_filter=1 #Empieza por default con el numero del filtro LP
        self.Aproximation="Butterworth"
        self.Ap=0
        self.As=0
        self.wo=0
        self.Q=0
        self.NormRange=0 #Rango de desnormalizacion
    #Setters
    def setFilter(self,filter):
        self.type_of_filter=filter
        print(filter)

    def setAprox(self,Aprox):
        self.Aproximation=Aprox

    def setAp(self,Ap):
        self.Ap=Ap

    def setAs(self,As):
        self.As=As

    def setAp(self,wo):
        self.wo=wo

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


