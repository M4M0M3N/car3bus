'''
oggetto macchina per memorizzre i valori letti
'''

class macchina:
    def __init__(self,):
        self.velocita = 0
        self.pedale_acceleratore = 0
        self.giri_motore = 0
        self.temperatura_motore = 0
        self.freccia = 0
        #0 spente, 1 anabagglianti, 2 abbaglianti
        self.luci = 0
        self.marcia = 0
        self.pressione_turbo = 1.1


    def info(self):
        print(f"{self.velocita}   {self.pedale_acceleratore}     {self.giri_motore}")




