'''
script fake utilizzato per passare dati precedentemente letti da obd e memorizzati nel file
'''
import os
from converti import *
from time import sleep

class obd_read:
    def __init__(self, m):

        #apro il file utilizzato per database
        # Percorso generale: cerca il file nella stessa cartella dello script
        db_path = os.path.join(os.path.dirname(__file__), 'database.txt')
        try:
            f = open(db_path, 'r')
        except Exception as e:
            print(e)
            print(os.listdir(os.path.dirname(__file__)))
            exit()

        righe = f.readlines()
        f.close()

        for r in righe:
            #leggo il file
            obd_read = r
            sleep(0.01)

            #se legggo pippo vuol dire che il file è terminato
            if obd_read == 'pippo':
                print("finito il file, ricomincio")
                exit(0)

            try:
                #divido la stringa nei vari valori
                #esempio di stringa 75,00,00,230007DD46518300
                address_id, rtr, dlc, value = obd_read.split(',')
                value = value[:-1]  # rimuovo l'ultimo carattere che è un \n
                
                if address_id == '202': #202 e' l'indirizzo che contiene queste informazioni: rmp, gas pedal

                    #converto i giri del motore e li salvo nell'oggetto macchina
                    rpm = conv_rmp(value)
                    m.giri_motore = round(rpm)

                    #converto la posizione dell'acceleratore e li salvo nell'oggetto macchina
                    gas = conv_gas(value)
                    m.pedale_acceleratore = round(gas)

                    #converto la velocità e li salvo nell'oggetto macchina
                    vel = conv_vel(value)
                    m.velocita = round(vel)

                    #print(f"       {round(rpm)}   {round(gas)}   {round(vel)}")

                elif address_id == '420':  #420 e' l'indirizzo che contiene queste informazioni: temperatura acqua

                    temp = conv_temp(value)
                    m.temperatura_motore = temp

                    #print(temp)
                
                elif address_id == '130' and False:  # 0x130 → informazioni cambio marcia
                    #raw = int(value[-4:], 16)
                    if conv_marcie(value) != 'Sconosciuto':
                        m.marcia = conv_marcie(value)
                    print(m.marcia)

                elif address_id == '91':  # 0x91 → contiene stato abbaglianti (byte finale)
                    #print(value)
                    m.luci, m.freccia = conv_luci(value)

            except:
                print(obd_read)
