'''
oggetto macchina per memorizzre i valori letti
'''

class macchina:
    def __init__(self,):
        self.velocita = None
        self.pedale_acceleratore = None
        self.giri_motore = None
        self.temperatura_motore = None
        self.freccia = None
        self.luci = None


    def info(self):
        print(f"{self.velocita}   {self.pedale_acceleratore}     {self.giri_motore}")




