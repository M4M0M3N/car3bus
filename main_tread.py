'''
main script dove si crea l'oggetto macchina e si gestisono i tread dei servizii collegati
'''

from threading import Thread

import gui_script
from macchina import macchina
from time import sleep


#Qui si sceglie far eseguire lo scrip fake che legge il file
from fake_obd_script import obd_read

#oppure lo script che legge direttamente da odb
#from obd_script import obd_read


m = macchina()

#metodo usato per avviare i diversi tread
def start_tread( target, oggetto):
    t = Thread(target=target, args=(oggetto, ))
    t.start()
    return t


m = macchina()

t_obd = start_tread(obd_read, m)
t_gui = start_tread(gui_script.run, m)


while True:

    if not t_obd.is_alive():
        t_obd = start_tread(obd_read, m)

    if not t_gui.is_alive():
        t_gui = start_tread(gui_script.run, m)

    sleep(1)



