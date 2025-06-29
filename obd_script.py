#import can
import serial
from converti import *

'''
script per leggere i dati tramite interfaccia obd, analizzarli e scirverli nell'oggetto macchina
'''

from time import sleep

class obd_read:
    def __init__(self, m):

        arduino = serial.Serial('/dev/ttyUSB0', 250000, timeout=1)  # o ttyACM0
        while True:
            
            linea = arduino.readline().decode('utf-8').strip()
            print(f"Ricevuto: {linea}")
            #sleep(0.5)
            #leggo il valore canbus
            message = linea
            #print(f"Received CAN frame: {message}")

            try:
                #divido la stringa nei vari valori
                #esempio di stringa 75,00,00,230007DD46518300
                address_id, rtr, dlc, value = message.split(',')

                if address_id == '202':  #202 e' l'indirizzo che contiene queste informazioni: rmp, gas pedal

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

                    print(temp)

                    '''elif address_id == '9F':  #marce ??

                    temp = value

                    print(f"{int(value[0:2],16)}  {int(value[2:4],16)}  {int(value[4:6],16)}  {int(value[6:8],16)}  ")#'''

            except:
                print(message)
